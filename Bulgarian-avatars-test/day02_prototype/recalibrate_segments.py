"""Recalibrate segment timings against the actual rendered MP4.

Hypereal trims/pads slightly during encoding (we observed ~4s drift on
the 6:48 master). The source-audio timings in day02-master-segments.json
DON'T match what's actually in the MP4 — so buttons land in the wrong
place, especially late in the file.

This script uses ffmpeg's silencedetect filter to find the gaps between
spoken segments in the MP4, then re-pairs them with the segment IDs in
the original order (we know there are 91 segments). The output JSON
is frame-accurate to the MP4.
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
MP4 = ROOT / "clips" / "day02" / "elena-day02-master-fs.mp4"
SEGS_IN = ROOT / "assets" / "elena" / "day02-master-segments.json"
SEGS_OUT = ROOT / "assets" / "elena" / "day02-master-segments-calibrated.json"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# silencedetect parameters tuned for our master:
#   noise = -45dB     loud enough to ignore atempo residue but quiet enough to
#                     catch our anullsrc-generated gaps
#   duration = 0.35   smaller than our shortest gap (600ms narration pause)
NOISE_DB = -45
# Min gap = 0.7s sits comfortably between our shortest inter-segment gap
# (PHRASE_PAUSE_MS=850ms, unaltered by atempo) and the longest internal
# pause inside a slowed narration segment (~550ms — sentence breaks at
# atempo=0.92 of ElevenLabs' ~500ms period pauses).
MIN_GAP_S = 0.8


def detect_silences(mp4_path: Path) -> list[tuple[float, float]]:
    """Return [(silence_start_s, silence_end_s), ...] from ffmpeg."""
    print(f"Running silencedetect on {mp4_path.name}...")
    proc = subprocess.run(
        [FFMPEG, "-i", str(mp4_path),
         "-af", f"silencedetect=noise={NOISE_DB}dB:d={MIN_GAP_S}",
         "-f", "null", "-"],
        capture_output=True, text=True, check=False, timeout=300,
    )
    blob = proc.stderr  # silencedetect writes to stderr
    starts = [float(m.group(1)) for m in re.finditer(r"silence_start: ([\d.]+)", blob)]
    ends   = [float(m.group(1)) for m in re.finditer(r"silence_end: ([\d.]+)", blob)]
    # Pair them up. silencedetect emits start then end for each silence.
    pairs = list(zip(starts, ends))
    print(f"  found {len(pairs)} silence regions")
    return pairs


def get_duration(mp4_path: Path) -> float:
    result = subprocess.run(
        [FFMPEG, "-i", str(mp4_path)],
        capture_output=True, text=True, check=False, timeout=30,
    )
    blob = (result.stdout or "") + (result.stderr or "")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", blob)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main() -> None:
    src = json.loads(SEGS_IN.read_text(encoding="utf-8"))
    seg_ids = [s["id"] for s in src["segments"]]
    n_segments = len(seg_ids)
    print(f"Expecting {n_segments} segments from source JSON")

    mp4_dur = get_duration(MP4)
    print(f"MP4 duration: {mp4_dur:.3f}s")

    silences = detect_silences(MP4)

    # Build segment boundaries from silence boundaries:
    #   - audio starts at 0 (or after leading silence if MP4 begins with one)
    #   - each segment is the audio BETWEEN consecutive silence boundaries
    #   - the silence between segments is the recorded silence region
    boundaries: list[tuple[float, float]] = []
    cursor = 0.0
    leading_silence = silences and silences[0][0] < 0.5
    if leading_silence:
        cursor = silences[0][1]
        silences = silences[1:]
    for sil_start, sil_end in silences:
        if sil_start - cursor > 0.05:  # ignore zero-length "segments"
            boundaries.append((cursor, sil_start))
        cursor = sil_end
    # Final segment (after last silence, if MP4 doesn't end with a silence)
    if mp4_dur - cursor > 0.05:
        boundaries.append((cursor, mp4_dur))

    print(f"Detected {len(boundaries)} spoken regions")

    # Greedy match: walk source segments + detected regions in lockstep.
    # If a source segment is longer than the next detected region, the
    # segment must have been split by an internal pause — keep merging
    # consecutive regions until the accumulated duration ≈ source duration.
    src_segs = src["segments"]
    new_segments = []
    di = 0
    for src_seg in src_segs:
        if di >= len(boundaries):
            new_segments.append({"id": src_seg["id"], "start": None, "end": None})
            continue
        src_dur = src_seg["end"] - src_seg["start"]
        start_t, end_t = boundaries[di]
        acc = end_t - start_t
        di += 1
        # Merge subsequent regions until the accumulated span covers ~85%
        # of the source segment's duration. Trust duration matching over
        # gap-size heuristics — atempo on slow segments can make internal
        # pauses indistinguishable from inter-segment gaps by size alone.
        while di < len(boundaries) and acc < src_dur * 0.85:
            next_start, next_end = boundaries[di]
            end_t = next_end
            acc = end_t - start_t
            di += 1
        new_segments.append({
            "id": src_seg["id"],
            "start": round(start_t, 3),
            "end": round(end_t, 3),
        })

    used = di
    print(f"Matched {len(new_segments)} source segments using {used}/{len(boundaries)} detected regions")
    if used != len(boundaries):
        print(f"  NOTE: {len(boundaries) - used} detected regions left over (likely tail noise)")

    # Show first few and last few for spot-checking
    for i, s in enumerate(new_segments):
        if i < 6 or i >= len(new_segments) - 5:
            dur = (s['end'] - s['start']) if s['start'] is not None else None
            dstr = f"{dur:.2f}s" if dur else "—"
            print(f"  [{i:3}] {s['id']:30}  {s['start']!s:>8} -> {s['end']!s:>8}  ({dstr})")
        elif i == 6:
            print("  ...")

    out = {
        "voice": src.get("voice"),
        "model": src.get("model"),
        "total_seconds": round(mp4_dur, 3),
        "source": "silencedetect on elena-day02-master-fs.mp4",
        "noise_db": NOISE_DB,
        "min_gap_s": MIN_GAP_S,
        "segments": new_segments,
    }
    SEGS_OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {SEGS_OUT}")


if __name__ == "__main__":
    main()
