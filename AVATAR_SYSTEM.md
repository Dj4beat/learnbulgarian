# Avatar System — handover document

Last updated: 2026-05-14

This is the authoritative reference for the AI-avatar narration system being added to the Bulgarian 60-day course. Standalone from `PROJECT_STATUS.md` — that doc tracks the per-day content upgrade workflow; this one tracks the avatar layer being added across all days.

---

## TL;DR

We are adding lip-synced AI-avatar video narration to every page of the course. The avatar system **complements** existing content — it doesn't replace any of the prose, tables, or audio buttons currently on the pages. Visual learners get a teacher; auditory learners get higher-quality consistent audio; reading learners are unaffected.

**Status at end-of-day 2026-05-14:** Day 2 prototype rendered and built. Tier-1 features wired up end-to-end. Awaiting QA + iteration in the next session.

**Branch:** `claude/blissful-bouman-36288c` (worktree at `.claude/worktrees/blissful-bouman-36288c/`)

---

## First task next session

**Walk through the amendments / observations one-by-one.** The user has feedback from QA that must be captured systematically:
- Each amendment should be documented (what changed, why, what we learned).
- Significant feature changes should be flagged here so future-us has the full picture.
- Don't batch — go through each item with the user, confirm, document, then implement.

Open this file at the bottom (the "Amendments Log") and start filling it in.

---

## The roster

| Character | Voice (ElevenLabs) | Voice ID | Status | Role |
|---|---|---|---|---|
| **Elena** | "Elena - Energetic, Friendly, and Clear" (BG native, Sofia) | `fSxb5mPM1l5zTVVtM3Vb` | ✅ Voice added, audio generated, MP4 rendered | Primary teacher · narration · most vocab |
| **Ivan** (= Georgi voice) | "Georgi - Tender, Rich, and Reassuring" (BG native young male) | `31jwlwrRwpOA5yGuVAby` | ⏳ Voice chosen, not yet added to library or rendered | Male peer in dialogues · café barista · friend |
| **Babà** | TBD — search needed | — | ⏳ Not chosen | Elder female · grandmother scenes · "Вие via age" lessons |

