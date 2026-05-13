"""Generate Elena's master audio file for the Day 2 prototype.

Single MP3 with named segments for every part of the page:
  - cold_open cinematic (English with Bulgarian words)
  - cold_recap intro + 11 phrase recaps
  - section intros (×8)
  - all 62 unique Bulgarian utterances as discrete clips
  - spotlight explanations (×6)
  - outro

Voice: Elena (Bulgarian native, ElevenLabs multilingual_v2).
English with mild Bulgarian accent = authentic teacher voice.

Writes:
  ../assets/elena/day02-master.mp3
  ../assets/elena/day02-master-segments.json

Cost: free (ElevenLabs TTS only — no Hypereal here).
"""
from __future__ import annotations
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
ASSETS = ROOT / "assets" / "elena"
WORK = ASSETS / "_work_master"
WORK.mkdir(parents=True, exist_ok=True)

ENV_PATH = Path(r"C:/Users/Dj4be/Desktop/Thesportsguru/.env")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

VOICE_ID = "fSxb5mPM1l5zTVVtM3Vb"  # Elena BG native
MODEL = "eleven_multilingual_v2"

# Pause configuration — comfortable seek margins.
NARRATION_PAUSE_MS = 600      # between narration sentences
PHRASE_PAUSE_MS = 850         # between vocab phrase clips
SECTION_PAUSE_MS = 1200       # between major sections of the master file
HEAD_MS = 250
TAIL_MS = 400

# ------------------------------------------------------------------
# THE SCRIPT
# Each entry: (segment_id, text_for_tts, pause_after_ms)
# Bulgarian text is mixed inline — ElevenLabs multilingual handles it.
# ------------------------------------------------------------------

# "slow" segments use higher stability + ffmpeg atempo=0.92 post-process.
# These are the longer English-heavy narration clips where ElevenLabs tends
# to rush — user feedback after the first pass.
SLOW_PREFIXES = ("cold_open", "recap_intro", "intro_", "spotlight_", "outro")


def is_slow(seg_id: str) -> bool:
    return any(seg_id.startswith(p) for p in SLOW_PREFIXES)


