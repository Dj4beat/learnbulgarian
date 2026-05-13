"""Duration probe: build a long Bulgarian audio file from Day 2's
single-speaker phrases (1-31, the ones without dialogue context).

If this audio file plays correctly through Hypereal i2v, we know the
service handles at least N seconds — which determines whether one
render per day is feasible or we need to split by section.

Writes:
  ../assets/day02-long.mp3         the concatenated audio
  ../assets/day02-long-segments.json   segment timing for the test page
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

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WORK = ASSETS / "_work_long"
WORK.mkdir(parents=True, exist_ok=True)

ENV_PATH = Path(r"C:/Users/Dj4be/Desktop/Thesportsguru/.env")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

VOICE_ID = "fSxb5mPM1l5zTVVtM3Vb"  # Elena (Bulgarian native, Sofia)
MODEL = "eleven_multilingual_v2"

# Day 2 phrases 1-31 (single-speaker, suitable for Elena alone).
# Dialogue phrases 32-52 require a roster of voices — out of scope for
# this duration test.
PHRASES = [
    ("zdravey",        "Здравей",                 "Hello (informal)"),
    ("zdraveite",      "Здравейте",               "Hello (formal/group)"),
    ("dobro_utro",     "Добро утро",              "Good morning"),
    ("dobar_den",      "Добър ден",               "Good day / afternoon"),
    ("dobar_vecher",   "Добър вечер",             "Good evening"),
    ("dovizhdane",     "Довиждане",               "Goodbye"),
    ("chao",           "Чао",                     "Bye"),
    ("do_skoro",       "До скоро",                "See you soon"),
    ("leka_nosht",     "Лека нощ",                "Good night"),
    ("izvini",         "Извини",                  "Sorry (informal)"),
    ("izvinete",       "Извинете",                "Sorry / excuse me (formal)"),
    ("chakay",         "Чакай",                   "Wait (informal)"),
    ("chakayte",       "Чакайте",                 "Wait (formal)"),
    ("govori",         "Говори",                  "Speak (informal)"),
    ("govorete",       "Говорете",                "Speak (formal)"),
    ("molya",          "Моля",                    "Please / you're welcome"),
    ("blagodarya",     "Благодаря",               "Thank you"),
    ("mnogo_blag",     "Много благодаря",         "Thank you very much"),
    ("nyama_nishto",   "Няма нищо",               "It's nothing / no worries"),
    ("zapovyadayte",   "Заповядайте",             "Here you are / please come in"),
    ("nazdrave",       "Наздраве",                "Cheers / bless you"),
    ("mersi",          "Мерси",                   "Thanks (casual)"),
    ("dobre_doshli",   "Добре дошли",             "Welcome"),
    ("ne_razbiram",    "Не разбирам",             "I don't understand"),
    ("ne_govoria",     "Не говоря добре български", "I don't speak Bulgarian well"),
    ("govorite_en",    "Говорите ли английски?",  "Do you speak English?"),
    ("po_bavno",       "Моля, говорете по-бавно", "Please speak more slowly"),
    ("kak_se_kazva",   "Как се казва това?",      "What is this called?"),
    ("razbrah",        "Разбрах",                 "I understood"),
    ("ucha_bg",        "Уча български",           "I am learning Bulgarian"),
    ("povtorete",      "Моля, повторете",         "Please repeat"),
]

GAP_MS = 700
HEAD_MS = 200
TAIL_MS = 250


def load_key() -> str:
    if os.getenv("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ELEVENLABS_API_KEY not found")


def tts(api_key: str, text: str, out_path: Path) -> None:
    if out_path.exists():
        return
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    resp = requests.post(
        url,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={
            "text": text, "model_id": MODEL,
            "voice_settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.0},
        },
        timeout=120,
    )
    if resp.status_code >= 400:
        sys.exit(f"ElevenLabs TTS failed ({resp.status_code}): {resp.text[:300]}")
    out_path.write_bytes(resp.content)


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
         "-t", f"{seconds}", "-q:a", "9", "-acodec", "libmp3lame", str(out_path)],
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
        capture_output=True, check=True, timeout=180,
    )


def main() -> None:
    api_key = load_key()
    print(f"Generating {len(PHRASES)} Day-2 phrases with Elena (BG native)")

    silence_gap = WORK / f"sil_{GAP_MS}.mp3"
    silence_head = WORK / f"sil_{HEAD_MS}.mp3"
    silence_tail = WORK / f"sil_{TAIL_MS}.mp3"
    make_silence(GAP_MS, silence_gap)
    make_silence(HEAD_MS, silence_head)
    make_silence(TAIL_MS, silence_tail)

    for slot_id, bg_text, _ in PHRASES:
        clip = WORK / f"{slot_id}.mp3"
        print(f"  [{slot_id}] {bg_text}")
        tts(api_key, bg_text, clip)

    parts: list[Path] = [silence_head]
    cursor_s = HEAD_MS / 1000.0
    segments: list[dict] = []
    for i, (slot_id, bg_text, en_gloss) in enumerate(PHRASES):
        clip = WORK / f"{slot_id}.mp3"
        dur = probe_duration_s(clip)
        parts.append(clip)
        start_s = cursor_s
        end_s = cursor_s + dur
        segments.append({
            "id": slot_id, "bg": bg_text, "en": en_gloss,
            "start": round(start_s, 3), "end": round(end_s, 3),
        })
        cursor_s = end_s
        if i < len(PHRASES) - 1:
            parts.append(silence_gap)
            cursor_s += GAP_MS / 1000.0
    parts.append(silence_tail)
    cursor_s += TAIL_MS / 1000.0

    out_mp3 = ASSETS / "day02-long.mp3"
    concat_mp3s(parts, out_mp3)
    total = cursor_s
    print(f"\nWrote {out_mp3}  ({total:.2f}s total, {out_mp3.stat().st_size//1024} KB)")
    print(f"  {len(PHRASES)} phrases, avg {total/len(PHRASES):.2f}s/phrase")

    out_json = ASSETS / "day02-long-segments.json"
    out_json.write_text(json.dumps({
        "voice": "Elena (Bulgarian native, Sofia accent)",
        "model": MODEL,
        "total_seconds": round(total, 3),
        "segments": segments,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_json}")


if __name__ == "__main__":
    main()
