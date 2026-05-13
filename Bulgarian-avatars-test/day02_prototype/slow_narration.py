"""Post-process the existing day02-master.mp3 to slow down English-narration
segments — without making any new ElevenLabs calls (quota exhausted).

Approach: slice each segment out of the existing master by its timestamp,
apply atempo=0.92 to slow-prefix segments, re-concat with the original
pause structure. Writes a fresh master + updated timing JSON.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
ELENA = ROOT / "assets" / "elena"
MASTER_IN = ELENA / "day02-master.mp3"
SEGS_IN = ELENA / "day02-master-segments.json"
MASTER_OUT = ELENA / "day02-master.mp3"  # overwrite
SEGS_OUT = ELENA / "day02-master-segments.json"  # overwrite
WORK = ELENA / "_work_slowed"
WORK.mkdir(exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Same pause structure as the original builder.
NARRATION_PAUSE_MS = 600
PHRASE_PAUSE_MS = 850
SECTION_PAUSE_MS = 1200
HEAD_MS = 250
TAIL_MS = 400

SLOW_PREFIXES = ("cold_open", "recap_intro", "intro_", "spotlight_", "outro")

# Map of segment_id → which gap follows it. Mirrors the original script's
# structure. Anything ending a major section gets SECTION_PAUSE_MS.
END_OF_SECTION = {
    "cold_open", "recap_11",
    "intro_s2", "intro_s3", "intro_s4", "intro_s5", "intro_s6",
    "intro_s7", "intro_s8", "intro_roleplays",
    "rp3_friend_4",
    "spotlight_te", "spotlight_mersi", "spotlight_zapovyadayte",
    "spotlight_vie", "spotlight_dobra_vs_dobar", "spotlight_ucha_bg",
}


def is_slow(seg_id: str) -> bool:
    return any(seg_id.startswith(p) for p in SLOW_PREFIXES)


def extract(src: Path, start_s: float, end_s: float, dest: Path) -> None:
    """Extract [start_s, end_s] from src into dest, re-encoded."""
    duration = end_s - start_s
    subprocess.run(
        [FFMPEG, "-y", "-ss", f"{start_s}", "-t", f"{duration}",
         "-i", str(src), "-acodec", "libmp3lame", "-b:a", "128k",
         "-ar", "44100", "-ac", "1", str(dest)],
        capture_output=True, check=True, timeout=60,
    )


def slow_down(src: Path, dest: Path, factor: float = 0.92) -> None:
    subprocess.run(
        [FFMPEG, "-y", "-i", str(src), "-af", f"atempo={factor}",
         "-acodec", "libmp3lame", "-b:a", "128k",
         "-ar", "44100", "-ac", "1", str(dest)],
        capture_output=True, check=True, timeout=60,
    )


def probe_duration_s(path: Path) -> float:
    result = subprocess.run(
        [FFMPEG, "-i", str(path)],
        capture_output=True, text=True, check=False, timeout=30,
    )
    blob = (result.stdout or "") + (result.stderr or "")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", blob)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def make_silence(duration_ms: int, out_path: Path) -> None:
    if out_path.exists():
        return
    seconds = duration_ms / 1000.0
    subprocess.run(
        [FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
         "-t", f"{seconds}", "-q:a", "9", "-acodec", "libmp3lame",
         "-ar", "44100", "-ac", "1", str(out_path)],
        capture_output=True, check=True, timeout=30,
    )


def concat_mp3s(parts: list[Path], out_path: Path) -> None:
    list_file = WORK / "_concat.txt"
    list_file.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in parts),
        encoding="utf-8",
    )
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-af", "loudnorm=I=-14:LRA=11:TP=-1.5",
         "-ar", "44100", "-ac", "1", "-acodec", "libmp3lame", "-b:a", "128k",
         str(out_path)],
        capture_output=True, check=True, timeout=300,
    )


def main() -> None:
    segs_data = json.loads(SEGS_IN.read_text(encoding="utf-8"))
    segments_in = segs_data["segments"]
    print(f"Loaded {len(segments_in)} segments from {SEGS_IN}")
    print(f"Slowing {sum(1 for s in segments_in if is_slow(s['id']))} segments by 8%")

    # Silences
    head_sil = WORK / f"sil_{HEAD_MS}.mp3"
    tail_sil = WORK / f"sil_{TAIL_MS}.mp3"
    phrase_sil = WORK / f"sil_{PHRASE_PAUSE_MS}.mp3"
    section_sil = WORK / f"sil_{SECTION_PAUSE_MS}.mp3"
    for ms, p in [(HEAD_MS, head_sil), (TAIL_MS, tail_sil),
                  (PHRASE_PAUSE_MS, phrase_sil), (SECTION_PAUSE_MS, section_sil)]:
        make_silence(ms, p)

    # Extract each segment, slow if applicable
    extracted: dict[str, Path] = {}
    for seg in segments_in:
        sid = seg["id"]
        raw_path = WORK / f"{sid}_raw.mp3"
        extract(MASTER_IN, seg["start"], seg["end"], raw_path)
        if is_slow(sid):
            final_path = WORK / f"{sid}_slow.mp3"
            slow_down(raw_path, final_path)
        else:
            final_path = raw_path
        extracted[sid] = final_path

    # Re-concat with the original pause structure
    parts: list[Path] = [head_sil]
    cursor_s = HEAD_MS / 1000.0
    new_segments: list[dict] = []
    for i, seg in enumerate(segments_in):
        sid = seg["id"]
        clip = extracted[sid]
        dur = probe_duration_s(clip)
        parts.append(clip)
        start_s = cursor_s
        end_s = cursor_s + dur
        new_segments.append({"id": sid, "start": round(start_s, 3), "end": round(end_s, 3)})
        cursor_s = end_s
        if i < len(segments_in) - 1:
            if sid in END_OF_SECTION:
                parts.append(section_sil); cursor_s += SECTION_PAUSE_MS / 1000.0
            else:
                parts.append(phrase_sil); cursor_s += PHRASE_PAUSE_MS / 1000.0
    parts.append(tail_sil)
    cursor_s += TAIL_MS / 1000.0

    concat_mp3s(parts, MASTER_OUT)
    print(f"\nWrote {MASTER_OUT}")
    print(f"  total: {cursor_s:.2f}s ({cursor_s/60:.2f} min)")
    print(f"  size:  {MASTER_OUT.stat().st_size//1024} KB")

    segs_data["segments"] = new_segments
    segs_data["total_seconds"] = round(cursor_s, 3)
    segs_data["post_process"] = "narration slowed by atempo=0.92"
    SEGS_OUT.write_text(json.dumps(segs_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {SEGS_OUT}")


if __name__ == "__main__":
    main()