**Why three:** Day 2 alone has multi-speaker dialogues that require a male voice (Ivan's introduction line in Roleplay 2) and an elder female voice (Баба Мария in Roleplay 2). Confirmed by an agent-driven full-course audit on 2026-05-13.

**Voice library reference:**
- ElevenLabs > Voice Library > filter `language=bg` returns ~30 native Bulgarian voices.
- Other strong female candidates if we re-pick: Milena (`M1ydWt7KnBCiuv4CnEDC`), Moonglow (`vnewfQdVVk9Y9DZWVRNm`), Alexandra (`pREMn4INXSs2KOPsNcsD`).
- Other strong male candidates if we re-pick Ivan: Yordan (`vZifugoCmJjNgn0bBdKH`), Peter K (`406EiNlYvqFqcz3vsnOm`), Kosta (`gdk0ZsvfAOobfbTtnx6p`).

---

## Elena's pose library

Six portrait variants of the same model (color, head-and-shoulders, mouth closed, eyes-to-camera). All 1024×1536 originals at `Bulgarian-avatars-test/Elana/` (Pexels-licensed equivalent; user-provided AI-consistent set). Cropped to 720×720 squares at `Bulgarian-avatars-test/assets/elena/`:

| File | Vibe | Use |
|---|---|---|
| `01-workhorse.jpg` | Black top, neutral, closed-mouth smile | Default narration · vocab library · ~70% of renders |
| `02-greetings.jpg` | Soft lavender, warm smile | Greetings · intros · section openers |
| `03-cultural.jpg` | Emerald formal | "In Bulgarian culture..." cultural notes |
| `04-rules.jpg` | Black asymmetric, slightly serious | Warnings · formality rule · "do not switch ти without invitation" |
| `05-grammar.jpg` | Burgundy, contemplative | Grammar · -те explanation · concept-heavy spotlights |
| `06-outro.jpg` | White/cream, soft | Outros · encouragement · "see you tomorrow" |

**i2v constraint:** poses must have closed mouth, eyes-to-camera, plain background. Hypereal animates only the mouth/face area. Sourcing more poses of "the same model" via Pexels is hard; AI generation is the realistic path if we need more.

There is also an original B&W Pexels portrait at `assets/elena.jpg` / `elena-square.jpg` from the first 4-phrase test — superseded by the color set but still referenced from the earlier `day02-avatars.html` test page.

---

## Architecture — how renders are structured

### The single most important finding

**Hypereal pricing is flat-rate per job, not per second.** All four probes we ran today (7s, 57s, 169s, 562s/9:22) cost the same 23 credits = **$0.23**. This unlocks "render long once, slice for delivery" as the optimal pattern.

### Render strategy across the 60-day course

Three buckets, all sourced into separate MP4s per character:

1. **Shared "vocab library" mega-MP4 per character** (rendered once each) — covers the ~200-300 high-frequency phrases that recur across the course. Every day's page references it via time-marks. Browser-cached after first load.
2. **Per-day narration MP4** (rendered once per day per active character) — the unique cinematics, section intros, spotlight explanations, recap, outro for that day.
3. **Per-scene dialogue MP4s** (rendered as needed for specific roleplays) — multi-character scenes where each character speaks their own lines on their own MP4.

### Slicing for mobile delivery

We've proven Hypereal accepts at least 562 seconds (9:22) in one render. Output for 9:22 ≈ 40 MB. **Mobile-delivery sweet spot is ~2-3 minute MP4s (~15-20 MB each).** Approach: render long, then post-process with `ffmpeg -ss/-t` to slice the master into delivery-sized chunks if size matters. Modern `<video>` supports HTTP range requests so seeking inside a single big file is also viable on hosted environments.

### Cost projection

| Strategy | Renders | Cost (USD) |
|---|---|---|
| One MP4 per phrase | 1,500-1,800 | $345-$415 |
| One MP4 per section | ~180-240 | $42-$55 |
| **One MP4 per character per day + shared vocab libraries** | **~100-150** | **$23-$35** |

The rightmost row is the target. Cap test pushed to 562s succeeded; further probes not needed.

---

## Hypereal account state (end of day)

- **Credits remaining:** 424 (≈$4.24)
- **Credits spent today:** 4 renders × 23 = 92 credits ($0.92)
- **Pricing:** 100 credits = $1 USD, pay-as-you-go, credits never expire.
- **Tier:** auto-unlocks rate-limit tiers as cumulative spend grows; daily-cap on free tier is 1,000 credits (~43 renders/day) — never a constraint at our pace.
- **API key:** in `C:/Users/Dj4be/Desktop/Thesportsguru/.env` as `HYPEREAL_API_KEY` (shared from the Sports Guru project pipeline).
- **Ledger script:** `C:/Users/Dj4be/Desktop/Thesportsguru/youtube/hypereal_credits.py` — call `python … balance` to check; called automatically with `record <slug>` after each render to log spend.

### The four renders we ran today

| # | Purpose | Audio | Output | Credits |
|---|---|---|---|---|
| 1 | First end-to-end test (4 greetings) | 7s | 7.5s @ 480×480 (546 KB) | 23 |
| 2 | 31-phrase soundboard test | 57s | 56s @ 480×480 (4.1 MB) | 23 |
| 3 | Duration probe (mid) | 169s | 169s @ 480×480 (12.4 MB) | 23 |
| 4 | Duration probe (max) | 562s | 9:22 @ 480×480 (40 MB) | 23 |
| 5 | **Day 2 prototype master** (Elena workhorse pose) | 408s | 6:44 @ 480×480 (32 MB) | 23 |

Total today: 5 renders, 115 credits, $1.15. (Five not four — I miscounted in earlier messages.)

---

## ElevenLabs account state

- **Plan:** Starter ($6/mo) — confirmed by user via screenshot 2026-05-14
- **Quota:** 30,000 chars/mo on Starter (Free was 40k — Starter actually has lower per-month chars but unlocks commercial use and instant voice cloning). Verify quota in app.
- **Quota status:** very low at end-of-day (used 39,944 of 40,000 on previous tier before upgrade). Top-up applied this session.
- **For the full 60-day course (3 characters):** approximately 240k chars of TTS needed. Likely path: bump to **Creator ($22/mo, 100k)** for several months, or one month of **Pro ($99/mo, 500k)** to sprint.
- **API key:** in `C:/Users/Dj4be/Desktop/Thesportsguru/.env` as `ELEVENLABS_API_KEY`.

---

## File map — where everything lives

All paths below are inside the worktree:
`C:\Users\Dj4be\Desktop\New Bulgarian\.claude\worktrees\blissful-bouman-36288c\`

### Test sandbox folder
```
Bulgarian-avatars-test/
├── day02-avatars.html              first 4-phrase test page (B&W Elena)
├── day02-soundboard.html           31-phrase soundboard test page (B&W Elena)
├── day02-prototype.html            ⭐ THE MAIN DAY-2 PROTOTYPE (color Elena, all Tier-1 features)
├── .gitignore                      excludes _work directories, raw Elana PNGs, _shared_bg.json
├── Elana/                          6 raw 1024×1536 color portraits (user-uploaded, gitignored)
├── assets/
│   ├── elena.jpg                   original B&W Pexels portrait (full res 3264×4896)
│   ├── elena-square.jpg            B&W 720×720 — used by first test
│   ├── day02-greetings.mp3         first test audio (4 phrases)
│   ├── day02-segments.json         first test segment timings
│   ├── day02-long.mp3              31-phrase soundboard audio
│   ├── day02-long-segments.json    31-phrase segment timings
│   ├── day02-mega.mp3              169s duration-probe audio (3× day02-long)
│   ├── day02-giant.mp3             562s duration-probe audio (10× day02-long)
│   └── elena/
│       ├── 01-workhorse.jpg        720×720 color pose (Hypereal-ready)
│       ├── 02-greetings.jpg        ⭐ used in cold-open hero on day02-prototype.html
│       ├── 03-cultural.jpg
│       ├── 04-rules.jpg
│       ├── 05-grammar.jpg          ⭐ used in grammar spotlights
│       ├── 06-outro.jpg            ⭐ used in soundboard header + outro card
│       ├── day02-master.mp3        ⭐ THE PROTOTYPE AUDIO (6:48, 91 segments, post-processed)
│       └── day02-master-segments.json   ⭐ segment timing for the prototype
├── clips/
│   └── day02/
│       ├── day02-greetings.mp4     first 4-phrase render (7s)
│       ├── day02-long.mp4          31-phrase render (57s)
│       ├── day02-mega.mp4          169s probe render
│       ├── day02-giant.mp4         562s probe render (9:22)
│       ├── elena-day02-master.mp4  ⭐ THE PROTOTYPE MP4 (6:44, 32 MB, original)
│       └── elena-day02-master-fs.mp4   ⭐ FASTSTART VERSION the HTML references (seek-friendly)
├── duration_test/
│   ├── build_long_audio.py         generator for 31-phrase soundboard
│   ├── run_hypereal_long.py        Hypereal trigger for 57s render
│   ├── run_hypereal_mega.py        Hypereal trigger for 169s probe
│   ├── run_hypereal_giant.py       Hypereal trigger for 562s probe
│   └── day02-inventory.json        every Bulgarian utterance scraped from day02.html
├── day02_prototype/
│   ├── build_master_audio.py       ⭐ generator for Elena's 91-segment master audio
│   ├── slow_narration.py           ⭐ post-process to slow English narration by 8%
│   └── run_hypereal_master.py      ⭐ Hypereal trigger for the prototype MP4
├── generate_audio.py               first-test audio generator (legacy)
└── run_hypereal.py                 first-test Hypereal trigger (legacy)
```

### Memory files (persistent across sessions)
```
C:\Users\Dj4be\.claude\projects\C--Users-Dj4be-Desktop-New-Bulgarian\memory\
├── MEMORY.md                       index
└── feedback_full_paths.md          rule: always give full absolute paths
```

---

## The Day 2 prototype — features built

All sourced from the single 6:44 Elena master MP4. The HTML is fully self-contained (segments JSON inlined for `file://` compatibility).

| Tier | Feature | Where on page | Status |
|---|---|---|---|
| 1 | 90-sec cold recap card | Top of page | Built |
| 1 | Bakery cold-open cinematic | Hero section, auto-plays on scroll | Built |
| 1 | Section intros (per section) | Each `.section-header` has a pill | Built |
| 1 | Upgraded ▶ Listen buttons | All vocab tables | Built |
| 1 | Register toggle rockers | Section 5, four -те pairs | Built |
| 1 | Spotlight "Hear Elena explain" buttons | Four cultural sidebars | Built |
| 1 | Live quiz audio (reveal on wrong) | Mini-quiz section | Built |
| 1 | Mega-soundboard with category filters | End of page (37 tiles) | Built |
| 1 | Floating mini-avatar (corner) | Always rendered, shows when speaking | Built |
| 1 | Outro card | Bottom of page | Built |
| 2 | Dialogue shadow mode (2-sec gaps) | Roleplay 1 toggle | Built (untested) |
| 2 | "Play whole scene" dialogue queue | Roleplay 1 | Built (untested) |
| 3 | Three-avatar roleplay (Babà + Ivan + you) | Roleplay 2 (placeholder only — needs Ivan + Babà renders) | Not built |
| 3 | Read-the-room scenario dramatisations | Section 7 | Not built |
| 3 | "Grandma Test" pop-up drill | Post-Roleplay 2 | Not built |

---

## Brainstorm: audio-button alignment (the "buttons don't line up" problem)

### What we observed
User QA on the prototype: "hardly any of the buttons line up with the audio (sometimes no audio heard)". Worst near the end of the page.

### Root cause
The source audio we fed to Hypereal was **408.41s**. The MP4 that came back is **404.52s**. That's a **~3.89 second drift** — about 1% shorter. Hypereal trims/re-encodes the audio during rendering; the drift accumulates linearly through the file. Our segment timing JSON was built against the source audio, so:
- Early segments (cold_open, recap_1): off by tens of ms — barely noticeable.
- Mid segments: off by 1-2s.
- Late segments (spotlights, outro): off by 3-4s — completely wrong button-to-audio mapping.

### Immediate fix applied 2026-05-14 EOD
`Bulgarian-avatars-test/day02_prototype/scale_segments.py` — multiplies every segment's start/end by `mp4_duration / source_duration = 0.990475`. Outputs `assets/elena/day02-master-segments-scaled.json`. The HTML's inlined SEGS block was overwritten with the scaled values. Buttons should now land within ~100-200ms of their target, vs ~3-4s off before.

This is a quick fix. The remaining ~100ms drift may still cause minor "wrong start" issues on short phrases.

### Broader solutions to consider (worth a session of work)

**Solution A — Silence-detection-based calibration (more accurate, more fragile).**
Use ffmpeg's `silencedetect` filter on the MP4 to find real segment boundaries between gaps. Map detected regions 1:1 to source segment IDs. We attempted this (`recalibrate_segments.py`) and got close — 98 regions detected vs 91 expected because long atempo'd narration segments have internal sentence-break pauses that look identical to inter-segment gaps. Could refine with a hybrid: trust silence detection for short phrase segments; fall back to ratio scaling for long narration segments.

**Solution B — Make the gaps obviously unique (cheap, reliable).**
Use a distinctive marker frequency in the inter-segment gaps that wouldn't appear naturally. E.g., insert a very short low-volume sine-wave click (50ms, -40dB) as the FIRST sample of every gap. Then `silencedetect` becomes trivially reliable — detect every click, every boundary known. Costs nothing (still silent-feeling to the listener; click is sub-audible). Most robust option.

**Solution C — Pad the audio before rendering (preventative).**
Add an extra 5 seconds of leading silence and 5 seconds of trailing silence to the source audio. Hypereal's trim won't reach the spoken content. Source-audio timings would then map 1:1 to MP4 timings. Cost: 5-10 wasted seconds of render (still $0.23 same render). Simplest preventative measure for future renders.

**Solution D — Pull the audio track directly from the MP4 for timing.**
After downloading the Hypereal MP4, extract its audio with `ffmpeg -i mp4 -vn audio.wav`, run that through our silence-pipeline locally, generate segments. The MP4's audio IS what plays — so any timing derived from it is by definition correct. Most robust at the cost of one extra ffmpeg pass per render.

**Recommended for next renders:** Solution C (padded silence). 5s pre-roll and 5s tail. Zero new logic, no detection needed, perfectly stable timings going forward.

**Recommended for THIS already-rendered MP4:** the ratio scaling that's already in place is good enough for QA. If we discover specific phrases that are still off after this fix, we'll either re-render with padding or use Solution B's click-marker approach.

---

## Brainstorm: text preservation in the prototype

### The feedback
"You've cut way too much text. Some people learn by video, some by reading, often both. Even if there are drop downs or reveal buttons, all text should remain."

### What I cut from the live day02.html in the prototype
The prototype is a stripped-down demo, not a full-page replacement. I included:
- Section 3 (greetings by time of day) — kept the 4-row vocab table
- Section 5 (-те ending) — replaced the 4-pair table with register-toggle rockers
- Section 6 (polite phrases) — kept an 8-row table
- Section 8 (Roleplay 1) — kept the dialogue
- Mini-quiz — reduced from 20 questions to 2

I removed entirely:
- Long opening prose / bakery story (still referenced for the cold-open auto-play but cut from the page)
- Section 2 (ти vs Вие table with full notes columns)
- Section 4 (full hello/goodbye table with `Notes` column)
- Section 7 ("Reading the room" — four scenario boxes with reasoning)
- Roleplay 2 (Баба Мария)
- Roleplay 3 (Sofia café)
- Quiz questions 3-20
- Writing task (5 BG answers)
- Full recap table (11 rows with example phrases)

### Why this matters
The course has a triple audience:
- **Readers** — need the full prose, examples, cultural notes.
- **Listeners/Videos** — need Elena's narration AND the lip-synced visual.
- **Mixed learners** — read first, then listen, then read again with comprehension.

Cutting text optimises for the avatar-feature demo but destroys the page for the first audience.

### The fix
Rebuild the prototype starting from the FULL `day02.html` (1364 lines), layering avatar features ON TOP — never replacing prose, tables, or info-boxes. Specifically:

1. **The bakery cold-open**: keep the existing intro story as-is. Add the avatar BESIDE the story (don't merge them). The avatar narrates the same content but the text stays.
2. **Register table (Section 2 ти vs Вие)**: keep the full table + its golden rule box. Add a small "Hear both forms" rocker BENEATH it (additive, not a replacement).
3. **All vocab tables**: keep every column (Bulgarian, Romanised, English, Notes, Audio). Upgrade the `▶ Listen` button's audio source from browser-TTS to Elena's MP4 — same UX, better quality. Zero text changes.
4. **The -те ending table (Section 5)**: keep the full table. The "register toggle rocker" becomes a SECOND interactive element below it, demonstrating the same content in a different modality.
5. **Section 7 (Reading the room)**: keep all four scenario boxes verbatim. Each gets a tiny "Hear Elena dramatise this scenario" button. The reading text remains; Elena adds an audio layer.
6. **All three roleplays**: keep full text. Add "▶ Play whole scene" + "🎤 Shadow mode" controls above each.
7. **All info-boxes**: keep all prose. Add "Hear Elena explain" buttons where a spotlight clip exists.
8. **Quiz**: keep all 20 questions and ALL options. Live audio = additive reveal-on-wrong icon.
9. **Writing task**: keep verbatim, no avatar features needed (it's a written-output exercise).
10. **Recap table**: keep all 11 rows. The cold-recap card at the top references these same phrases via MP4 seek.

### Rule going forward
**Avatar features must be ADDITIVE, never substitutive.** Drop-downs and reveal-toggles are fine for tidiness, but the underlying text must be there for any reader who wants it.

### Plan for v2 prototype
Build `Bulgarian-avatars-test/day02-prototype-v2.html` starting as a copy of `day02.html`, then:
- Insert the cold-open hero, recap card, and section-intro pills as additions
- Rewire `data-text` audio buttons to seek into Elena's MP4 (keep the buttons, swap the backend)
- Add `data-seg` attributes alongside `data-text` to map each existing button to its master-MP4 segment ID
- Append the mega-soundboard and outro card at the end
- Add new "Hear Elena explain" buttons to existing info-boxes (where a spotlight exists)

---

## Bugs / known issues at end-of-day

1. **`fetch()` blocked on `file://`** — fixed by inlining the segments JSON into `day02-prototype.html`. The external JSON file remains as the source of truth; the inlined copy must be kept in sync if segment timings change.
2. **Seek-on-large-file** — fixed by:
   - Running `ffmpeg -movflags +faststart` on the master MP4 (moov atom at front).
   - Changing `preload="metadata"` → `preload="auto"`.
   - Adding `ensureBuffered()` to wait for the target timestamp to land in `video.buffered` before firing the seek.
   - The HTML references `elena-day02-master-fs.mp4` (faststart version), NOT the original `elena-day02-master.mp4`. Original is kept on disk but unused.
3. **First-click latency** — on first click after page load, there's a 1-3s wait while the buffer fills past the target timestamp. Subsequent clicks are instant. Acceptable.
4. **English-narration pacing** — user feedback: "sometimes a little fast in places". Fixed by post-processing 17 narration segments with `atempo=0.92` (8% slower) via `slow_narration.py`. The `build_master_audio.py` also passes higher `stability=0.78` for slow segments to ElevenLabs.

---

## Key learnings captured today

1. **Hypereal is flat-rate, not per-second.** Pricing was the architecture's biggest unknown; this finding unlocked the "long render + slice" pattern.
2. **Hypereal duration cap is at least 562s.** Could be higher — no need to probe further.
3. **ElevenLabs multilingual_v2 + a Bulgarian-native voice = the right TTS stack.** English narration spoken by a BG-native voice has a mild authentic accent — feels right for a Bulgarian-teacher persona.
4. **Same-model multi-pose portraits are hard to source from Pexels.** AI generation is the realistic path if we need more poses. The user provided 6 consistent color portraits this session.
5. **`file://` breaks `fetch()`.** Inline all data when building pages for local file testing.
6. **Large MP4s need `faststart` + `preload="auto"` + buffered-range checks** for seeks to work reliably.
7. **Browser TTS for `data-phonetic` is jarring** next to ElevenLabs-rendered audio. Once a page commits to Elena's MP4, retire the fallback for items the MP4 covers.
8. **Visual learners are an underserved audience** in language apps. The avatar-on-page pattern is rare in mainstream apps (Duolingo, Memrise, Pimsleur). This is a positioning advantage.
9. **A "soundboard at the end of every section" is the killer feature** — turns each lesson page into a permanent reference learners return to weeks later.
10. **Same MP4 can be referenced across multiple pages** (cross-page vocab atlas). Render once, browser-cache once, every later page free.

---

## Amendments log

Use this section in the next session. Walk through each amendment one-by-one. For each:
- **Item:** short title
- **Trigger:** what feedback prompted the change
- **Change made:** what was edited (file, line, behaviour)
- **Reasoning / learning captured:** WHY this matters going forward
- **Render impact:** does this need a new Hypereal render? new audio?

### Pending amendments (from QA observations)

_To be filled in next session — one row per item._

| # | Item | Trigger | Change | Learning | Render impact |
|---|---|---|---|---|---|
| 1 | _(walk through next session)_ | | | | |
| 2 | | | | | |
| 3 | | | | | |

### Already-applied amendments today

| # | Item | Change | Learning |
|---|---|---|---|
| 1 | B&W → color Elena | First test used B&W Pexels portrait; user provided 6 color poses mid-session, switched to `01-workhorse.jpg` for the prototype render | Color reads warmer for a teacher; B&W felt "serious art portrait". |
| 2 | Voice swap: Alice (English-Bulgarian) → Elena (BG-native) | User feedback: Alice "didn't sound very Bulgarian"; switched to ElevenLabs Voice Library Bulgarian voice. | Premade ElevenLabs voices speak Bulgarian via multilingual_v2 but with a non-native accent. The Voice Library has 30+ true-native BG voices — always start there for BG content. |
| 3 | Loudness | User said voice "a bit on the quiet side"; added `loudnorm=I=-14:LRA=11:TP=-1.5` ffmpeg filter to the concat step. | ElevenLabs output is conservatively mixed (~-23 LUFS). YouTube/Spotify standard is -14 LUFS. Always normalise final audio. |
| 4 | Narration pacing | User feedback: "sometimes a little fast in places". Tagged English-heavy segments with a "slow" prefix list, applied `atempo=0.92`. | ElevenLabs rushes longer English sentences; Bulgarian-only short clips were fine. Treat narration and vocab as separate pacing classes. |
| 5 | Seek bug (button N plays N samples) | Original first test: every button played from time 0 due to async `video.currentTime = X` before `play()`. | The `seeked` event must be awaited before `play()`. Codified in the working seek logic. |
| 6 | Seek bug on large MP4 | Prototype version: 32 MB MP4 with `preload="metadata"` — seeks snapped back to opening clip. | Three fixes required together: faststart, `preload="auto"`, and `ensureBuffered()` await. |
| 7 | `file://` fetch failure | Page initially loaded segments via fetch — silently failed on `file://`. | Inline data when targeting `file://` testing. Always test on `file://` as the lowest-friction QA path before going to a local server. |

---

## What "fully working" looks like (acceptance criteria for the prototype)

When the user QAs the prototype next session, these should all work:

- [ ] Cold-open auto-plays on scroll to Section 1 (autoplay may need user gesture first on some browsers).
- [ ] Cold-recap card plays the 11-phrase recap in sequence.
- [ ] Every ▶ Listen button plays only its own phrase, stops cleanly.
- [ ] Register-pair rockers play the matched form (ти or Вие) on click.
- [ ] Spotlight buttons play the explanation segment.
- [ ] Quiz wrong-answer reveals speaker icons; icons play their option's audio.
- [ ] Mega-soundboard tiles play; filter buttons reduce the grid.
- [ ] Floating mini-avatar appears bottom-right when something is playing, hides when idle.
- [ ] Outro card plays Elena's sign-off.

---

## Session work done while user was away (2026-05-14 final pass)

After the user reported v2 "very broken" with strict instructions to test methodically and not return until confident, I:

1. Diagnosed the actual v2 bugs (path prefix, seek-into-MP4 fragility, double-audio risk)
2. Switched to a **per-segment-audio-file architecture** — eliminates the seek alignment problem at the root. Each of the 91 segments is its own atomic MP3 file at `Bulgarian-avatars-test/audio/elena-day02/<seg>.mp3`.
3. Regenerated 17 missing slow segments via ElevenLabs (after user's Starter quota upgrade) — ~3,400 chars used.
4. Built `day02-prototype-v3.html` from the full `day02.html` (all 1364 lines of text preserved), with the old browser-TTS audio.js script REMOVED at build time (no possibility of double-fire).
5. Wrote `verify_v3_static.py` (8 structural checks: button wiring, file existence, path correctness, image resolution, MP4 resolution, old-script absence, structural blocks, soundboard coverage). All 8 pass.
6. Ran **three independent QC-agent audits** to find logic bugs. Total **5 critical defects found and fixed**:
   - Recap card stopped after 1 of 12 clips (queue wiped by stop() call inside playSegment)
   - "Добър ден" button played the shop-owner roleplay audio (normalize() stripped trailing `!` so both forms collided into one key)
   - Recap button couldn't be toggle-stopped (currentButton was null'd by playSegment when called from playQueue)
   - Cold-open stuck in "playing" UI state when browser autoplay was blocked (rejection wasn't cleaned up)
   - Cold-open MP4 audio could play simultaneously with an inline button's audio (stopAudio paused Audio but not coldVideo)
7. Added build-time existence check for all 27 non-button segment IDs (recaps, spotlights, intros, cold-open, outro). Build hard-fails if any audio file is missing.
8. Third QC pass returned ✓ ready to show user.

The QC log (`Bulgarian-avatars-test/day02_prototype/QC_LOG.md`) records the full investigation with timestamps, each bug, each fix, each verification, and lessons learned.

**File for user QA when they return:**
```
C:\Users\Dj4be\Desktop\New Bulgarian\.claude\worktrees\blissful-bouman-36288c\Bulgarian-avatars-test\day02-prototype-v3.html
```

Open the file directly — no server needed. (The v2 prototype at `day02-prototype-v2.html` is now superseded; v3 fixes its bugs.)

---

## Session work done while user was away (2026-05-14 late)

While the user was offline, two improvements were made based on their parting feedback:

### 1. Audio button alignment fix
- Detected the ~3.89s drift between source audio (408.41s) and rendered MP4 (404.52s).
- `Bulgarian-avatars-test/day02_prototype/scale_segments.py` — scales segment timings by `mp4_dur / src_dur = 0.99047`.
- Output: `Bulgarian-avatars-test/assets/elena/day02-master-segments-scaled.json`.
- Replaced inlined SEGS block in `day02-prototype.html` with scaled values.
- Buttons in the existing prototype should now land within ~100-200ms of target (was 3-4s off).

### 2. v2 prototype preserving all original text
- New file: `Bulgarian-avatars-test/day02-prototype-v2.html` (~133 KB)
- Built by `Bulgarian-avatars-test/day02_prototype/build_v2.py` which:
  - Reads the live `day02.html` (1364 lines, 103 KB)
  - Adds `data-seg="..."` to every existing `.play-audio` button (59 of them mapped)
  - Injects Elena CSS in a new `<style>` block (no conflict with existing styles)
  - Injects 6 content blocks: cold-open hero, recap card, section pills, spotlight buttons, mega-soundboard, outro card, floating mini-avatar
  - Adds the controller JS using capture-phase click delegation to intercept the existing audio.js handler — Elena's MP4 wins
- **All original text is preserved.** Every table column, info-box, scenario, roleplay, quiz question, recap entry, and writing task remains exactly as in `day02.html`.

### What the user should QA on the v2 prototype
Open:
`C:\Users\Dj4be\Desktop\New Bulgarian\.claude\worktrees\blissful-bouman-36288c\Bulgarian-avatars-test\day02-prototype-v2.html`

Check:
- Is ALL the original text still there? (Should be — verify a few sections.)
- Do existing `▶ Listen` buttons now play Elena's voice instead of browser TTS?
- Does the cold-open hero block appear AFTER the bakery story info-box?
- Does the recap card appear at the top of the main content?
- Do section pills appear next to each Section X header (Sections 2-8)?
- Do "Hear Elena explain" buttons appear on the cultural sidebars?
- Does the mega-soundboard appear at the end before the footer?
- Does the floating mini-avatar appear bottom-right when Elena is speaking?
- Are the audio buttons now lined up with the right phrases?

Potential issues to look for:
- **Double audio**: if both Elena AND the existing audio.js fire, you'll hear two voices. The capture-phase + preventDefault should prevent this, but the existing handler might be attached differently than expected. If you hear doubles, we add a hard `.play-audio` handler nuke at init.
- **CSS conflicts**: Elena CSS uses scoped class names (elena-*) but variable references (`--navy`, etc.) inherit from day02.html's :root. Should look consistent. If anything looks broken, easy to tweak the elena-css block.
- **Layout overlap**: the mega-soundboard sits inside `<main>` near the bottom; if there's any conflict with the existing footer/recap table, we adjust the injection anchor.

If v2 looks right, we kill `day02-prototype.html` (the stripped-down original) and treat v2 as the canonical prototype going forward.

---

## Tomorrow's first task (carry-over)

**Walk through user's QA amendments one-by-one.** For each:
1. Capture in the "Pending amendments" table above.
2. Discuss + decide the fix.
3. Implement (free TTS regenerations / page edits as needed; new renders cost $0.23 each — get explicit approval before firing one).
4. Update the "Already-applied amendments" table once landed.

After the QA loop closes, the next major task is **sourcing Ivan + Babà portraits and rendering their voices** — this unlocks the multi-character roleplays on Day 2 and is the gate to scaling beyond Day 2.
