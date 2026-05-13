"""Build day02-prototype-v3.html — foolproof per-segment-audio version.

Key changes from v2:
  - Each .play-audio button plays its OWN MP3 file from
    audio/elena-day02/<segment_id>.mp3 — no MP4 seek, no alignment risk.
  - The old day02 audio.js <script> block (which fired browser TTS as a
    fallback) is REMOVED so it can't double-trigger.
  - All asset paths are relative to the v3 HTML's location
    (Bulgarian-avatars-test/), no Bulgarian-avatars-test/ prefix.
  - Cold-open still uses the master MP4 (single contiguous clip — only
    place where the lip-sync video is actually watched).
  - Mini-avatar shows a static Elena image during inline audio playback.

Output: Bulgarian-avatars-test/day02-prototype-v3.html
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
SOURCE_HTML = ROOT / "day02.html"
DEST_HTML = ROOT / "Bulgarian-avatars-test" / "day02-prototype-v3.html"
AUDIO_DIR = ROOT / "Bulgarian-avatars-test" / "audio" / "elena-day02"


# ---------------------------------------------------------------------------
# 1. Mapping data-text → segment_id
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    # Only collapse whitespace; PRESERVE punctuation so "Добър ден" and
    # "Добър ден!" remain distinct keys mapping to different segments.
    return re.sub(r"\s+", " ", text).strip()


RAW_MAPPING = {
    "Здравей": "p_zdravey", "Здравейте": "p_zdraveite",
    "Добро утро": "p_dobro_utro", "Добър ден": "p_dobar_den",
    "Добър вечер": "p_dobar_vecher", "Довиждане": "p_dovizhdane",
    "Чао": "p_chao", "До скоро": "p_do_skoro",
    "Лека нощ": "p_leka_nosht", "Приятен ден": "p_priyaten_den",
    "Извини": "p_izvini", "Извинете": "p_izvinete",
    "Чакай": "p_chakay", "Чакайте": "p_chakayte",
    "Говори": "p_govori", "Говорете": "p_govorete",
    "Заповядай": "p_zapovyaday", "Заповядайте": "p_zapovyadayte",
    "Моля": "p_molya", "Благодаря": "p_blagodarya",
    "Много благодаря": "p_mnogo_blag", "Няма нищо": "p_nyama_nishto",
    "Наздраве": "p_nazdrave", "Мерси": "p_mersi",
    "Добре дошли": "p_dobre_doshli",
    "Не разбирам": "p_ne_razbiram",
    "Не говоря добре български": "p_ne_govoria",
    "Говорите ли английски?": "p_govorite_en",
    "Моля, говорете по-бавно": "p_po_bavno",
    "Как се казва това?": "p_kak_se_kazva",
    "Разбрах": "p_razbrah", "Уча български": "p_ucha_bg",
    "Моля, повторете": "p_povtorete",
    # Roleplay 1
    "Добър ден!": "rp1_owner_1",
    "Добър ден. Извинете — говорите ли английски?": "rp1_you_1",
    "Малко. Нещо желаете?": "rp1_owner_2",
    "Уча български. Не говоря добре още.": "rp1_you_2",
    "Браво! Много добре! Заповядайте.": "rp1_owner_3",
    "Благодаря! Довиждане.": "rp1_you_3",
    "Довиждане! Приятен ден.": "rp1_owner_4",
    # Roleplay 2
    "Бабо, това е приятелят ми. Той учи български!": "rp2_ivan",
    "О, здравейте! Много приятно.": "rp2_baba_1",
    "Здравейте! Много приятно и за мен. Уча български — радвам се.": "rp2_you_1",
    "Браво! Харесва ли ви България?": "rp2_baba_2",
    "Да, много! Много красива страна.": "rp2_you_2",
    "Чудесно! Кафе?": "rp2_baba_3",
    "Да, моля. Благодаря много.": "rp2_you_3",
    # Roleplay 3
    "Здравей! Какво ще вземеш?": "rp3_friend_1",
    "Здравей! Едно кафе, моля.": "rp3_you_1",
    "Голямо или малко?": "rp3_friend_2",
    "Голямо, моля. Извини — говориш ли английски?": "rp3_you_2",
    "Да, малко. Учиш ли български?": "rp3_friend_3",
    "Да! Уча от два дни.": "rp3_you_3",
    "Готино! Заповядай. Приятна сутрин.": "rp3_friend_4",
}
NORMALIZED_MAPPING = {normalize(k): v for k, v in RAW_MAPPING.items()}


def attach_data_seg(html: str) -> tuple[str, int, set[str]]:
    pattern = re.compile(
        r'(<button[^>]*class="[^"]*play-audio[^"]*"[^>]*data-text=")([^"]+)("[^>]*)>'
    )
    matched = 0
    unmatched: set[str] = set()

    def repl(m):
        nonlocal matched
        text = m.group(2)
        norm = normalize(text)
        seg_id = NORMALIZED_MAPPING.get(norm)
        if not seg_id:
            unmatched.add(text)
            return m.group(0)
        # Verify the audio file actually exists
        if not (AUDIO_DIR / f"{seg_id}.mp3").exists():
            unmatched.add(f"{text} -> {seg_id} (FILE MISSING)")
            return m.group(0)
        matched += 1
        return f'{m.group(1)}{text}{m.group(3)} data-seg="{seg_id}">'

    return pattern.sub(repl, html), matched, unmatched


# ---------------------------------------------------------------------------
# 2. Elena CSS (relative paths only — no Bulgarian-avatars-test/ prefix)
# ---------------------------------------------------------------------------

ELENA_CSS = """
<style id="elena-css">
.elena-cold-open {
  background: var(--cream-dark); border-radius: 18px;
  padding: 28px 20px; margin: 24px auto 36px; max-width: 900px;
  display: grid; grid-template-columns: 1fr; gap: 18px; align-items: center;
}
@media (min-width: 600px) { .elena-cold-open { grid-template-columns: 240px 1fr; } }
.elena-cold-open .ec-avatar {
  aspect-ratio: 1 / 1; border-radius: 16px; overflow: hidden;
  background: #000; position: relative; box-shadow: 0 8px 24px rgba(0,0,0,0.18);
  cursor: pointer;
}
.elena-cold-open .ec-avatar img, .elena-cold-open .ec-avatar video {
  position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
}
.elena-cold-open .ec-avatar img.poster { transition: opacity 0.3s; }
.elena-cold-open .ec-avatar.playing img.poster { opacity: 0; }
.elena-cold-open .ec-avatar .ec-overlay {
  position: absolute; inset: 0; display: grid; place-items: center;
  background: rgba(0,0,0,0.3); transition: opacity 0.2s;
}
.elena-cold-open .ec-avatar.playing .ec-overlay { opacity: 0; pointer-events: none; }
.elena-cold-open .ec-btn {
  background: var(--gold); color: var(--navy); border-radius: 50%;
  width: 64px; height: 64px; display: grid; place-items: center;
  font-size: 26px; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
.elena-cold-open h3 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 22px; margin-bottom: 8px; color: var(--rose);
}
.elena-cold-open p { color: var(--ink); margin-bottom: 8px; }
.elena-cold-open .ec-hint { font-size: 13px; color: var(--gold); font-style: italic; margin-top: 8px; }

