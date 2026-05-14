"""Generate two additional/fixed spotlight clips:
  - spotlight_molya:        NEW — explains Моля's three uses (was missing)
  - spotlight_ucha_bg_v2:   FIXED — same content but "two words" not "three words"

Both use Elena voice with the slow-segment voice settings and an
atempo=0.92 post-process so they match the pacing of existing spotlights.
"""
from __future__ import annotations
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import requests
import imageio_ffmpeg

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "assets" / "elena" / "_work_master"
AUDIO_OUT = ROOT / "audio" / "elena-day02"
ENV = Path(r"C:/Users/Dj4be/Desktop/Thesportsguru/.env")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICE_ID = "fSxb5mPM1l5zTVVtM3Vb"
MODEL = "eleven_multilingual_v2"

SCRIPTS = [
    ("spotlight_molya",
     "Spotlight: Моля — the most versatile word in Bulgarian. "
     "Three jobs, one word. As a request: кафе, моля — a coffee, please. "
     "As a reply to thanks: моля means you're welcome. "
     "As a question, on its own: моля? — pardon? could you repeat that? "
     "Memorise all three from the start. You will use Моля dozens of times every day."),
    ("spotlight_ucha_bg",
     "Spotlight: Уча български — two words that change every interaction. "
     "Say this early in any Bulgarian conversation where you are struggling. "
     "The response is almost always warmth, patience, and slower speech. "
     "It is the single most useful sentence you will learn this week."),
]


def load_key() -> str:
    if os.getenv("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ELEVENLABS_API_KEY not found")


def tts(api_key: str, text: str, out_path: Path) -> None:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    resp = requests.post(
        url,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={"text": text, "model_id": MODEL,
              "voice_settings": {"stability": 0.78, "similarity_boost": 0.75, "style": 0.05}},
        timeout=180,
    )
    if resp.status_code >= 400:
        sys.exit(f"ElevenLabs TTS failed ({resp.status_code}): {resp.text[:300]}")
    out_path.write_bytes(resp.content)


def slow_down(src: Path, dest: Path, factor: float = 0.92) -> None:
    subprocess.run(
        [FFMPEG, "-y", "-i", str(src), "-af", f"atempo={factor}",
         "-acodec", "libmp3lame", "-b:a", "128k", str(dest)],
        capture_output=True, check=True, timeout=60,
    )


def main():
    api_key = load_key()
    for sid, text in SCRIPTS:
        raw = WORK / f"{sid}.mp3"
        slowed = WORK / f"{sid}_slow.mp3"
        if raw.exists():
            raw.unlink()  # force regen
        if slowed.exists():
            slowed.unlink()
        print(f"  [{sid}] TTS ({len(text)} chars)")
        tts(api_key, text, raw)
        slow_down(raw, slowed, 0.92)
        dest = AUDIO_OUT / f"{sid}.mp3"
        shutil.copy2(slowed, dest)
        print(f"    -> {dest.relative_to(ROOT)} ({dest.stat().st_size//1024} KB)")
    print("Done.")


if __name__ == "__main__":
    main()