SCRIPT: list[tuple[str, str, int]] = [
    # ============ COLD-OPEN CINEMATIC (auto-plays on scroll into Section 1) ============
    ("cold_open",
     "Imagine. You walk into a Bulgarian bakery at 8 in the morning. "
     "The woman behind the counter says something warm — you catch the word "
     "Добро утро. You point at a баничка and she hands you one, still warm. "
     "You smile, say thank you in English, and leave feeling like you missed "
     "a whole conversation. By the end of today, that won't happen again.",
     SECTION_PAUSE_MS),

    # ============ 90-SEC COLD RECAP (top of page, for returning learners) ============
    ("recap_intro",
     "Returning learner? Quick recap. Eleven phrases — the ones that matter most.",
     PHRASE_PAUSE_MS),
    ("recap_1",  "Здравей. Hello, informal.", PHRASE_PAUSE_MS),
    ("recap_2",  "Здравейте. Hello, formal or to a group.", PHRASE_PAUSE_MS),
    ("recap_3",  "Добро утро. Good morning.", PHRASE_PAUSE_MS),
    ("recap_4",  "Добър ден. Good day.", PHRASE_PAUSE_MS),
    ("recap_5",  "Довиждане. Goodbye, always safe.", PHRASE_PAUSE_MS),
    ("recap_6",  "Моля. Please. Also you're welcome. Also pardon.", PHRASE_PAUSE_MS),
    ("recap_7",  "Благодаря. Thank you.", PHRASE_PAUSE_MS),
    ("recap_8",  "Извинете. Excuse me, formal.", PHRASE_PAUSE_MS),
    ("recap_9",  "Не разбирам. I don't understand.", PHRASE_PAUSE_MS),
    ("recap_10", "Говорите ли английски? Do you speak English?", PHRASE_PAUSE_MS),
    ("recap_11", "Уча български. I'm learning Bulgarian. Your magic phrase.", SECTION_PAUSE_MS),

    # ============ SECTION INTROS ============
    ("intro_s2",
     "Section two. Formal versus informal. The most important distinction in Bulgarian. "
     "Two words for 'you': ти informal, Вие formal. Get this wrong with the wrong person — instant offence.",
     SECTION_PAUSE_MS),
    ("intro_s3",
     "Section three. Three greetings, three times of day. Listen for the small word that changes between them.",
     SECTION_PAUSE_MS),
    ("intro_s4",
     "Section four. The full hello and goodbye set. Six phrases, complete coverage.",
     SECTION_PAUSE_MS),
    ("intro_s5",
     "Section five. One suffix that unlocks formality across the whole language. Watch the -те ending.",
     SECTION_PAUSE_MS),
    ("intro_s6",
     "Section six. The eight phrases you'll use most. Greetings get you in. Politeness keeps you welcome.",
     SECTION_PAUSE_MS),
    ("intro_s7",
     "Section seven. When you don't know what to say. These survival phrases buy you time and goodwill.",
     SECTION_PAUSE_MS),
    ("intro_s8",
     "Reading the room. Four scenarios. Decide: formal or informal? The factors are setting, age, and context.",
     SECTION_PAUSE_MS),
    ("intro_roleplays",
     "Three roleplays coming up. Read each line aloud before you press play. Pause if you need to. There's no rush.",
     SECTION_PAUSE_MS),

    # ============ ALL 62 BULGARIAN UTTERANCES — individual clips ============
    # These power: inline ▶ Listen buttons, the mega-soundboard, the register toggle, quiz audio.
    # Format: just the Bulgarian, no English. The page provides context.

    # Greetings & farewells
    ("p_zdravey",         "Здравей.",         PHRASE_PAUSE_MS),
    ("p_zdraveite",       "Здравейте.",       PHRASE_PAUSE_MS),
    ("p_dobro_utro",      "Добро утро.",      PHRASE_PAUSE_MS),
    ("p_dobar_den",       "Добър ден.",       PHRASE_PAUSE_MS),
    ("p_dobar_vecher",    "Добър вечер.",     PHRASE_PAUSE_MS),
    ("p_dovizhdane",      "Довиждане.",       PHRASE_PAUSE_MS),
    ("p_chao",            "Чао.",             PHRASE_PAUSE_MS),
    ("p_do_skoro",        "До скоро.",        PHRASE_PAUSE_MS),
    ("p_leka_nosht",      "Лека нощ.",        PHRASE_PAUSE_MS),
    ("p_priyaten_den",    "Приятен ден.",     PHRASE_PAUSE_MS),
    # -те pairs
    ("p_izvini",          "Извини.",          PHRASE_PAUSE_MS),
    ("p_izvinete",        "Извинете.",        PHRASE_PAUSE_MS),
    ("p_chakay",          "Чакай.",           PHRASE_PAUSE_MS),
    ("p_chakayte",        "Чакайте.",         PHRASE_PAUSE_MS),
    ("p_govori",          "Говори.",          PHRASE_PAUSE_MS),
    ("p_govorete",        "Говорете.",        PHRASE_PAUSE_MS),
    ("p_zapovyaday",      "Заповядай.",       PHRASE_PAUSE_MS),
    ("p_zapovyadayte",    "Заповядайте.",     PHRASE_PAUSE_MS),
    # Polite phrases
    ("p_molya",           "Моля.",            PHRASE_PAUSE_MS),
    ("p_blagodarya",      "Благодаря.",       PHRASE_PAUSE_MS),
    ("p_mnogo_blag",      "Много благодаря.", PHRASE_PAUSE_MS),
    ("p_nyama_nishto",    "Няма нищо.",       PHRASE_PAUSE_MS),
    ("p_nazdrave",        "Наздраве.",        PHRASE_PAUSE_MS),
    ("p_mersi",           "Мерси.",           PHRASE_PAUSE_MS),
    ("p_dobre_doshli",    "Добре дошли.",     PHRASE_PAUSE_MS),
    ("p_s_udovolstvie",   "Благодаря, с удоволствие.", PHRASE_PAUSE_MS),
    ("p_dostatachno",     "Благодаря, достатъчно.",    PHRASE_PAUSE_MS),
    # Survival
    ("p_ne_razbiram",     "Не разбирам.",     PHRASE_PAUSE_MS),
    ("p_ne_govoria",      "Не говоря добре български.", PHRASE_PAUSE_MS),
    ("p_govorite_en",     "Говорите ли английски?", PHRASE_PAUSE_MS),
    ("p_po_bavno",        "Моля, говорете по-бавно.", PHRASE_PAUSE_MS),
    ("p_kak_se_kazva",    "Как се казва това?", PHRASE_PAUSE_MS),
    ("p_razbrah",         "Разбрах.",         PHRASE_PAUSE_MS),
    ("p_ucha_bg",         "Уча български.",   PHRASE_PAUSE_MS),
    ("p_povtorete",       "Моля, повторете.", PHRASE_PAUSE_MS),
    ("p_mozhem_na_ti",    "Можем на ти.",     PHRASE_PAUSE_MS),
    # Cultural words referenced inline
    ("p_utro",            "Утро.",            PHRASE_PAUSE_MS),
    ("p_banichka",        "Баничка.",         PHRASE_PAUSE_MS),
    ("p_zdrave",          "Здраве.",          PHRASE_PAUSE_MS),
    ("p_dobro",           "Добро.",           PHRASE_PAUSE_MS),
    ("p_dobar",           "Добър.",           PHRASE_PAUSE_MS),
    ("p_dobra_vecher",    "Добра вечер.",     PHRASE_PAUSE_MS),
    # Roleplay 1 lines (shop)
    ("rp1_owner_1",       "Добър ден!",       PHRASE_PAUSE_MS),
    ("rp1_you_1",         "Добър ден. Извинете — говорите ли английски?", PHRASE_PAUSE_MS),
    ("rp1_owner_2",       "Малко. Нещо желаете?", PHRASE_PAUSE_MS),
    ("rp1_you_2",         "Уча български. Не говоря добре още.", PHRASE_PAUSE_MS),
    ("rp1_owner_3",       "Браво! Много добре! Заповядайте.", PHRASE_PAUSE_MS),
    ("rp1_you_3",         "Благодаря! Довиждане.", PHRASE_PAUSE_MS),
    ("rp1_owner_4",       "Довиждане! Приятен ден.", PHRASE_PAUSE_MS),
    # Roleplay 2 lines (Babà — note: voiced by Elena here as the soundboard reference, the actual roleplay page would use Babà avatar)
    ("rp2_ivan",          "Бабо, това е приятелят ми. Той учи български!", PHRASE_PAUSE_MS),
    ("rp2_baba_1",        "О, здравейте! Много приятно.", PHRASE_PAUSE_MS),
    ("rp2_you_1",         "Здравейте! Много приятно и за мен. Уча български — радвам се.", PHRASE_PAUSE_MS),
    ("rp2_baba_2",        "Браво! Харесва ли ви България?", PHRASE_PAUSE_MS),
    ("rp2_you_2",         "Да, много! Много красива страна.", PHRASE_PAUSE_MS),
    ("rp2_baba_3",        "Чудесно! Кафе?",   PHRASE_PAUSE_MS),
    ("rp2_you_3",         "Да, моля. Благодаря много.", PHRASE_PAUSE_MS),
    # Roleplay 3 lines (café — informal)
    ("rp3_friend_1",      "Здравей! Какво ще вземеш?", PHRASE_PAUSE_MS),
    ("rp3_you_1",         "Здравей! Едно кафе, моля.", PHRASE_PAUSE_MS),
    ("rp3_friend_2",      "Голямо или малко?", PHRASE_PAUSE_MS),
    ("rp3_you_2",         "Голямо, моля. Извини — говориш ли английски?", PHRASE_PAUSE_MS),
    ("rp3_friend_3",      "Да, малко. Учиш ли български?", PHRASE_PAUSE_MS),
    ("rp3_you_3",         "Да! Уча от два дни.", PHRASE_PAUSE_MS),
    ("rp3_friend_4",      "Готино! Заповядай. Приятна сутрин.", SECTION_PAUSE_MS),

    # ============ SPOTLIGHT EXPLANATIONS (mini lectures) ============
    ("spotlight_te",
     "Spotlight: the -те ending. This is your formality switch — one suffix that works "
     "across most of Bulgarian. Здравей becomes Здравейте. Извини becomes Извинете. "
     "Чакай becomes Чакайте. Same word, formal version. Learn the informal once, the formal is free.",
     SECTION_PAUSE_MS),
    ("spotlight_mersi",
     "Spotlight: Мерси. You'll hear this constantly in Bulgaria, especially in cafés and shops. "
     "It's borrowed from French, from the 19th century when French was the language of the Bulgarian elite. "
     "Today, Мерси is the casual cousin of Благодаря — both work, Мерси is just more relaxed.",
     SECTION_PAUSE_MS),
    ("spotlight_zapovyadayte",
     "Spotlight: Заповядайте. This word is everywhere in Bulgarian hospitality. "
     "Sit down — Заповядайте. Try this food — Заповядайте. Come in — Заповядайте. "
     "Refusing food in a Bulgarian home can feel impolite. The safe response: "
     "Благодаря, с удоволствие. Thank you, with pleasure.",
     SECTION_PAUSE_MS),
    ("spotlight_vie",
     "Spotlight: the golden rule. When in doubt, use Вие. Bulgarians switch to ти themselves "
     "when they're comfortable with you. Jumping to ти without invitation is the most common — "
     "and noticeable — mistake a foreigner makes. Wait to be invited.",
     SECTION_PAUSE_MS),
    ("spotlight_dobra_vs_dobar",
     "Spotlight: Добра versus Добър. You'll sometimes see Добра вечер instead of Добър вечер. "
     "Both work, but Добър is the standard. Вечер is technically feminine, which is why Добра appears — "
     "but Добър has won by usage. Use Добър and you'll always be right.",
     SECTION_PAUSE_MS),
    ("spotlight_ucha_bg",
     "Spotlight: Уча български — three words that change everything. Say this early in any "
     "Bulgarian interaction where you're struggling. The response is almost always warmth, patience, "
     "and slower speech. It's the single most useful sentence in this lesson.",
     SECTION_PAUSE_MS),

    # ============ OUTRO ============
    ("outro",
     "Браво. You've learned about twenty new phrases — the foundation of every Bulgarian interaction. "
     "Tomorrow: questions. How to ask anything you need. Until then — Лека нощ. Приятен ден. Довиждане.",
     0),
]


