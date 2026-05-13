"""Regenerate the 17 missing 'slow' segment TTS clips.

These exist embedded in the master MP3/MP4 but not as individual files.
With ElevenLabs quota restored we can re-fetch them as discrete clips
for the per-segment-file v3 architecture.
"""
from __future__ import annotations
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
WORK = ROOT / "assets" / "elena" / "_work_master"
ENV = Path(r"C:/Users/Dj4be/Desktop/Thesportsguru/.env")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

VOICE_ID = "fSxb5mPM1l5zTVVtM3Vb"
MODEL = "eleven_multilingual_v2"

# Verbatim copies of the slow-segment scripts from build_master_audio.py.
SLOW_SCRIPTS = [
    ("cold_open",
     "Imagine. You walk into a Bulgarian bakery at 8 in the morning. "
     "The woman behind the counter says something warm — you catch the word "
     "Добро утро. You point at a баничка and she hands you one, still warm. "
     "You smile, say thank you in English, and leave feeling like you missed "
     "a whole conversation. By the end of today, that won't happen again."),
    ("recap_intro",
     "Returning learner? Quick recap. Eleven phrases — the ones that matter most."),
    ("intro_s2",
     "Section two. Formal versus informal. The most important distinction in Bulgarian. "
     "Two words for 'you': ти informal, Вие formal. Get this wrong with the wrong person — instant offence."),
    ("intro_s3",
     "Section three. Three greetings, three times of day. Listen for the small word that changes between them."),
    ("intro_s4",
     "Section four. The full hello and goodbye set. Six phrases, complete coverage."),
    ("intro_s5",
     "Section five. One suffix that unlocks formality across the whole language. Watch the -те ending."),
    ("intro_s6",
     "Section six. The eight phrases you'll use most. Greetings get you in. Politeness keeps you welcome."),
    ("intro_s7",
     "Section seven. When you don't know what to say. These survival phrases buy you time and goodwill."),
    ("intro_s8",
     "Reading the room. Four scenarios. Decide: formal or informal? The factors are setting, age, and context."),
    ("intro_roleplays",
     "Three roleplays coming up. Read each line aloud before you press play. Pause if you need to. There's no rush."),
    ("spotlight_te",
     "Spotlight: the -те ending. This is your formality switch — one suffix that works "
     "across most of Bulgarian. Здравей becomes Здравейте. Извини becomes Извинете. "
     "Чакай becomes Чакайте. Same word, formal version. Learn the informal once, the formal is free."),
    ("spotlight_mersi",
     "Spotlight: Мерси. You'll hear this constantly in Bulgaria, especially in cafés and shops. "
     "It's borrowed from French, from the 19th century when French was the language of the Bulgarian elite. "
     "Today, Мерси is the casual cousin of Благодаря — both work, Мерси is just more relaxed."),
    ("spotlight_zapovyadayte",
     "Spotlight: Заповядайте. This word is everywhere in Bulgarian hospitality. "
     "Sit down — Заповядайте. Try this food — Заповядайте. Come in — Заповядайте. "
     "Refusing food in a Bulgarian home can feel impolite. The safe response: "
     "Благодаря, с удоволствие. Thank you, with pleasure."),
    ("spotlight_vie",
     "Spotlight: the golden rule. When in doubt, use Вие. Bulgarians switch to ти themselves "
     "when they're comfortable with you. Jumping to ти without invitation is the most common — "
     "and noticeable — mistake a foreigner makes. Wait to be invited."),
    ("spotlight_dobra_vs_dobar",
     "Spotlight: Добра versus Добър. You'll sometimes see Добра вечер instead of Добър вечер. "
     "Both work, but Добър is the standard. Вечер is technically feminine, which is why Добра appears — "
     "but Добър has won by usage. Use Добър and you'll always be right."),
    ("spotlight_ucha_bg",
     "Spotlight: Уча български — three words that change everything. Say this early in any "
     "Bulgarian interaction where you're struggling. The response is almost always warmth, patience, "
     "and slower speech. It's the single most useful sentence in this lesson."),
    ("outro",
     "Браво. You've learned about twenty new phrases — the foundation of every Bulgarian interaction. "
     "Tomorrow: questions. How to ask anything you need. Until then — Лека нощ. Приятен ден. Довиждане."),
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
    total_chars = sum(len(t) for _, t in SLOW_SCRIPTS)
    print(f"Regenerating {len(SLOW_SCRIPTS)} slow segments ({total_chars} chars)")
    for sid, text in SLOW_SCRIPTS:
        raw = WORK / f"{sid}.mp3"
        slowed = WORK / f"{sid}_slow.mp3"
        if slowed.exists():
            print(f"  [{sid}] already cached, skipping")
            continue
        if not raw.exists():
            print(f"  [{sid}] TTS ({len(text)} chars)")
            tts(api_key, text, raw)
        else:
            print(f"  [{sid}] raw cached, applying atempo")
        slow_down(raw, slowed, 0.92)
        print(f"    -> {slowed.name} ({slowed.stat().st_size//1024} KB)")
    print("\nAll 17 slow segments now exist as individual files.")


if __name__ == "__main__":
    main()
