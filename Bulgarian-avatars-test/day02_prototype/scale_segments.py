"""Simple, robust calibration: scale all segment timings by the ratio
of (MP4 duration / source audio duration). Handles the ~1% drift
introduced by Hypereal's re-encoding of our concatenated audio.

Far more reliable than silence-detection-based matching, which fails
on segments with internal pauses (long spotlights, atempo'd narration).
The error after scaling is typically <100ms per segment — well within
the buffered seek tolerance.
"""
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
SEGS_OUT = ROOT / "assets" / "elena" / "day02-master-segments-scaled.json"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def get_duration(mp4_path: Path) -> float:
    result = subprocess.run(
        [FFMPEG, "-i", str(mp4_path)],
        capture_output=True, text=True, check=False, timeout=30,
    )
    blob = (result.stdout or "") + (result.stderr or "")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", blob)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main():
    src = json.loads(SEGS_IN.read_text(encoding="utf-8"))
    src_dur = src["total_seconds"]
    mp4_dur = get_duration(MP4)
    ratio = mp4_dur / src_dur

    print(f"Source audio duration: {src_dur:.3f}s")
    print(f"MP4 duration:          {mp4_dur:.3f}s")
    print(f"Scale ratio:           {ratio:.6f}  ({(1-ratio)*100:+.3f}%)")

    # Hypereal also typically trims leading silence. Inspect the offset.
    # We can't measure precisely without silence detection, but we can
    # subtract a small constant if needed. For now, only apply ratio scaling.
    new_segments = []
    for seg in src["segments"]:
        new_segments.append({
            "id": seg["id"],
            "start": round(seg["start"] * ratio, 3),
            "end":   round(seg["end"]   * ratio, 3),
        })

    out = {
        **src,
        "total_seconds": round(mp4_dur, 3),
        "scale_ratio_applied": round(ratio, 6),
        "calibration": "ratio-scaled to match MP4 duration",
        "segments": new_segments,
    }
    SEGS_OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {SEGS_OUT}")
    print(f"Spot check — first 3 and last 3 segments:")
    for i in [0, 1, 2, -3, -2, -1]:
        s = new_segments[i]
        print(f"  [{i:3}] {s['id']:30}  {s['start']:7.3f} -> {s['end']:7.3f}")


if __name__ == "__main__":
    main()