# ------------------------------------------------------------------
# Pipeline
# ------------------------------------------------------------------

def load_key() -> str:
    if os.getenv("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ELEVENLABS_API_KEY not found")


def tts(api_key: str, text: str, out_path: Path, slow: bool = False) -> None:
    if out_path.exists():
        return
    # Slow segments: higher stability (less expression variance, more deliberate),
    # lower style (less prosodic drift). Combined with atempo=0.92 post-process
    # in the silence-build step, this fixes the "rushed" English narration the
    # first pass produced.
    if slow:
        settings = {"stability": 0.78, "similarity_boost": 0.75, "style": 0.05}
    else:
        settings = {"stability": 0.6, "similarity_boost": 0.75, "style": 0.15}
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    resp = requests.post(
        url,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={"text": text, "model_id": MODEL, "voice_settings": settings},
        timeout=180,
    )
    if resp.status_code >= 400:
        sys.exit(f"ElevenLabs TTS failed ({resp.status_code}): {resp.text[:300]}")
    out_path.write_bytes(resp.content)


def slow_down(src: Path, dest: Path, factor: float = 0.92) -> None:
    """Slow audio by 8% without changing pitch. Idempotent."""
    if dest.exists():
        return
    subprocess.run(
        [FFMPEG, "-y", "-i", str(src), "-af", f"atempo={factor}",
         "-acodec", "libmp3lame", "-b:a", "128k", str(dest)],
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
        capture_output=True, check=True, timeout=300,
    )