.elena-recap-card {
  background: var(--navy); color: var(--cream); border-radius: 16px;
  padding: 18px; margin: 24px auto 16px; max-width: 900px;
  display: flex; gap: 16px; align-items: center;
  box-shadow: 0 6px 20px rgba(26,31,78,0.18);
}
.elena-recap-card .er-thumb {
  width: 72px; height: 72px; border-radius: 50%;
  overflow: hidden; flex-shrink: 0; border: 2px solid var(--gold);
}
.elena-recap-card .er-thumb img { width: 100%; height: 100%; object-fit: cover; }
.elena-recap-card .er-text { flex: 1; }
.elena-recap-card .er-label { font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--gold-light); }
.elena-recap-card .er-title { font-family: 'Playfair Display', serif; font-size: 18px; margin: 3px 0 4px; }
.elena-recap-card .er-meta { font-size: 13px; opacity: 0.85; }
.elena-recap-card button {
  background: var(--gold); color: var(--navy); border: 0;
  border-radius: 10px; padding: 10px 16px;
  font-family: inherit; font-weight: 700; font-size: 14px;
  cursor: pointer; flex-shrink: 0;
}
.elena-recap-card button:hover { background: #f0b340; }

.elena-intro-pill {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--navy); color: var(--cream); border: 0;
  border-radius: 999px; padding: 6px 14px 6px 6px;
  font-family: inherit; font-size: 13px; cursor: pointer;
  margin-left: 12px; vertical-align: middle;
}
.elena-intro-pill img { width: 26px; height: 26px; border-radius: 50%; object-fit: cover; }
.elena-intro-pill:hover { background: var(--navy-mid); }
.elena-intro-pill.playing { background: var(--gold); color: var(--navy); }

