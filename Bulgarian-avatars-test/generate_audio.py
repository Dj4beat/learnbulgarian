"""Generate concatenated Bulgarian audio for the Day 2 avatar test.

Four phrases, each spoken in Bulgarian, concatenated with timed silence
gaps so the single resulting MP3 can be sliced clientside via <video>
currentTime jumps. Uses imageio-ffmpeg directly (no pydub — Py 3.13
removed audioop and pydub's compat layer is shaky).

Writes:
  assets/day02-greetings.mp3   — the audio Hypereal will animate
  assets/day02-segments.json   — {phrase_id: [start_s, end_s]} for the UI

Voice: Alice (Xb7hH8MSUJpSbSDYk0k2) — branded "Clear, Engaging Educator".
Model: eleven_multilingual_v2 (only model that handles Bulgarian).
"""
from __future__ import annotations
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import requests
import imageio_ffmpeg

# Windows cp1252 stdout can't render Cyrillic.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
WORK = ASSETS / "_work"
WORK.mkdir(exist_ok=True)

ENV_PATH = Path(r"C:/Users/Dj4be/Desktop/Thesportsguru/.env")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

PHRASES = [
    ("zdraveite",  "Здравейте",   "Hello"),
    ("dobro_utro", "Добро утро",  "Good morning"),
    ("dobar_den",  "Добър ден",   "Good day"),
    ("dovizhdane", "Довиждане",   "Goodbye"),
]

VOICE_ID = "fSxb5mPM1l5zTVVtM3Vb"  # Elena — native Bulgarian female, Sofia accent
VOICE_LABEL = "Elena (Bulgarian native, Sofia accent)"
MODEL = "eleven_multilingual_v2"

GAP_MS = 900    # silent gap between phrases
HEAD_MS = 250   # pre-roll
TAIL_MS = 250   # post-roll


def load_key() -> str:
    if os.getenv("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ELEVENLABS_API_KEY not found")


def tts(api_key: str, text: str, out_path: Path) -> None:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    resp = requests.post(
        url,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={
            "text": text,
            "model_id": MODEL,
            "voice_settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.0},
        },
        timeout=120,
    )
    if resp.status_code >= 400:
        sys.exit(f"ElevenLabs TTS failed ({resp.status_code}): {resp.text[:300]}")
    out_path.write_bytes(resp.content)


def probe_duration_s(path: Path) -> float:
    """Use ffmpeg -i to read duration from stderr (we don't have ffprobe)."""
    result = subprocess.run(
        [FFMPEG, "-i", str(path)],
        capture_output=True, text=True, check=False, timeout=30,
    )
    blob = (result.stdout or "") + (result.stderr or "")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", blob)
    if not m:
        sys.exit(f"could not read duration from {path}")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def make_silence(duration_ms: int, out_path: Path) -> None:
    """Generate a silent mp3 of given duration."""
    if out_path.exists():
        return
    seconds = duration_ms / 1000.0
    subprocess.run(
        [FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
         "-t", f"{seconds}", "-q:a", "9", "-acodec", "libmp3lame", str(out_path)],
        capture_output=True, check=True, timeout=30,
    )


def concat_mp3s(parts: list[Path], out_path: Path) -> None:
    """Concat using ffmpeg concat demuxer. All parts must share codec params."""
    list_file = WORK / "_concat.txt"
    list_file.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in parts),
        encoding="utf-8",
    )
    # Re-encode + loudness-normalise. ElevenLabs output is conservative
    # (~ -23 LUFS); -14 LUFS matches YouTube/Spotify and feels properly loud
    # without clipping. TP=-1.5 leaves headroom for the lossy mp3 re-encode.
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-af", "loudnorm=I=-14:LRA=11:TP=-1.5",
         "-ar", "44100", "-ac", "1", "-acodec", "libmp3lame", "-b:a", "128k",
         str(out_path)],
        capture_output=True, check=True, timeout=120,
    )


def main() -> None:
    api_key = load_key()
    print(f"Generating {len(PHRASES)} Bulgarian clips with {VOICE_LABEL}")

    silence_gap = WORK / f"sil_{GAP_MS}.mp3"
    silence_head = WORK / f"sil_{HEAD_MS}.mp3"
    silence_tail = WORK / f"sil_{TAIL_MS}.mp3"
    make_silence(GAP_MS, silence_gap)
    make_silence(HEAD_MS, silence_head)
    make_silence(TAIL_MS, silence_tail)

    clip_paths: dict[str, Path] = {}
    for slot_id, bg_text, _ in PHRASES:
        clip_path = WORK / f"{slot_id}.mp3"
        print(f"  [{slot_id}] {bg_text}")
        tts(api_key, bg_text, clip_path)
        clip_paths[slot_id] = clip_path

    parts: list[Path] = [silence_head]
    cursor_s = HEAD_MS / 1000.0
    segments: list[dict] = []
    for i, (slot_id, bg_text, en_gloss) in enumerate(PHRASES):
        clip = clip_paths[slot_id]
        dur = probe_duration_s(clip)
        parts.append(clip)
        start_s = cursor_s
        end_s = cursor_s + dur
        segments.append({
            "id": slot_id, "bg": bg_text, "en": en_gloss,
            "start": round(start_s, 3), "end": round(end_s, 3),
        })
        cursor_s = end_s
        print(f"    -> {start_s:.2f}s — {end_s:.2f}s  ({dur:.2f}s clip)")
        if i < len(PHRASES) - 1:
            parts.append(silence_gap)
            cursor_s += GAP_MS / 1000.0
    parts.append(silence_tail)
    cursor_s += TAIL_MS / 1000.0

    out_mp3 = ASSETS / "day02-greetings.mp3"
    concat_mp3s(parts, out_mp3)
    print(f"\nWrote {out_mp3}  ({cursor_s:.2f}s total, {out_mp3.stat().st_size//1024} KB)")

    out_json = ASSETS / "day02-segments.json"
    out_json.write_text(json.dumps({
        "voice": VOICE_LABEL,
        "model": MODEL,
        "total_seconds": round(cursor_s, 3),
        "segments": segments,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_json}")


if __name__ == "__main__":
    main()
