# Project Status

Last updated: 2026-04-09

This file is the interruption-safe handover log for the Bulgarian course project at **learnbulgarian.io**.
Update it after every meaningful content, QA, audio, or workflow change.

---

## What This Project Is

A free, self-study 60-day Bulgarian language course for English speakers. Covers A1 → B1 (Pre-intermediate / Intermediate). Every lesson page is a standalone HTML file with rich audio, vocabulary tables, dialogues, quizzes, writing tasks, and a recap section.

**Live URL:** https://learnbulgarian.io/bulgarian/

---

## Hosting & FTP

| Key | Value |
|-----|-------|
| Host (SFTP) | access811018624.webspace-data.io |
| Username | u99549562 |
| Password | United!!001ad |
| Protocol | SFTP (port 22) — FTP is disabled on this server |
| Site root | /app811033055/bulgarian/ |
| Audio root | /app811033055/bulgarian/audio/ |

**Upload with paramiko (Python) — preferred for Cyrillic filenames:**
```python
import paramiko
transport = paramiko.Transport(("access811018624.webspace-data.io", 22))
transport.connect(username="u99549562", password="United!!001ad")
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put("local_file.html", "/app811033055/bulgarian/local_file.html")
```

**Upload HTML only with curl:**
```bash
curl --insecure -T day01.html \
  "sftp://access811018624.webspace-data.io/app811033055/bulgarian/day01.html" \
  --user "u99549562:United!!001ad"
```

---

## Audio Generation

### How it works

- Each play button in the HTML has a `data-text` attribute (Bulgarian text to speak)
- The script `generate_pro_audio.py` scans all `data-text` values and calls Google Cloud TTS
- Voice: **bg-BG-Standard-A** (female Bulgarian)
- MP3s are saved to `audio/<day-name>/`
- The page JavaScript tries the MP3 first; if it fails it falls back to browser Web Speech API

### Commands