.elena-spotlight-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--navy); color: var(--cream); border: 0;
  border-radius: 8px; padding: 8px 14px;
  font-family: inherit; font-size: 13px; cursor: pointer; margin-top: 10px;
}
.elena-spotlight-btn img { width: 22px; height: 22px; border-radius: 50%; object-fit: cover; }
.elena-spotlight-btn:hover { background: var(--navy-mid); }
.elena-spotlight-btn.playing { background: var(--gold); color: var(--navy); }

.play-audio.elena-playing { background: var(--gold) !important; color: var(--navy) !important; }

.elena-soundboard {
  background: var(--cream-dark); border-radius: 16px;
  padding: 22px; margin: 36px auto 24px; max-width: 900px;
}
.elena-soundboard .esb-head { display: flex; gap: 14px; align-items: center; margin-bottom: 16px; flex-wrap: wrap; }
.elena-soundboard .esb-avatar { width: 56px; height: 56px; border-radius: 50%; overflow: hidden; border: 2px solid var(--gold); }
.elena-soundboard .esb-avatar img { width: 100%; height: 100%; object-fit: cover; }
.elena-soundboard .esb-text { flex: 1; min-width: 0; }
.elena-soundboard h2 { margin: 0; color: var(--navy); font-family: 'Playfair Display', serif; font-size: 22px; }
.elena-soundboard .esb-sub { margin: 2px 0 0; font-size: 13px; color: var(--muted); font-style: italic; }
.elena-soundboard .esb-filters { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.elena-soundboard .esb-filter {
  background: #fff; border: 1px solid var(--border);
  border-radius: 999px; padding: 6px 14px;
  font-family: 'Source Sans 3', sans-serif; font-size: 12px;
  cursor: pointer; color: var(--muted);
}
.elena-soundboard .esb-filter.active { background: var(--navy); color: var(--cream); border-color: var(--navy); }
.elena-soundboard .esb-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; }
.elena-soundboard .esb-tile {
  background: #fff; border: 1px solid var(--border); border-radius: 10px;
  padding: 10px 12px; cursor: pointer; text-align: left;
  font-family: 'Source Sans 3', sans-serif; font-size: 14px;
}
.elena-soundboard .esb-tile .bg { color: var(--rose); font-weight: 600; }
.elena-soundboard .esb-tile .en { color: var(--muted); font-size: 12px; margin-top: 2px; }
.elena-soundboard .esb-tile:hover { border-color: var(--gold); }
.elena-soundboard .esb-tile.playing { background: var(--gold-light); border-color: var(--gold); }

.elena-outro {
  background: var(--rose); color: #fff; border-radius: 16px;
  padding: 22px; margin: 24px auto; max-width: 900px;
  display: flex; gap: 18px; align-items: center;
}
.elena-outro .eo-avatar {
  width: 72px; height: 72px; border-radius: 50%;
  overflow: hidden; flex-shrink: 0; border: 2px solid var(--gold);
}
.elena-outro .eo-avatar img { width: 100%; height: 100%; object-fit: cover; }
.elena-outro h2 { margin: 0 0 6px; font-family: 'Playfair Display', serif; font-size: 22px; color: var(--gold-light); }
.elena-outro p { margin: 0 0 10px; }
.elena-outro button {
  background: var(--gold); color: var(--navy); border: 0;
  border-radius: 10px; padding: 10px 18px;
  font-family: inherit; font-weight: 700; cursor: pointer; font-size: 14px;
}