def main() -> None:
    api_key = load_key()
    print(f"Generating {len(SCRIPT)} segments for Elena's master audio")

    # Pre-build silences we'll need
    silences: dict[int, Path] = {}
    for _, _, pause_ms in SCRIPT:
        if pause_ms and pause_ms not in silences:
            sp = WORK / f"sil_{pause_ms}.mp3"
            make_silence(pause_ms, sp)
            silences[pause_ms] = sp
    head_sil = WORK / f"sil_{HEAD_MS}.mp3"
    tail_sil = WORK / f"sil_{TAIL_MS}.mp3"
    make_silence(HEAD_MS, head_sil)
    make_silence(TAIL_MS, tail_sil)

    # Generate each TTS clip (idempotent — re-runs only fetch missing files).
    # Slow segments get the slower voice_settings AND a post-process atempo.
    for seg_id, text, _ in SCRIPT:
        slow = is_slow(seg_id)
        raw_path = WORK / f"{seg_id}.mp3"
        if not raw_path.exists():
            print(f"  TTS [{seg_id}]{' (slow)' if slow else ''}  {text[:55]}...")
            tts(api_key, text, raw_path, slow=slow)
        if slow:
            slowed = WORK / f"{seg_id}_slow.mp3"
            slow_down(raw_path, slowed, factor=0.92)

    # Build the concatenated timeline and record segment timings.
    # For slow segments, use the slowed file instead of the raw TTS output.
    parts: list[Path] = [head_sil]
    cursor_s = HEAD_MS / 1000.0
    segments: list[dict] = []
    for seg_id, text, pause_ms in SCRIPT:
        if is_slow(seg_id):
            clip = WORK / f"{seg_id}_slow.mp3"
        else:
            clip = WORK / f"{seg_id}.mp3"
        dur = probe_duration_s(clip)
        parts.append(clip)
        start_s = cursor_s
        end_s = cursor_s + dur
        segments.append({
            "id": seg_id,
            "start": round(start_s, 3),
            "end": round(end_s, 3),
        })
        cursor_s = end_s
        if pause_ms:
            parts.append(silences[pause_ms])
            cursor_s += pause_ms / 1000.0
    parts.append(tail_sil)
    cursor_s += TAIL_MS / 1000.0

    out_mp3 = ASSETS / "day02-master.mp3"
    concat_mp3s(parts, out_mp3)
    print(f"\nWrote {out_mp3}")
    print(f"  total: {cursor_s:.2f}s ({cursor_s/60:.2f} min)")
    print(f"  size:  {out_mp3.stat().st_size//1024} KB")
    print(f"  segments: {len(segments)}")

    out_json = ASSETS / "day02-master-segments.json"
    out_json.write_text(json.dumps({
        "voice": "Elena (Bulgarian native, Sofia accent)",
        "model": MODEL,
        "total_seconds": round(cursor_s, 3),
        "segments": segments,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_json}")


if __name__ == "__main__":
    main()