Always run from the project folder using the venv Python:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py day17.html
```

Multiple files at once:
```bat
venv\Scripts\python.exe generate_pro_audio.py day17.html day18.html day19.html
```

Force overwrite existing MP3s (use after editing dialogue text):
```bat
venv\Scripts\python.exe generate_pro_audio.py --force day18.html
```

### Critical rule — Cyrillic filenames

The browser's `makeFilename()` function and the Python generator must sanitise Bulgarian text **identically**. If they differ, the page will silently fall back to speech synthesis instead of playing the stored MP3. This was fixed in the shared JS across all pages.

---

## CEFR Level Labels

| Level | Correct label |
|-------|--------------|
| A1 | Beginner / Elementary |
| A2 | Elementary / Pre-intermediate |
| B1 | Pre-intermediate / Intermediate |

**In badges and optgroups:**
- A1 → "A1 — Beginner"
- A2 → "A2 — Pre-intermediate"
- B1 → "B1 — Pre-intermediate / Intermediate"

**Key fact:** A2 is NOT Intermediate. B1 is NOT Advanced.

---

## File Structure

```
C:\Users\Dj4be\Desktop\New Bulgarian\
├── day01.html … day60.html      ← WORKING FILES (edit these)
├── audio/
│   ├── day01/                   ← MP3s for day01
│   ├── day02/ … day60/
├── backup/                      ← Recent auto-backups
├── Old Files not in use/        ← Archive of superseded files
├── generate_pro_audio.py        ← Audio generator
├── venv/                        ← Python virtual environment
├── PROJECT_STATUS.md            ← This file
└── PROJECT_INFO.html            ← Visual project dashboard
```

**Never edit files in `backup/` or `Old Files not in use/` — edits go in the root only.**

---

## How to Amend a Day

1. Edit the root `dayXX.html` file
2. If you changed any `data-text` attribute values, regenerate audio:
   ```bat
   venv\Scripts\python.exe generate_pro_audio.py --force dayXX.html
   ```
3. Upload the HTML and audio folder to the server:
   - HTML: `/app811033055/bulgarian/dayXX.html`
   - Audio: `/app811033055/bulgarian/audio/dayXX/` (all MP3s)
4. Commit to git:
   ```bat
   git add dayXX.html audio/dayXX/
   git commit -m "Brief description of change"
   ```

---

## Git Workflow

Repository is on the local machine. Commit after every meaningful batch of changes.

```bat
git add day*.html
git commit -m "Description of changes"
git log --oneline -10
```

---

## Current State of All 60 Days (as of 2026-04-09)

**All 60 days are COMPLETE, UPLOADED, and UP TO DATE on the live server.**

### What every root day file now has:
- Full JSON-LD SEO schema (@graph: LearningResource + BreadcrumbList + FAQPage)
- Open Graph and Twitter Card meta tags
- Scene-setting cultural introduction before Section 1
- Cultural enrichment row in the recap table
- Dense MP3 audio (all data-text buttons served from audio/ directory)
- Mobile-responsive layout
- Correct CEFR labels (A2 = Pre-intermediate, B1 = Pre-intermediate / Intermediate)
- All URLs pointing to learnbulgarian.io (no whatchan.co.uk references)
- All prices in euros (Bulgaria adopted the euro on 1 January 2026)

---

## Major Changes Made (Chronological)

### Phase 1 — Structure and credibility
- Audited all files; created `Old Files not in use/` archive
- Removed broken `exam-a2.html` references from `index.html` and `sitemap.xml`
- Fixed CEFR labels: A2 "Intermediate" → "Pre-intermediate"; B1 "Advanced" → "Intermediate"
- Fixed Russian contamination: `это`→`това`, `новый`→`нов`, `где`→`къде`, `который`→`който`

### Phase 2 — Audio and teaching quality (Days 17–34)
- Rebuilt lessons one by one with dense per-item audio (data-text on every table row)
- Added scene-setting intros, practical phrase sections, line-by-line dialogue audio
- Corrected unnatural Bulgarian, awkward transliterations, mixed-script bugs
- Added mobile table stacking (cards with header labels) for phone usability
- Fixed `generate_pro_audio.py` to support `--force` flag
- Fixed browser `makeFilename()` to preserve Cyrillic → correct MP3 filenames

### Phase 3 — SEO and engagement (Days 18–60)
- Added JSON-LD structured data schema to every day (Days 18–60 batched)
- Added Open Graph + Twitter Card meta tags to all pages
- Added cultural scene-setting intro to Days 18–27 (Days 28–60 already had them)
- Added cultural recap row to every day's recap table
- Fixed mixed Cyrillic/Latin character bugs: Day 21 (×1), Day 24 (×1), Day 25 (×1), Day 32 (×2), Day 33 (×2), Day 34 (×1), Day 37 (×1)

### Phase 4 — Domain migration
- Replaced all 120 whatchan.co.uk font references with learnbulgarian.io across all 60 root files
- Zero whatchan.co.uk references remain in root files

### Phase 5 — Currency conversion (euro adoption 1 Jan 2026)
- Rate: 1 EUR = 1.95583 BGN (irrevocable conversion rate)
- Converted all лева/лв dialogue prices to евро in:
  - Day 18: market dialogue
  - Day 21: train ticket dialogue
  - Day 22: pharmacy dialogue
  - Day 30: clothes shopping dialogue
  - Day 47: flat hunting dialogue + recap row
  - Day 59: hotel booking dialogue
- Updated Bulgarian text, romanisation, English translations, and audio data attributes
- Regenerated MP3 audio for all 6 days
- Educational/historical references (conversion rate explanation, quiz distractors) left as-is

### Phase 6 — CEFR correction (2026-04-09)
- B1 label updated: "Intermediate" → "Pre-intermediate / Intermediate" across 25 files
- day01.html course description updated: "to pre-intermediate (B1)" → "to intermediate (B1)"

---

## Quality Rules

- Review as a native Bulgarian teacher checking work for English-speaking adult learners
- Reject Russian intrusions, false friends, awkward calques, unnatural Bulgarian
- CEFR: A2 = Pre-intermediate (NOT Intermediate), B1 = Pre-intermediate/Intermediate (NOT Advanced)
- Use `day16.html` as the model for audio density and pedagogical richness
- Every lesson should feel engaging, not like a flat word list
- Add Bulgarian-specific facts, customs, and practical local detail
- Every lesson must pass a mobile acceptance check
- After every change: update PROJECT_STATUS.md, regenerate audio if needed, upload, commit

---

## Known Issues / Residual Risks

- Pages with unusual custom sections may still need page-specific mobile CSS after live spot checks
- `day01.html` alphabet audio should be verified live (MP3 pause between letter and example word)
- Audio generation requires Google Cloud credentials configured in the venv environment

---

## Reference Files

| File | Purpose |
|------|---------|
| `QUALITY_CHECK_AGENT.md` | QA review checklist |
| `ENGAGEMENT_AGENT.md` | Engagement review standard |
| `DAY_UPGRADE_WORKFLOW.md` | Step-by-step lesson upgrade process |
| `COURSE_REVIEW_ROADMAP.md` | Long-term course improvement plan |
| `PROJECT_INFO.html` | Visual project dashboard (open in browser) |