.elena-mini {
  position: fixed; bottom: 16px; right: 16px;
  width: 180px; background: var(--navy); border-radius: 14px;
  overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  z-index: 1000; opacity: 0; transform: translateY(20px);
  transition: opacity 0.25s, transform 0.25s; pointer-events: none;
}
.elena-mini.show { opacity: 1; transform: translateY(0); pointer-events: auto; }
.elena-mini .em-img { aspect-ratio: 1 / 1; background: #000; position: relative; overflow: hidden; }
.elena-mini .em-img img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.elena-mini .em-caption {
  padding: 8px 12px; color: var(--cream); font-size: 12px;
  display: flex; align-items: center; gap: 8px;
}
.elena-mini .em-pulse {
  width: 8px; height: 8px; background: var(--gold);
  border-radius: 50%; flex-shrink: 0;
  animation: elenaPulse 1.2s infinite;
}
@keyframes elenaPulse { 0%,100% { opacity: 0.5; } 50% { opacity: 1; } }

.elena-banner {
  background: var(--gold); color: var(--navy);
  padding: 8px 16px; text-align: center;
  font-family: 'Source Sans 3', sans-serif;
  font-size: 12px; font-weight: 700; letter-spacing: 0.5px;
}
</style>
"""


# ---------------------------------------------------------------------------
# 3. Injected HTML blocks (correct relative paths!)
# ---------------------------------------------------------------------------

COLD_OPEN_BLOCK = """
<div class="elena-cold-open" id="elenaColdOpen">
  <div class="ec-avatar" id="elenaColdAvatar">
    <img class="poster" src="assets/elena/02-greetings.jpg" alt="Elena">
    <div class="ec-overlay"><div class="ec-btn">▶</div></div>
  </div>
  <div class="ec-prose">
    <h3>Hear it from Elena</h3>
    <p>Press play, or just keep scrolling — Elena will narrate the bakery story above. The text is right there; this is the audio layer.</p>
    <p class="ec-hint">Auto-plays once when you scroll past.</p>
  </div>
</div>
"""

RECAP_CARD = """
<div class="elena-recap-card">
  <div class="er-thumb"><img src="assets/elena/01-workhorse.jpg" alt="Elena"></div>
  <div class="er-text">
    <div class="er-label">Returning learner?</div>
    <div class="er-title">Elena's 90-second recap</div>
    <div class="er-meta">Eleven phrases — the ones that matter most.</div>
  </div>
  <button data-elena-action="play-recap">▶ Play recap</button>
</div>
"""


def section_intro_pill(seg_id: str) -> str:
    return (
        f'<button class="elena-intro-pill" data-elena-action="play-segment" '
        f'data-seg="{seg_id}"><img src="assets/elena/01-workhorse.jpg" alt=""> Hear Elena introduce</button>'
    )


def spotlight_btn(seg_id: str, pose: str = "05-grammar.jpg") -> str:
    return (
        f'<button class="elena-spotlight-btn" data-elena-action="play-segment" '
        f'data-seg="{seg_id}"><img src="assets/elena/{pose}" alt=""> Hear Elena explain</button>'
    )


SOUNDBOARD_BLOCK = """
<div class="elena-soundboard" id="elenaSoundboard">
  <div class="esb-head">
    <div class="esb-avatar"><img src="assets/elena/06-outro.jpg" alt="Elena"></div>
    <div class="esb-text">
      <h2>Day 2 Mega-Soundboard</h2>
      <p class="esb-sub">Every Bulgarian phrase from today. Tap to hear Elena.</p>
    </div>
  </div>
  <div class="esb-filters" id="esbFilters">
    <button class="esb-filter active" data-filter="all">All</button>
    <button class="esb-filter" data-filter="greetings">Greetings</button>
    <button class="esb-filter" data-filter="formality">Formality</button>
    <button class="esb-filter" data-filter="polite">Polite</button>
    <button class="esb-filter" data-filter="survival">Survival</button>
    <button class="esb-filter" data-filter="dialogue">Dialogue</button>
  </div>
  <div class="esb-grid" id="esbGrid"></div>
</div>

<div class="elena-outro">
  <div class="eo-avatar"><img src="assets/elena/06-outro.jpg" alt="Elena"></div>
  <div class="eo-content">
    <h2>Браво!</h2>
    <p>You've stocked up on the foundation. Tomorrow: questions — how to ask anything you need.</p>
    <button data-elena-action="play-segment" data-seg="outro">▶ Hear Elena sign off</button>
  </div>
</div>

<div class="elena-mini" id="elenaMini">
  <div class="em-img"><img id="elenaMiniImg" src="assets/elena/01-workhorse.jpg" alt="Elena"></div>
  <div class="em-caption"><span class="em-pulse"></span><span id="elenaCaption">Elena is speaking</span></div>
</div>
"""


def build_controller_js() -> str:
    return """
<script id="elena-controller">
(() => {
  const AUDIO_BASE = 'audio/elena-day02/';
  const COLD_OPEN_VIDEO = 'clips/day02/elena-day02-master-fs.mp4';

  // ----- soundboard tile data -----
  const SOUNDBOARD = [
    {id:'p_zdravey', bg:'Здравей', en:'Hello (informal)', cats:['greetings']},
    {id:'p_zdraveite', bg:'Здравейте', en:'Hello (formal)', cats:['greetings','formality']},
    {id:'p_dobro_utro', bg:'Добро утро', en:'Good morning', cats:['greetings']},
    {id:'p_dobar_den', bg:'Добър ден', en:'Good day', cats:['greetings']},
    {id:'p_dobar_vecher', bg:'Добър вечер', en:'Good evening', cats:['greetings']},
    {id:'p_dovizhdane', bg:'Довиждане', en:'Goodbye', cats:['greetings']},
    {id:'p_chao', bg:'Чао', en:'Bye (informal)', cats:['greetings']},
    {id:'p_do_skoro', bg:'До скоро', en:'See you soon', cats:['greetings']},
    {id:'p_leka_nosht', bg:'Лека нощ', en:'Good night', cats:['greetings']},
    {id:'p_priyaten_den', bg:'Приятен ден', en:'Have a nice day', cats:['greetings']},
    {id:'p_izvini', bg:'Извини', en:'Sorry (informal)', cats:['formality']},
    {id:'p_izvinete', bg:'Извинете', en:'Sorry (formal)', cats:['formality']},
    {id:'p_chakay', bg:'Чакай', en:'Wait (informal)', cats:['formality']},
    {id:'p_chakayte', bg:'Чакайте', en:'Wait (formal)', cats:['formality']},
    {id:'p_govori', bg:'Говори', en:'Speak (informal)', cats:['formality']},
    {id:'p_govorete', bg:'Говорете', en:'Speak (formal)', cats:['formality']},
    {id:'p_zapovyaday', bg:'Заповядай', en:'Here you go (inf)', cats:['formality','polite']},
    {id:'p_zapovyadayte', bg:'Заповядайте', en:'Here you go (formal)', cats:['formality','polite']},
    {id:'p_molya', bg:'Моля', en:'Please / pardon', cats:['polite']},
    {id:'p_blagodarya', bg:'Благодаря', en:'Thank you', cats:['polite']},
    {id:'p_mnogo_blag', bg:'Много благодаря', en:'Thank you very much', cats:['polite']},
    {id:'p_nyama_nishto', bg:'Няма нищо', en:"It's nothing", cats:['polite']},
    {id:'p_nazdrave', bg:'Наздраве', en:'Cheers / bless you', cats:['polite']},
    {id:'p_mersi', bg:'Мерси', en:'Thanks (casual)', cats:['polite']},
    {id:'p_dobre_doshli', bg:'Добре дошли', en:'Welcome', cats:['polite']},
    {id:'p_ne_razbiram', bg:'Не разбирам', en:"I don't understand", cats:['survival']},
    {id:'p_ne_govoria', bg:'Не говоря добре български', en:"I don't speak BG well", cats:['survival']},
    {id:'p_govorite_en', bg:'Говорите ли английски?', en:'Do you speak English?', cats:['survival']},
    {id:'p_po_bavno', bg:'Моля, говорете по-бавно', en:'Speak more slowly', cats:['survival']},
    {id:'p_kak_se_kazva', bg:'Как се казва това?', en:'What is this called?', cats:['survival']},
    {id:'p_razbrah', bg:'Разбрах', en:'Got it', cats:['survival']},
    {id:'p_ucha_bg', bg:'Уча български', en:"I'm learning Bulgarian", cats:['survival']},
    {id:'p_povtorete', bg:'Моля, повторете', en:'Please repeat', cats:['survival']},
    {id:'rp1_owner_1', bg:'Добър ден!', en:'(Shop owner)', cats:['dialogue']},
    {id:'rp1_owner_3', bg:'Браво! Много добре!', en:'(Owner) Well done!', cats:['dialogue']},
    {id:'rp2_baba_1', bg:'О, здравейте!', en:'(Grandma) Hello!', cats:['dialogue']},
    {id:'rp3_friend_1', bg:'Здравей! Какво ще вземеш?', en:'(Friend) What will you have?', cats:['dialogue']},
  ];

  const RECAP_QUEUE = ['recap_intro','recap_1','recap_2','recap_3','recap_4','recap_5',
                       'recap_6','recap_7','recap_8','recap_9','recap_10','recap_11'];

  const mini = document.getElementById('elenaMini');
  const caption = document.getElementById('elenaCaption');
  const coldAvatar = document.getElementById('elenaColdAvatar');

  // Cold-open: use the master MP4 (one contiguous lip-synced segment).
  const coldVideo = document.createElement('video');
  coldVideo.src = COLD_OPEN_VIDEO;
  coldVideo.preload = 'auto';
  coldVideo.playsInline = true;
  if (coldAvatar) coldAvatar.appendChild(coldVideo);

  // ----- Audio state machine -----
  // Two-tier stop: stopAudio() pauses current playback without clearing the
  // queue (so an in-progress queue keeps running after each segment ends).
  // stopAll() is the explicit reset — used by user-initiated stops, by
  // playSegment when called from outside, and by the cold-open path.
  let currentAudio = null;
  let currentButton = null;
  let queue = [];
  let coldOpenAutoplayed = false;
  let queueLabel = '';
  let queueButton = null;

  function clearButtonState() {
    document.querySelectorAll('.elena-playing, .elena-intro-pill.playing, .elena-spotlight-btn.playing, .esb-tile.playing, .elena-recap-card button.playing')
      .forEach(b => b.classList.remove('elena-playing', 'playing'));
  }
  function setCurrentButton(btn) {
    clearButtonState();
    currentButton = btn;
    if (!btn) return;
    if (btn.classList.contains('play-audio')) btn.classList.add('elena-playing');
    else btn.classList.add('playing');
  }
  function showMini(label) {
    if (caption) caption.textContent = label || 'Elena is speaking';
    mini.classList.add('show');
  }
  function hideMini() { mini.classList.remove('show'); }

  function stopAudio() {
    // Pauses CURRENT playback from all sources (Audio + cold-open MP4).
    // PRESERVES queue so an in-progress recap continues. Must stop the
    // cold-open video too because it has its own embedded audio track —
    // without this, scrolling to cold-open then clicking an inline button
    // produces two simultaneous audio streams.
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.src = '';
      currentAudio = null;
    }
    if (coldVideo && !coldVideo.paused) {
      coldVideo.pause();
      if (coldAvatar) coldAvatar.classList.remove('playing');
    }
  }

  function stopAll() {
    // Full reset: stop audio, clear queue, reset UI, pause cold-open.
    stopAudio();
    queue = [];
    queueLabel = '';
    queueButton = null;
    coldVideo.pause();
    if (coldAvatar) coldAvatar.classList.remove('playing');
    setCurrentButton(null);
    hideMini();
  }

  function _startSegment(segId, btn, label) {
    // Internal — actually load and start the audio. Does NOT touch queue
    // or call any public stop function, so queue progression is safe.
    const url = AUDIO_BASE + segId + '.mp3';
    const audio = new Audio(url);
    currentAudio = audio;
    setCurrentButton(btn);
    showMini(label || segId);
    audio.addEventListener('ended', () => {
      if (audio !== currentAudio) return;  // superseded
      audio.src = '';
      currentAudio = null;
      if (queue.length) {
        const next = queue.shift();
        _startSegment(next, queueButton || btn, queueLabel || label);
      } else {
        setCurrentButton(null);
        hideMini();
      }
    });
    audio.addEventListener('error', () => {
      console.error('Audio load failed for', segId, url);
      if (audio !== currentAudio) return;
      setCurrentButton(null);
      hideMini();
      currentAudio = null;
    });
    audio.play().catch(err => {
      console.warn('audio.play() rejected', err);
      if (audio !== currentAudio) return;
      currentAudio = null;  // consistency with error handler
      setCurrentButton(null);
      hideMini();
    });
  }

  function playSegment(segId, btn, label) {
    // Public — user-initiated single-clip playback. Resets queue.
    stopAudio();
    queue = [];
    queueLabel = '';
    queueButton = null;
    _startSegment(segId, btn, label);
  }

  function playQueue(ids, btn, label) {
    // Public — user-initiated sequence. Sets queue and starts first clip
    // WITHOUT calling playSegment (which would wipe the queue).
    if (!ids.length) return;
    stopAudio();
    queue = ids.slice(1);
    queueButton = btn;
    queueLabel = label;
    _startSegment(ids[0], btn, label);
  }

  // ----- click delegation -----
  // The original day02 audio.js is REMOVED in build, so no double-fire.
  // But .play-audio buttons might be clicked from anywhere; we handle
  // them and the new data-elena-action buttons in one delegate.
  document.addEventListener('click', e => {
    // (a) .play-audio buttons rewired with data-seg
    const audioBtn = e.target.closest('.play-audio[data-seg]');
    if (audioBtn) {
      e.preventDefault();
      if (currentButton === audioBtn) { stopAll(); return; }
      playSegment(audioBtn.dataset.seg, audioBtn, audioBtn.dataset.text || audioBtn.dataset.seg);
      return;
    }
    // (b) any element with data-elena-action
    const t = e.target.closest('[data-elena-action]');
    if (!t) return;
    e.preventDefault();
    const action = t.dataset.elenaAction;
    if (action === 'play-segment') {
      if (currentButton === t) { stopAll(); return; }
      const label = t.textContent.trim().slice(0, 40);
      playSegment(t.dataset.seg, t, label);
    } else if (action === 'play-recap') {
      if (currentButton === t) { stopAll(); return; }
      playQueue(RECAP_QUEUE, t, 'Day 2 recap');
    }
  });

  // Cold-open: master MP4 plays once on first scroll-into-view.
  function playColdOpen(isAutoplay) {
    stopAll();
    coldAvatar.classList.add('playing');
    showMini('Cold-open: the bakery');
    coldVideo.muted = false;
    coldVideo.currentTime = 0;
    coldVideo.onended = () => {
      coldAvatar.classList.remove('playing');
      hideMini();
    };
    coldVideo.play().catch(err => {
      // Most likely cause: browser autoplay policy blocks unmuted media
      // without user gesture. Roll back the UI so the static poster is
      // visible — user can click the avatar to start it as a gesture.
      console.warn('cold-open play() rejected', err);
      coldAvatar.classList.remove('playing');
      hideMini();
    });
  }

  if (coldAvatar) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting && !coldOpenAutoplayed) {
          coldOpenAutoplayed = true;
          playColdOpen(true);
        }
      });
    }, { threshold: 0.4 });
    obs.observe(document.getElementById('elenaColdOpen'));
    coldAvatar.addEventListener('click', () => playColdOpen(false));
  }

  // Render mega-soundboard
  const grid = document.getElementById('esbGrid');
  function renderBoard(filter) {
    if (!grid) return;
    grid.innerHTML = '';
    SOUNDBOARD
      .filter(s => filter === 'all' || s.cats.includes(filter))
      .forEach(s => {
        const tile = document.createElement('button');
        tile.className = 'esb-tile';
        tile.dataset.elenaAction = 'play-segment';
        tile.dataset.seg = s.id;
        tile.innerHTML = '<div class="bg">' + s.bg + '</div><div class="en">' + s.en + '</div>';
        grid.appendChild(tile);
      });
  }
  renderBoard('all');
  const filters = document.getElementById('esbFilters');
  if (filters) {
    filters.addEventListener('click', e => {
      const btn = e.target.closest('.esb-filter');
      if (!btn) return;
      filters.querySelectorAll('.esb-filter').forEach(b => b.classList.toggle('active', b === btn));
      renderBoard(btn.dataset.filter);
    });
  }
})();
</script>
"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

RECAP_QUEUE = [
    "recap_intro", "recap_1", "recap_2", "recap_3", "recap_4", "recap_5",
    "recap_6", "recap_7", "recap_8", "recap_9", "recap_10", "recap_11",
]
SPOTLIGHT_SEGS = [
    "spotlight_te", "spotlight_mersi", "spotlight_zapovyadayte",
    "spotlight_vie", "spotlight_dobra_vs_dobar", "spotlight_ucha_bg",
]
INTRO_SEGS = [
    "intro_s2", "intro_s3", "intro_s4", "intro_s5", "intro_s6",
    "intro_s7", "intro_s8", "intro_roleplays",
]
REQUIRED_NON_BUTTON_SEGS = [
    "cold_open", "outro", *RECAP_QUEUE, *SPOTLIGHT_SEGS, *INTRO_SEGS,
]


def verify_audio_files_exist():
    """Hard-fail the build if any audio file referenced by the page is missing."""
    missing = []
    for seg in REQUIRED_NON_BUTTON_SEGS:
        if not (AUDIO_DIR / f"{seg}.mp3").exists():
            missing.append(seg)
    if missing:
        print(f"BUILD HALT — {len(missing)} required audio files missing:")
        for m in missing:
            print(f"  audio/elena-day02/{m}.mp3")
        sys.exit(1)
    print(f"  audio dir check: all {len(REQUIRED_NON_BUTTON_SEGS)} non-button segs present")


def main() -> None:
    verify_audio_files_exist()
    html = SOURCE_HTML.read_text(encoding="utf-8")
    print(f"Source: {SOURCE_HTML.name}, {len(html)} chars")

    # --- 0. Remove the existing audio.js script block (lines 1211-1308 approx) ---
    # Anchor: starts with `<script>\n(function(){\n  var currentAudio = null;`
    audio_script_pat = re.compile(
        r'<script>\s*\(function\(\)\{\s*var currentAudio\s*=.*?\}\)\(\);\s*</script>',
        re.DOTALL
    )
    html, n = audio_script_pat.subn(
        '<!-- original audio.js removed by build_v3.py — replaced with Elena per-file audio system -->',
        html, count=1
    )
    print(f"Old audio.js removal: {'ok' if n else 'FAILED — anchor not found, may double-fire'}")

    # --- 1. Add data-seg to audio buttons ---
    html, matched, unmatched = attach_data_seg(html)
    print(f"Wired {matched} audio buttons to per-segment files")
    if unmatched:
        print("  unmapped data-text values:")
        for u in sorted(unmatched):
            print(f"    {u!r}")

    # --- 2. Inject Elena CSS after the existing </style> ---
    html, n = re.subn(r"</style>", "</style>" + ELENA_CSS, html, count=1)
    if not n:
        sys.exit("could not find </style> to inject Elena CSS")

    # --- 3. Inject the recap card after <main class="page-body"> ---
    html, n = re.subn(r'(<main class="page-body">)', lambda m: m.group(1) + RECAP_CARD, html, count=1)
    print(f"Recap card: {'ok' if n else 'MISS'}")

    # --- 4. Inject cold-open hero after the bakery story info-box ---
    pat = re.compile(
        r'(<div class="info-box blue"[^>]*>\s*<p class="info-box-title">[^<]*Your first conversation[^<]*</p>.*?</div>)',
        re.DOTALL
    )
    html, n = pat.subn(lambda m: m.group(1) + COLD_OPEN_BLOCK, html, count=1)
    print(f"Cold-open: {'ok' if n else 'MISS'}")

    # --- 5. Inject section-intro pills ---
    section_map = {
        "Section 2": "intro_s2", "Section 3": "intro_s3", "Section 4": "intro_s4",
        "Section 5": "intro_s5", "Section 6": "intro_s6", "Section 7": "intro_s7",
        "Section 8": "intro_s8",
    }
    for label, seg_id in section_map.items():
        pat = re.compile(rf'(<p class="sh-label">{re.escape(label)}</p>)')
        pill = "\n  " + section_intro_pill(seg_id)
        html, n = pat.subn(lambda m: m.group(1) + pill, html, count=1)
        print(f"  pill {label}: {'ok' if n else 'MISS'}")

    # --- 6. Inject spotlight buttons inside specific info-boxes ---
    spotlight_anchors = [
        ("⚠️ The golden rule",                 "spotlight_vie",            "04-rules.jpg"),
        ("💡 Memory tip — Здравей",            "spotlight_te",             "05-grammar.jpg"),
        ("💡 Why this matters",                "spotlight_te",             "05-grammar.jpg"),
        ("💡 Моля — the most versatile word",  "spotlight_ucha_bg",        "05-grammar.jpg"),
        ("🇧🇬 Мерси — the French connection",  "spotlight_mersi",          "03-cultural.jpg"),
        ("🏠 Bulgarian hospitality",           "spotlight_zapovyadayte",   "03-cultural.jpg"),
        ("💡 The most useful phrase",          "spotlight_ucha_bg",        "05-grammar.jpg"),
    ]
    for anchor, seg_id, pose in spotlight_anchors:
        pat = re.compile(
            rf'(<p class="info-box-title">[^<]*{re.escape(anchor)}[^<]*</p>.*?)(</div>)',
            re.DOTALL
        )
        btn = spotlight_btn(seg_id, pose)
        html, n = pat.subn(lambda m: m.group(1) + btn + m.group(2), html, count=1)
        print(f"  spotlight {anchor[:30]}: {'ok' if n else 'MISS'}")

    # --- 7. Append soundboard + outro + mini-avatar BEFORE </body> ---
    html, n = re.subn(r"(</body>)", SOUNDBOARD_BLOCK + build_controller_js() + r"\1", html, count=1)
    if not n:
        sys.exit("could not find </body> to inject Elena footer blocks")

    # --- 8. Banner so user knows this is v3 ---
    html, _ = re.subn(
        r"<body[^>]*>",
        lambda m: m.group(0) + '\n<div class="elena-banner">ELENA v3 PROTOTYPE — per-segment audio files (no MP4 seek) — all 59 audio buttons + spotlights + soundboard</div>',
        html, count=1
    )

    DEST_HTML.write_text(html, encoding="utf-8")
    print(f"\nWrote {DEST_HTML}  ({len(html)} chars)")


if __name__ == "__main__":
    main()
