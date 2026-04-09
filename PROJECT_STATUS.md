# Project Status

Last updated: 2026-04-08 18:18:00 +03:00

This file must be updated after every meaningful content, QA, audio, or workflow change.

## Purpose

This is the interruption-safe handover log for the Bulgarian course project.

Use it to answer:
- what has already been fixed
- what standard the work should follow
- which lesson is currently being upgraded
- what to do next

## Current Standard

Reference lesson for A2 upgrade quality:
- `day16.html`

Quality review rules:
- `QUALITY_CHECK_AGENT.md`
- `ENGAGEMENT_AGENT.md`

One-day upgrade process:
- `DAY_UPGRADE_WORKFLOW.md`

## Active Strategy

- Upgrade lessons one day at a time
- Prioritize quality and accuracy over speed
- Treat `day16.html` as the model for dense audio and stronger teaching structure
- Run a Bulgarian-teacher-style QA pass before considering a lesson complete
- Do not treat this as an audio-only project
- Each lesson may need new teaching elements, more examples, clearer explanations, richer vocabulary support, and structural improvements
- Visitors respond well to abundant examples, so every lesson should include generous supporting examples around the topic
- Lessons must not feel like flat word lists; each one should include engaging, topic-relevant material and Bulgarian-specific detail where useful
- An explicit engagement review is now part of the acceptance process

## New Engagement Requirement

Problem identified:
- some rebuilt modules are becoming too list-like despite stronger audio and accuracy

Response adopted:
- added `ENGAGEMENT_AGENT.md`
- updated `DAY_UPGRADE_WORKFLOW.md` so each lesson must be reviewed for engagement as well as accuracy
- from this point on, lessons should include more interesting Bulgarian context, practical human scenarios, and culturally useful details where relevant
- lessons should open with a stronger scene-setting introduction before Section 1 where the topic benefits from it

Roadmap impact:
- continue forward lesson rebuilds with this stronger engagement standard
- later revisit previously rebuilt modules to add more cultural and motivational content where they still feel too list-heavy
- treat that revisit as required work, not optional polish: every module should be informative, entertaining, and educational

## Confirmed Course Corrections Already Made

### File cleanup and structure

- Audited active vs old files
- Created archive folder: `Old Files not in use`
- Added archive report: `Old Files not in use/REPORT.txt`
- Removed broken `exam-a2.html` references from `index.html` and `sitemap.xml`

### CEFR wording fixes

- Replaced `A2 - Intermediate` / `A2 &mdash; Intermediate` with `A2 - Pre-intermediate` / `A2 &mdash; Pre-intermediate`
- Replaced `B1 - Advanced` / `B1 &mdash; Advanced` with `B1 - Intermediate` / `B1 &mdash; Intermediate`

### Russian / non-Bulgarian credibility fixes

- `day07.html`: `это` -> `това`
- `day10.html`: `новый` -> `нов`
- `day38.html`: `где` -> `къде`
- `day46.html`: `который` -> `който`

## Audio Workflow

Main generator:
- `generate_pro_audio.py`

What it does:
- scans HTML pages for `data-text`
- creates MP3 files in `audio/<page-name>/`
- uses the Bulgarian text in `data-text` as the spoken source

Run from:
- `C:\Users\Dj4be\Desktop\New Bulgarian`

Command pattern:

```bat
venv\Scripts\python.exe generate_pro_audio.py day17.html
```

Or for multiple files:

```bat
venv\Scripts\python.exe generate_pro_audio.py day43.html day49.html day52.html
```

## Audio Coverage Baseline

Measured `data-text` density:

- `day01` to `day16`: average `112.9`
- `day17` to `day34`: average `4.9` before upgrades

This is the reason the later A2 lessons need rebuilding, not just small edits.

## Lessons Already Upgraded For Audio / Structure

### Earlier pass

- `day35.html`
- `day50.html`
- `day60.html`
- `exam-b1.html`
- `day43.html`
- `day49.html`
- `day52.html`
- `day53.html`
- `day54.html`
- `day59.html`

### Current one-day upgrade track

- `day17.html` upgraded
- `day18.html` upgraded
- `day19.html` upgraded

## Day 17 Status

Reference comparison:
- `day16.html`: `130` `data-text` entries
- `day17.html`: increased from `5` to `64` `data-text` entries

Day 17 changes completed:
- added per-item audio to the main restaurant vocabulary table
- added per-item audio to the ordering phrases table
- added per-item audio to the taste/texture table
- added per-item audio to the paying-the-bill table
- added line-by-line dialogue audio controls
- corrected `servityor ka` -> `servityorka`
- corrected the vegetarian model answer so it no longer teaches an allergy sentence
- corrected the quiz answer option to match the taught phrase `Имате ли свободна маса за двама?`
- improved dialogue naturalness: `Прясна е` -> `Току-що е приготвена`

Day 17 QA status:
- Pass for current stage
- Still below `day16` density, but substantially improved and directionally correct

Day 17 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py day17.html
```

## Day 18 Status

Reference comparison:
- `day18.html`: increased from `5` to `51` `data-text` entries

Day 18 changes completed:
- corrected awkward shop names:
  - `дрехи магазин` -> `магазин за дрехи`
  - `обувки магазин` -> `магазин за обувки`
- corrected mixed-script transliteration contamination in shop names
- replaced the less useful `Фактура, моля.` with `Касова бележка, моля.`
- improved market dialogue naturalness:
  - `Ресто два лева` -> `Два лева ресто`
  - `here is five leva` -> `here are five leva`
- added per-item audio to:
  - shop types
  - quantities and measures
  - shopping transaction phrases
- added new supporting content:
  - quantity-request note
  - useful market-request example card
  - extra example audio block
  - line-by-line market dialogue audio

Day 18 QA status:
- Pass for current stage
- richer and more reliable than the original page
- still below `day16` density, but substantially improved

Day 18 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py day18.html
```

## Day 19 Status

Reference comparison:
- `day19.html`: increased from `5` to `61` `data-text` entries

Day 19 changes completed:
- upgraded the professions table with per-item audio
- corrected the teaching note for `учител` vs `преподавател`
- improved the lawyer note to explain formal title usage
- upgraded the workplace vocabulary table with per-item audio
- upgraded the “talking about work” table with per-item audio
- added extra work-conversation examples for English-speaking learners
- upgraded the work-verbs table with per-item audio
- cleaned mixed-script transliteration contamination in the work-verbs section
- cleaned transliteration for `от вкъщи`

Day 19 QA status:
- Pass for current stage
- substantially richer and more teachable than the original page
- still below `day16` density, but well beyond token audio coverage

Day 19 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py day19.html
```

## Mobile UX Fixes

### Day 17

- added explicit mobile layout rules for small screens
- made vocabulary tables horizontally scrollable on phones
- tightened mobile spacing for hero, sections, reading cards, recap, quiz, and coffee block
- forced audio buttons inside mobile tables to remain visible and tappable
- made section-level audio controls full-width on mobile for easier tapping

### Day 18 and Day 19

- applied the same mobile-first table and control fix as Day 17
- made expanded vocab tables horizontally scrollable on phones
- kept in-table audio controls visible and tappable on small screens
- tightened mobile spacing for the upgraded lesson layout

### Stronger Mobile Table Fix

- replaced the horizontal-scroll-only approach with stacked mobile vocab cards for Day 17, Day 18, and Day 19
- hid table headers on phones and rendered each row as a vertical card
- this prevents the audio column from being pushed off-screen on smaller devices/browsers
- made the in-table mobile audio area explicitly labeled as `Audio`
- expanded icon-only controls into visible `Play` / `Stop` buttons on phones

### Day 17 Mobile Fallback

- added an explicit mobile-only vocabulary card list for Section 1 on Day 17
- this duplicates the individual word audio controls outside the table structure so mobile browsers cannot hide them

Reason:
- the new per-item audio column was not reliably visible on mobile
- the page needed stronger small-screen handling after the desktop-oriented content expansion

## Day 01 Audio Regression

Issue found:
- some `day01` alphabet buttons were playing stale MP3 files instead of refreshed lesson audio
- the generator script skipped existing files, so old audio could survive after text improvements
- this could remove the intended pause between the letter and the example word and could also preserve outdated examples
- a larger root cause was then confirmed: the browser-side `makeFilename()` logic stripped Cyrillic text and often requested `_.mp3` instead of the real Bulgarian MP3 filename
- when that happened, pages silently fell back to browser/system speech synthesis instead of using the stored MP3 sample

Fixes applied:
- `generate_pro_audio.py` now supports `--force` so existing MP3 files can be intentionally regenerated
- `day01.html` restored the `Е` example to `Е. Ема` for clearer beginner pronunciation practice
- the shared `makeFilename()` logic was corrected across all lesson pages so Bulgarian text now maps to the same MP3 filenames produced by `generate_pro_audio.py`

Day 01 regeneration command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day01.html
```

Validation focus:
- after regeneration, `day01` should play stored MP3s instead of speech synthesis fallback
- the `A` and `E` alphabet buttons should again have the intended pause between the letter and the example word

## Next Recommended Task

- Regenerate `day01.html` audio with `--force` and confirm the alphabet pause is restored
- Then audit and upgrade `day20.html`
- Follow the same sequence:
  1. audit structure and language
  2. improve pedagogy and naturalness
  3. add new lesson elements where needed
  4. expand topic coverage with many useful examples
  5. add dense audio coverage
  6. run QA review
  7. generate MP3s

## Maintenance Rule

After every change, update:
- this file
- `PROJECT_INFO.html`

## Shared Mobile Layout Pass

Issue found:
- the early lesson template was still largely desktop-first
- `day02.html` exposed the problem clearly, but the same structure existed across most lesson pages
- dense content blocks such as vocab tables, recap tables, roleplay cards, dialogue rows, audio zones, and page controls did not reflow reliably on phones

Fix applied:
- added a shared mobile CSS layer across all `day01.html` to `day60.html` pages plus `exam-b1.html`
- tightened hero and section spacing on small screens
- made major controls full-width and easier to tap
- made vocab and recap tables scroll safely instead of breaking the layout
- stacked roleplay/dialogue/card layouts vertically on phones
- collapsed common grids to one column on smaller screens

Deployment note:
- this fix is in the HTML files, so the updated pages must be uploaded before the mobile improvements appear live

Residual risk:
- pages with unusual one-off custom sections may still need page-specific mobile cleanup after live spot checks

## Day 02 Mobile Follow-up

User feedback:
- `day02.html` still looked poor on mobile after the shared mobile pass
- the formal/informal table was still rendering like compressed desktop columns

Fix applied:
- added page-specific mobile table-card styling to `day02.html`
- the major Day 2 tables now stack each row into a labeled card on phones instead of squeezing multiple columns into narrow widths
- applied this to the register, greeting, hello/goodbye, `-те` pattern, polite phrases, survival phrases, and recap tables

## Early Lesson Mobile QA Sweep

Scope:
- `day03.html` to `day16.html`

Issue pattern:
- many early lessons still used dense desktop tables for vocabulary, grammar comparisons, and recap blocks
- the shared mobile pass improved spacing but did not fully solve narrow multi-column table layouts

Fix applied:
- added a stronger mobile table system to `day03.html` through `day16.html`
- on phones, `.vocab-table`, `.recap-table`, `.agree-table`, and `.article-table` now render as stacked cards
- added a small table-label script so each mobile table cell shows its original column header as a label
- this avoids compressed columns and makes the early lessons much more readable on smaller screens

Deployment note:
- these fixes are in the HTML files and must be uploaded before the live mobile versions improve

## Day 20 Status

Reference comparison:
- `day20.html`: increased from `5` to `57` `data-text` entries

Day 20 changes completed:
- upgraded the routine-verbs table with per-item audio
- upgraded the frequency-adverbs table with per-item audio
- rebuilt the time-expressions table with practical examples and per-item audio
- added a new practical section of short daily-routine phrases with individual audio buttons
- improved the model routine text to sound more natural in Bulgarian
- corrected awkward phrasing such as `отивам на спорт` to a more natural routine example
- corrected the dialogue phrase `Трябва ми много сутрин` to `Трябва ми повече време сутрин`
- corrected the dialogue question `Кога вечерям обикновено?` to `Кога вечеряш обикновено?`
- fixed the next-page pager label to `Day 21: Transport & Travel`
- fixed the Day 20 mobile selector label so it matches the actual lesson topic
- added a page-specific mobile table-label script so Day 20 tables stack more cleanly on phones

Day 20 QA status:
- Pass for current stage
- much stronger pedagogy and audio coverage than the original page
- still needs MP3 generation for the new per-item audio targets

Day 20 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day20.html
```

## Day 21 Status

Reference comparison:
- `day21.html`: increased from `5` to `60` `data-text` entries

Day 21 changes completed:
- upgraded the transport-types table with per-item audio
- corrected transport notes and transliteration cleanup, including `мотоциклет` transliteration and timetable-related forms
- upgraded the station-vocabulary table with per-item audio
- upgraded the ticket-buying table with per-item audio and more realistic sample targets
- upgraded the bus/metro section with per-item audio
- added a new practical travel-phrases section with individual audio buttons
- improved the station dialogue so it sounds more natural in Bulgarian
- corrected stale navigation labels for Day 20 and Day 22
- added a page-level mobile table-label script so Day 21 tables stack more cleanly on phones

Day 21 QA status:
- Pass for current stage
- much stronger pedagogy and audio coverage than the original page
- still needs MP3 generation for the new per-item audio targets

Day 21 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day21.html
```

## Day 22 Status

Reference comparison:
- `day22.html`: increased from `5` to `69` `data-text` entries

Day 22 changes completed:
- upgraded the body-parts table with per-item audio
- upgraded the `боли ме / болят ме` table with per-item audio
- upgraded the illnesses-and-symptoms table with per-item audio
- upgraded the doctor-and-pharmacy table with per-item audio
- added a new practical health-phrases section with individual audio buttons
- improved the pharmacy dialogue so it sounds more natural in Bulgarian
- corrected stale navigation labels for Day 20, Day 21, and Day 23
- added a page-level mobile table-label script so Day 22 tables stack more cleanly on phones

Day 22 QA status:
- Pass for current stage
- much stronger pedagogy and audio coverage than the original page
- still needs MP3 generation for the new per-item audio targets

Day 22 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day22.html
```

## Day 23 Status

Reference comparison:
- `day23.html`: increased from `5` to `50` `data-text` entries

Day 23 changes completed:
- tightened the aorist explanation so it teaches completed past actions more clearly for English-speaking learners
- added a new trigger-examples table showing when the aorist is used in natural sentences
- expanded Group 1 verbs with practical model sentences and per-item audio
- expanded Group 2 verbs with practical model sentences and per-item audio
- rebuilt the irregular aorists section with individual example sentences and removed the duplicate `дойда` entry
- rebuilt the time-expressions section with individual audio buttons for the key past-time phrases
- added a new practical past-story phrases section for high-frequency speaking chunks
- replaced the old compact dialogue block with line-by-line dialogue audio
- corrected stale navigation labels for Day 19 to Day 23 in the mobile selector and fixed the pager labels for Day 22 and Day 24
- added a page-level mobile table-label script so Day 23 tables stack more cleanly on phones

Day 23 QA status:
- Pass for current stage
- grammar explanation is materially stronger than the original page
- audio coverage is now dense enough for a first full pass, though still lighter than the very strongest early modules
- still needs MP3 generation for the new per-item audio targets

Day 23 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day23.html
```

## Day 24 Status

Reference comparison:
- `day24.html`: increased from `5` to `39` `data-text` entries

Day 24 changes completed:
- strengthened the core explanation of `ще + present tense` for English-speaking learners
- added a new present-vs-future comparison table with practical example sentences and per-item audio
- corrected the wrong positive example `Ще валя` to `Ще вали`
- rebuilt the negative-future section with individual audio buttons for each positive/negative pair
- rebuilt the future-time-expressions section with per-item audio and corrected mixed-script transliteration on `вдругиден`
- rebuilt the questions-and-conditionals section with individual audio
- added a new useful future-chunks section for high-frequency speaking phrases
- replaced the old compact dialogue block with line-by-line dialogue audio
- corrected stale navigation labels for Day 19 to Day 24 in the mobile selector and fixed the pager labels for Day 23 and Day 25
- added a page-level mobile table-label script so Day 24 tables stack more cleanly on phones

Day 24 QA status:
- Pass for current stage
- grammar accuracy is stronger than the original lesson and the obvious content error is fixed
- audio coverage is now substantially improved, though still lighter than the strongest early modules
- still needs MP3 generation for the new per-item audio targets

Day 24 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day24.html
```

## Day 25 Status

Reference comparison:
- `day25.html`: increased from `5` to `53` `data-text` entries

Day 25 changes completed:
- fixed the Russian intrusion `довольна` and corrected the paired adjective form to `доволна`
- corrected mixed-script corruption in `сериозен`
- rebuilt the core emotions section with proper masculine/feminine teaching and individual audio examples
- rebuilt the feeling-expression section with per-item audio for the most useful emotional constructions
- rebuilt the asking-about-feelings section with individual audio buttons
- rebuilt the personality section with clearer adjective pairs and per-item audio examples
- added a new comforting-and-responding section with practical support phrases
- replaced the old compact dialogue block with line-by-line dialogue audio
- corrected stale navigation labels for Day 19 to Day 25 in the mobile selector and fixed the pager labels for Day 24 and Day 26
- added a page-level mobile table-label script so Day 25 tables stack more cleanly on phones

Day 25 QA status:
- Pass for current stage
- credibility issues are materially improved because the Russian contamination and broken forms are removed
- pedagogy is much stronger for English-speaking learners because adjective pairs and response phrases are clearer
- still needs MP3 generation for the new per-item audio targets

Day 25 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day25.html
```

## Day 26 Status

Reference comparison:
- `day26.html`: increased from `5` to `63` `data-text` entries

Day 26 changes completed:
- fixed the broken `дъга` row where English and Bulgarian had been swapped
- corrected mixed-script corruption in `мълния` and `мъгливо`
- corrected the weather vocabulary and transliteration quality across the page
- rebuilt the main weather vocabulary section with per-item audio
- rebuilt the weather-expressions section with per-item audio for the key impersonal constructions
- rebuilt the seasons section with clearer seasonal example sentences and individual audio
- rebuilt the forecast-and-plans section with per-item audio
- added a new useful weather-chunks section for everyday speech
- replaced the old compact dialogue block with line-by-line dialogue audio
- corrected stale navigation labels for Day 19 to Day 26 in the mobile selector and fixed the pager labels for Day 25 and Day 27
- added a page-level mobile table-label script so Day 26 tables stack more cleanly on phones

Day 26 QA status:
- Pass for current stage
- obvious credibility issues are fixed and the lesson now reads more naturally
- pedagogy is much stronger because weather, forecasts, and seasonal phrases are now separated more clearly
- still needs MP3 generation for the new per-item audio targets

Day 26 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day26.html
```

## Day 27 Status

Reference comparison:
- `day27.html`: increased from `4` to `77` `data-text` entries

Day 27 changes completed:
- corrected the broken transliteration `kolektsionirana` to `kolektsionirane`
- corrected the unnatural model phrase `Четенето е моят любим хоби` to `Четенето е любимото ми хоби`
- corrected mixed-script transliteration corruption in `на ниво аматьор`
- corrected the dialogue prompt from `Какво обичам да правиш` to `Какво обичаш да правиш`
- replaced the unnatural `Ходя планинарство всяка събота` with the more natural `Ходя на планина почти всяка събота`
- rebuilt the main hobbies vocabulary table with per-item audio
- rebuilt the sports vocabulary table with per-item audio
- rebuilt the interests-and-questions section with more practical model sentences and per-item audio
- rebuilt the frequency-and-intensity section with individual audio plus extra example sentences
- added a new useful hobby-phrases section for everyday conversation
- expanded the Bulgarian cultural-life section and added individual audio there too
- replaced the old compact dialogue block with line-by-line dialogue audio
- corrected stale navigation labels in the mobile selector and fixed the pager labels for Day 26 and Day 28
- added a page-level mobile table-label script so Day 27 tables stack more cleanly on phones
- replaced the weak scrollable-table mobile behavior with stacked mobile cards so the per-word audio buttons stay visible without horizontal scrolling

Day 27 QA status:
- Pass for current stage
- the obvious language and transliteration errors are fixed
- pedagogy is materially stronger because the page now teaches vocabulary, patterns, and conversation chunks separately
- still needs MP3 generation for the new per-item audio targets

Day 27 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day27.html
```

## Day 28 Status

Reference comparison:
- `day28.html`: increased from `5` to `87` `data-text` entries

Day 28 changes completed:
- corrected the broken note text in the hostel row and removed mixed-script corruption
- corrected the mixed-script transliteration `hizhа` to `hizha`
- corrected `Стаята не е почистена` transliteration from `pochostena` to `pochistena`
- corrected the unnatural `Шумно е много` to `Много е шумно`
- made the check-in request more natural with `Ключа за стаята, моля`
- rebuilt the accommodation table with per-item audio
- rebuilt the room-features section with per-item audio and added practical question examples
- rebuilt the check-in and check-out section with per-item audio and clearer ordering for English-speaking learners
- rebuilt the requests-and-problems section with per-item audio and cleaner Bulgarian
- added a new useful hotel-phrases section for everyday speaking
- added a new Bulgarian stay-culture section with guesthouse, spa, old-town, and parking vocabulary plus Bulgarian-specific accommodation context
- added a new scene-setting introduction before Section 1 so the lesson starts with Bulgarian travel context instead of jumping straight into lists
- replaced the old compact dialogue block with line-by-line dialogue audio
- corrected stale navigation labels in the mobile selector and fixed the pager labels for Day 27 and Day 29
- added the stronger mobile table-card layout so per-word audio buttons stay visible on phones without horizontal scrolling
- expanded the writing task so it now includes Bulgarian-specific accommodation choices rather than only mechanical booking language

Day 28 QA status:
- Pass for current stage
- the obvious language, transliteration, and phrasing issues are fixed
- pedagogy is materially stronger because the lesson now separates accommodation types, room features, reception tasks, and problem-reporting clearly
- engagement is stronger because the lesson now teaches how Bulgarians actually travel and stay inside the country, not just hotel desk vocabulary
- still needs MP3 generation for the new per-item audio targets

Day 28 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day28.html
```

## Day 29 Status

Reference comparison:
- `day29.html`: increased from `5` to `83` `data-text` entries

Day 29 changes completed:
- corrected mixed-script transliteration corruption in `паспортен контрол`, `изгубен багаж`, `Регистрацията отваря`, `Последно повикване`, `обменно бюро`, and other airport rows
- corrected the vocabulary row `колички за багаж` to the more standard singular headword `количка за багаж`
- added a new scene-setting introduction before Section 1 so the lesson begins with Bulgarian air-travel context instead of lists
- expanded the intro and Bulgaria-specific framing so the lesson now includes Sofia, Varna, Burgas, Plovdiv, and a practical Schengen vs non-Schengen travel explanation
- rebuilt the airport vocabulary table with per-item audio
- rebuilt the check-in and boarding section with per-item audio and extra practical travel questions
- rebuilt the delays-and-problems section with cleaner Bulgarian and per-item audio
- expanded the Bulgarian-airport-reality section with Schengen-area, border-control, and passport-check vocabulary plus example phrases comparing Italy and the UK
- rebuilt the travel-essentials section with per-item audio
- replaced the old compact lost-luggage block with line-by-line dialogue audio
- expanded the writing task so it includes Bulgarian travel context, Schengen awareness, and not only word recall
- corrected stale navigation labels in the mobile selector and fixed the pager labels for Day 28 and Day 30
- added the stronger mobile table-card layout so per-word audio buttons stay visible on phones without horizontal scrolling

Day 29 QA status:
- Pass for current stage
- obvious transliteration corruption and weak phrasing are fixed
- pedagogy is materially stronger because the lesson now separates airport flow, airport problems, and wider Bulgaria travel logistics more clearly
- engagement is stronger because the lesson now frames airports as part of real travel into Bulgaria rather than as a raw glossary, including the coast airports and Schengen context
- still needs MP3 generation for the new per-item audio targets

Day 29 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day29.html
```

## Day 30 Status

Reference comparison:
- `day30.html`: increased from `5` to `93` `data-text` entries

Day 30 changes completed:
- added a proper scene-setting introduction before Section 1 so the lesson starts with Bulgarian shopping context rather than a vocabulary list
- rebuilt the clothing section with per-item audio for the core clothes, accessories, and fitting-room vocabulary
- rebuilt the sizes-and-fit section with denser per-item audio and added natural example phrases
- expanded the materials section into a richer style/materials section with `шевица` and stronger agreement examples
- added a new Bulgaria-specific shopping-reality section covering boutiques, second-hand shopping, seaside seasonality, and traditional clothing context
- rebuilt the purchase section with clearer shop language, returns language, and card-payment language
- replaced the compact jacket dialogue with a line-by-line Sofia shopping dialogue
- expanded the writing task so it includes cultural context and Bulgarian shopping reality, not only translation prompts
- fixed the mobile lesson selector to include the current A2 lesson set
- applied the stronger mobile table-card layout and automatic table header labels for phone layouts
- corrected stale pager labels for Day 29 and Day 31

Day 30 QA status:
- Pass for current stage
- language and teaching value are materially stronger than the original sparse version
- engagement is stronger because the lesson now connects clothes shopping to Bulgarian life, seasons, and traditional motifs
- mobile behavior is stronger because the vocab and recap tables now stack into labelled cards
- still needs MP3 generation for the new per-item audio targets

Day 30 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day30.html
```

## Day 31 Status

Reference comparison:
- `day31.html`: increased from `4` to `67` `data-text` entries

Day 31 changes completed:
- added a proper scene-setting introduction before Section 1 so the lesson starts with cultural framing rather than exam notes alone
- added new audio coverage for the introduction, timeline summary, geography, Orthodox heritage, and food culture sections
- corrected outdated time-sensitive wording so the page no longer says Bulgaria is still expected to join Schengen
- corrected the Day 31 currency row from `Лев (BGN)` to `Евро (EUR)` and added the actual euro adoption date of 1 January 2026
- corrected the national symbols section so the anthem and currency audio/wording no longer use broken quoted attributes or stale euro-adoption phrasing
- replaced the weak grouped audio coverage with per-item playback for named items including national symbols, holidays, famous Bulgarians, major traditions, geography names, monasteries, and food terms
- cleaned mixed-script and typography issues in the customs section, including `нестинари` and `мартеница`
- corrected the geography table spelling for `Златни пясъци`
- replaced several weak or unreliable entries in the famous-Bulgarians section with stronger, more credible examples
- applied the stronger mobile table-card layout and automatic table header labels for phone layouts
- corrected stale pager labels for Day 30 and Day 32

Day 31 QA status:
- Pass for current stage
- credibility is stronger because the outdated and broken facts are removed
- audio usefulness is materially stronger because learners can now play individual names instead of relying on broad summary clips
- engagement remains strong because this lesson already had rich substance, and the new intro frames it better
- mobile behavior is materially stronger because the large exam tables now stack into labelled cards
- still needs MP3 generation for the refreshed section audio

Day 31 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day31.html
```

## Maintenance Updates

- corrected `day56.html` so the euro debate no longer asks whether Bulgaria should adopt the euro in the future
- rewrote the Day 56 debate around the post-`1 January 2026` reality: easier travel, price-rounding concerns, oversight, and public trust after adoption
- corrected the Day 56 pager labels so they point to the real Day 55 and Day 57 lesson titles
- after this maintenance fix, the forward lesson sequence resumes with `day32.html`

## Day 32 Status

Reference comparison:
- `day32.html`: increased from `5` to `53` `data-text` entries

Day 32 changes completed:
- added a proper scene-setting introduction so the directions lesson starts with real Bulgarian city context instead of a flat glossary
- expanded the mobile day selector to the current A2 lesson range through Day 32
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- rebuilt the core directions, asking-for-directions, and imperative route tables with much denser per-item playback
- added a Bulgaria-specific city-landmarks section covering Sofia, Plovdiv, Varna, and Burgas so the lesson teaches how directions are actually given in Bulgarian cities
- added a new route-building phrases section with practical expressions like `след светофара`, `до спирката`, and `малко по-надолу`
- corrected the Sofia dialogue audio string so it no longer contains broken nested quotes and now uses `Не може да го изпуснете`
- corrected stale pager labels for Day 31 and Day 33

Day 32 QA status:
- Pass for current stage
- engagement is stronger because the page now teaches place-aware Bulgarian, not just isolated direction words
- mobile behavior is materially stronger because the tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has much denser per-item coverage
- still needs MP3 generation for the refreshed items

Day 32 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day32.html
```

## Day 33 Status

Reference comparison:
- `day33.html`: increased from `5` to `53` `data-text` entries

Day 33 changes completed:
- added a proper scene-setting introduction so the family lesson starts with Bulgarian social context rather than a flat glossary
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile day selector to the current A2 lesson range through Day 33
- rebuilt the extended-family, relationship-status, and life-events tables with much denser per-item playback
- corrected real language issues including `Много го липсва` to `Много ми липсва`, improved `много жива` to `много жизнена`, and fixed several weak romanisation lines
- improved the relationship-status table so the masculine and feminine forms are clearer and more teachable
- corrected stale pager labels for Day 32 and Day 34

Day 33 QA status:
- Pass for current stage
- credibility is stronger because the dialogue now uses natural Bulgarian in sensitive family/grief contexts
- engagement is stronger because the lesson now frames family as a real cultural theme, not just a lexical list
- mobile behavior is materially stronger because the tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has much denser per-item coverage
- still needs MP3 generation for the refreshed items

Day 33 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day33.html
```

## Day 34 Status

Reference comparison:
- `day34.html`: increased from `6` to `52` `data-text` entries

Day 34 changes completed:
- added a proper scene-setting introduction so the lesson starts with real Bulgarian discussion culture rather than an abstract phrase list
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile day selector to the current A2 lesson range through Day 34
- rebuilt the expressing-opinions, agreeing, disagreeing, asking-for-opinions, and connector tables with dense per-item playback
- corrected stale pager labels for Day 33 and Day 35
- added automatic mobile table header labels for the lesson tables and recap

Day 34 QA status:
- Pass for current stage
- engagement is stronger because the lesson now frames opinions inside real Bulgarian daily life
- mobile behavior is materially stronger because the tables now stack into labelled cards
- audio usefulness is materially stronger because almost every key Bulgarian phrase on the page now has a play option
- still needs MP3 generation for the refreshed items

Day 34 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day34.html
```

## Day 35 Status

Reference comparison:
- `day35.html`: increased from `4` to `54` `data-text` entries

Day 35 changes completed:
- added a proper scene-setting introduction so the checkpoint now frames why Day 35 matters in real Bulgarian life, not just as a test page
- corrected the grammar typo `через` to `през` in the seasons reference row
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile day selector to the full A2 range through Day 35
- rebuilt the A2 grammar reference with per-item playback on the key grammar labels and example sentences
- rebuilt the vocabulary self-check table so every major topic row now has its own Bulgarian audio support
- rewrote the citizenship-exam guide to be safer and more accurate, focusing on preparation rather than overconfident process claims that may change
- added an explicit note that the official public sample tests are fully in Bulgarian, so learners should not expect English prompts in the real exam
- added a second 20-question Bulgarian-only mock so Day 35 now trains learners inside Bulgarian exam wording, not only English-led revision
- corrected the Day 35 quiz header so it now reflects the real pass target of `12/20`, not the stale `6+` text
- corrected stale pager labels on Day 35 and fixed the stale previous-page label on `day36.html`

Day 35 QA status:
- Pass for current stage
- accuracy is stronger because the page no longer gives brittle exam-process specifics as if they were permanent facts
- accuracy is stronger because the page now reflects the official public sample-test reality: Bulgarian-only test content
- pedagogy is stronger because the checkpoint now behaves like a revision hub rather than a summary sheet
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the checkpoint now has dense support across grammar, topic recaps, and exam-orientation language
- still needs MP3 generation for the refreshed items

Day 35 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day35.html
```

## Day 36 Status

Reference comparison:
- `day36.html`: increased from `5` to `85` `data-text` entries

Day 36 changes completed:
- added a proper scene-setting introduction so the first B1 lesson starts with Bulgarian memory and storytelling context rather than a bare grammar jump
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile day selector to include the full A2 range and the start of B1
- corrected a real teaching risk by removing the misleading `гледех` model and rebuilding the core imperfect explanation around reliable high-frequency patterns
- rebuilt the core verb-pattern, high-frequency verb, irregular verb, and imperfect-vs-aorist tables with dense per-item playback
- added a new memory-phrases section so learners can start telling stories, not just reciting endings
- expanded the dialogue support with line-level audio in addition to the summary clip
- corrected small QA issues including a bad romanisation line and a weak duplicate quiz distractor
- added the mobile table-header labelling script so the stacked-card layout works correctly on phones

Day 36 QA status:
- Pass for current stage
- accuracy is materially stronger because the lesson no longer teaches a misleading core model form
- pedagogy is materially stronger because the lesson now teaches the imperfect as a meaning system, not just a chart
- engagement is stronger because the lesson is framed through Bulgarian memory, family stories, and lived past experience
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has dense support across patterns, examples, and dialogue lines
- still needs MP3 generation for the refreshed items

Day 36 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day36.html
```

## Day 37 Status

Reference comparison:
- `day37.html`: increased from `5` to `48` `data-text` entries

Day 37 changes completed:
- added a proper scene-setting introduction so the lesson frames reported speech through real Bulgarian life: media, landlords, doctors, neighbours, and family messages
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile selector to include the full A2 range and the early B1 lessons
- corrected the teaching emphasis around tense backshift so the lesson no longer presents an over-rigid “never changes” rule
- rebuilt the statements, reporting-verbs, indirect-questions, and reported-commands tables with denser per-item playback
- added stronger dialogue support with line-level audio
- added a Bulgarian-usage note connecting reported speech to real media and everyday communication
- corrected stale pager labels and cleaned the quiz header wording
- added the mobile table-header labelling script so the stacked-card layout works correctly on phones

Day 37 QA status:
- Pass for current stage
- accuracy is materially stronger because the lesson now teaches reported speech as practical Bulgarian usage rather than as an over-absolute contrast with English
- pedagogy is stronger because the key patterns are clearer and better supported with examples and audio
- engagement is stronger because the lesson is framed through real social and informational contexts in Bulgaria
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has denser support across the key structures
- still needs MP3 generation for the refreshed items

Day 37 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day37.html
```

## Day 38 Status

Reference comparison:
- `day38.html`: increased from `5` to `50` `data-text` entries

Day 38 changes completed:
- added a proper scene-setting introduction so the lesson frames conditionals and wishes through real Bulgarian hopes, regrets, migration talk, housing talk, and alternative-life conversations
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile selector to include the full A2 range and the early B1 lessons
- rebuilt the real-conditionals, hypothetical-conditionals, wishes, and regret sections with denser per-item playback
- corrected several language-quality issues in the dialogue and examples, including the unnatural `не сме изселили се` phrasing
- added stronger line-level dialogue audio
- added a Bulgarian-context engagement note about how often conditionals are used in real conversations about life choices and opportunity
- corrected stale pager labels and cleaned the quiz header wording
- added the mobile table-header labelling script so the stacked-card layout works correctly on phones

Day 38 QA status:
- Pass for current stage
- accuracy is stronger because the lesson examples and dialogue are more natural Bulgarian
- pedagogy is stronger because the key conditional and wish patterns are clearer and better supported with audio
- engagement is stronger because the lesson is framed through realistic Bulgarian hopes, regrets, housing, and migration talk
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has denser support across the main structures
- still needs MP3 generation for the refreshed items

Day 38 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day38.html
```

## Day 39 Status

Reference comparison:
- `day39.html`: increased from `4` to `53` `data-text` entries

Day 39 changes completed:
- added a proper scene-setting introduction so the lesson frames comparison through real Bulgarian talk about cities, salaries, rents, regional life, and quality of life
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile selector to include the full A2 range and the early B1 lessons
- rebuilt the review, comparison, superlative, and progressive-comparison sections with denser per-item playback
- corrected real language issues including `Кой е най-дългият река` to `Коя е най-дългата река`
- cleaned the dialogue audio summary so it no longer contains English leakage or broken phrasing
- added stronger line-level dialogue audio
- added a Bulgarian-context engagement note about how common comparisons are in everyday conversations about cities, prices, and life choices
- corrected stale pager labels and cleaned the quiz header wording
- removed a stray Latin-script `Sofia` from the quiz
- added the mobile table-header labelling script so the stacked-card layout works correctly on phones

Day 39 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer teaches broken agreement in the superlative example
- pedagogy is stronger because the comparison structures are now taught through fuller patterns and examples
- engagement is stronger because the lesson is framed through real Bulgarian comparison talk rather than abstract grammar alone
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has dense support across the main structures
- still needs MP3 generation for the refreshed items

Day 39 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day39.html
```

## Day 40 Status

Reference comparison:
- `day40.html`: increased from `4` to `54` `data-text` entries

Day 40 changes completed:
- added a proper scene-setting introduction so the lesson starts with real Bulgarian signs, estate adverts, museums, heritage descriptions, and public notices instead of jumping straight into abstract grammar
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile selector to include the full A2 range and early B1 lessons through Day 40
- rebuilt the `се`-passive section with denser per-item playback and more realistic Bulgarian examples drawn from daily life
- rebuilt the full passive section around safer, example-led participle teaching instead of overclaiming a perfectly mechanical rule
- fixed the broken Section 3 paragraph class and rebuilt the `от` agent section with denser per-item audio
- rebuilt the fixed passive expressions section so it now covers estate language, signs, museums, and news language
- corrected the Boyana Church dialogue for Bulgarian naturalness and credibility, including the broken mixed-script romanisation and the ungrammatical summary audio line
- added line-level dialogue audio, corrected stale pager labels, and added the mobile table-header labelling script

Day 40 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer teaches broken or mixed-script Bulgarian in the heritage dialogue
- pedagogy is stronger because the lesson now separates the everyday `се`-passive from the more formal participle passive with better examples
- engagement is stronger because the grammar is framed through real Bulgarian reading contexts rather than abstract tables alone
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has dense support across signs, structures, and dialogue lines
- still needs MP3 generation for the refreshed items

Day 40 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day40.html
```

## Day 41 Status

Reference comparison:
- `day41.html`: increased from `5` to `71` `data-text` entries

Day 41 changes completed:
- added a proper scene-setting introduction so the lesson frames media as a way to understand Bulgaria, not just as a glossary of newspaper words
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile selector to include the full A2 range and early B1 lessons through Day 41
- rebuilt the media vocabulary, news topics, reaction phrases, and news-perfect sections with dense per-item playback
- corrected the real language error `кризис` to `криза`
- removed subjective and brittle media claims, replacing them with safer source-aware framing around public broadcasters, commercial broadcasters, and the national news agency
- rebuilt the Bulgaria media section around BNT, BNR, Horizont, BTA, bTV, Nova, and Dnevnik, with a media-literacy note about following sources rather than headlines
- corrected the dialogue and romanisation quality, added line-level dialogue audio, and corrected stale pager labels
- added the mobile table-header labelling script so the stacked-card layout works correctly on phones

Day 41 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer teaches `кризис`, broken romanisation, or shaky subjective broadcaster claims
- pedagogy is stronger because the lesson now teaches how to talk about news, cite sources, and understand the news-perfect more clearly
- engagement is stronger because the topic is framed through real Bulgarian media use and media literacy rather than a flat list of nouns
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has dense support across vocabulary, analysis phrases, outlets, and dialogue lines
- still needs MP3 generation for the refreshed items

Day 41 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day41.html
```

## Day 42 Status

Reference comparison:
- `day42.html`: increased from `5` to `41` `data-text` entries

Day 42 changes completed:
- added a proper scene-setting introduction so the lesson frames idioms as a window into Bulgarian humour, emotion, and folk mentality rather than as a disconnected phrase list
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile selector to include the full A2 range and early B1 lessons through Day 42
- rebuilt the body-idiom, common-idiom, proverb, and set-expression sections with denser per-item playback
- removed several weak or dubious items instead of teaching them as if they were high-confidence everyday idioms
- corrected the proverb spelling from `Без труд, нема плод` to the standard `Без труд няма плод`
- corrected weak dialogue phrasing, fixed romanisation issues, and rebuilt the conversation around cleaner natural Bulgarian
- added line-level dialogue audio, corrected stale pager labels, and added the mobile table-header labelling script

Day 42 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer teaches several shaky idioms as if they were core standard expressions
- pedagogy is stronger because the lesson now distinguishes between useful everyday idioms, proverbs, and set reaction phrases more clearly
- engagement is stronger because the lesson now explains what idioms reveal about Bulgarian culture and folk imagery
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has dense support across idioms, proverbs, and dialogue lines
- still needs MP3 generation for the refreshed items

Day 42 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day42.html
```

## Day 43 Status

Reference comparison:
- `day43.html`: increased from `4` to `34` `data-text` entries

Day 43 changes completed:
- added a proper scene-setting introduction so the lesson frames formal writing through real institutional, residence, work, and administrative use in Bulgaria
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile selector to include the full A2 range and early B1 lessons through Day 43
- rebuilt the register, greeting, sign-off, and formal-request sections with denser per-item playback
- corrected the model letter by removing broken mixed-script text and weak over-formality, including `Bulgarian счетоводно` and the damaged romanisation
- rebuilt the official-documents section around safer high-frequency bureaucracy vocabulary instead of a longer but weaker list
- corrected stale pager labels and added the mobile table-header labelling script

Day 43 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer teaches broken mixed-script Bulgarian or damaged romanisation in the model letter
- pedagogy is stronger because the lesson now focuses on the practical formulas a learner actually needs for offices, schools, and employers
- engagement is stronger because the page is framed around real-life Bulgarian bureaucracy and formal communication rather than abstract style theory
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has per-item support across the key formal phrases and document vocabulary
- still needs MP3 generation for the refreshed items

Day 43 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day43.html
```

## Day 44 Status

Reference comparison:
- `day44.html`: increased from `4` to `49` `data-text` entries

Day 44 changes completed:
- added a proper scene-setting introduction so the lesson frames education through real Bulgarian life: jobs, residence paperwork, family expectations, and qualifications
- replaced the weak mobile table treatment with the stronger labelled stacked-card layout for phone screens
- expanded the mobile selector to include the full A2 range and early B1 lessons through Day 44
- rebuilt the education-system, subject, academic-vocabulary, qualification, and education-phrases sections with denser per-item playback
- tightened the dialogue so it now uses cleaner, more natural Bulgarian and safer phrasing around recognition of foreign diplomas
- corrected stale pager labels and added the mobile table-header labelling script

Day 44 QA status:
- Pass for current stage
- accuracy is materially stronger because the dialogue no longer contains broken romanisation artifacts or awkward wording about recognition procedures
- pedagogy is stronger because the lesson now separates school structure, subjects, qualifications, and personal background language more clearly
- engagement is stronger because the page links education to real Bulgarian life and migration-related use cases
- mobile behavior is materially stronger because the main tables now stack into labelled cards
- audio usefulness is materially stronger because the lesson now has per-item support across core school and university vocabulary
- still needs MP3 generation for the refreshed items

Day 44 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day44.html
```

## Day 45 Status

Reference comparison:
- `day45.html`: increased from `4` to `44` `data-text` entries

Day 45 changes completed:
- added a stronger scene-setting introduction so the lesson explains why aspect matters in real Bulgarian life before the learner reaches the grammar tables
- replaced the old mobile horizontal-scroll fallback with the stronger labelled stacked-card table behavior for phones
- expanded the mobile selector through Day 45 and corrected the stale pager labels
- corrected the weak Section 2 prefix teaching, including the bad `ивам` row, and rebuilt the aspect-formation explanation around safer, clearer pair examples
- added much denser per-item audio across the core contrast section, pair-formation section, tense-usage section, essential pair list, and dialogue lines
- cleaned broken romanisation artifacts in the dialogue and corrected the writing-task typo `одно imperfective`
- added the mobile table-header labelling script so stacked cards retain their headers on small screens

Day 45 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer contains the broken `ивам` row, damaged romanisation, or stale pager labels
- pedagogy is stronger because the page now teaches aspect through result, completion, and deadline logic instead of sparse abstract tables
- engagement is stronger because the new intro frames aspect through work, contracts, tasks, and everyday Bulgarian situations
- mobile behavior is materially stronger because the main tables now stack into labelled cards instead of relying on horizontal scrolling
- audio usefulness is materially stronger because the lesson now has dense support across the core pairs, tense contrasts, and dialogue lines
- still needs MP3 generation for the refreshed items

Day 45 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day45.html
```

## Day 46 Status

Reference comparison:
- `day46.html`: increased from `5` to `30` `data-text` entries

Day 46 changes completed:
- added a stronger scene-setting introduction so the lesson starts with why relative clauses matter in real Bulgarian speech, not just a grammar label
- replaced the old mobile horizontal-scroll fallback with the stronger labelled stacked-card table behavior for phones
- expanded the mobile selector through Day 46 and corrected the stale pager labels to Day 45 and Day 47
- added much denser per-item audio across the core pronoun forms, key relative-clause patterns, preposition patterns, possession forms with `чийто`, and dialogue phrases
- corrected mixed-script and romanisation issues, including the broken `говориш` and the damaged `poznavam` line
- improved the answer key so it teaches the more natural Bulgarian sentence order instead of a clumsier learner-style model
- added the mobile table-header labelling script so stacked cards retain their headers on small screens

Day 46 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer contains the broken mixed-script romanisation artifacts
- pedagogy is stronger because the lesson now separates form, agreement, preposition use, possession, and sentence order more clearly
- engagement is stronger because the new intro links relative clauses to work, property, school, news, and everyday descriptions in Bulgaria
- mobile behavior is materially stronger because the main tables now stack into labelled cards instead of relying on horizontal scrolling
- audio usefulness is materially stronger because the lesson now has per-item support across the key forms and patterns instead of only a handful of grouped clips
- still needs MP3 generation for the refreshed items

Day 46 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day46.html
```

## Day 47 Status

Reference comparison:
- `day47.html`: increased from `4` to `94` `data-text` entries

Day 47 changes completed:
- added a stronger scene-setting introduction so the lesson starts with the real housing decisions learners face in Bulgaria, not just a word list
- replaced the old mobile horizontal-scroll fallback with the stronger labelled stacked-card table behavior for phones
- expanded the mobile selector through Day 47 and corrected the stale pager labels to Day 46 and Day 48
- added dense per-item audio across housing types, renting terms, buying vocabulary, legal/process language, property-description phrases, renovation language, DIY tasks, complaint phrases, and dialogue lines
- corrected multiple mixed-script and damaged romanisation issues in the renting table, property section, and Sofia flat-hunting dialogue
- improved a few weaker teaching points, including the parking phrase and the deposit complaint line
- added Bulgaria-specific housing context around older panel blocks versus newer residential complexes
- expanded the lesson beyond renting with full new sections on buying a home in Bulgaria, renovation language, and DIY / practical home tasks
- added current market framing based on official Bulgarian statistics, including the strong year-on-year rise in housing prices in Q1 2025
- added a new legal/process section covering cadastre, property register, tax valuation, local acquisition tax, registration, and checks for encumbrances
- added the mobile table-header labelling script so stacked cards retain their headers on small screens

Day 47 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer contains the corrupted mixed-script romanisation strings in key housing vocabulary
- pedagogy is stronger because the lesson now separates housing types, rental terms, buying language, legal/process language, property features, renovation language, and complaint language more clearly
- engagement is stronger because the page now teaches Bulgaria-specific housing realities, market context, renovation realities, and the real buying process rather than generic property vocabulary
- mobile behavior is materially stronger because the main tables now stack into labelled cards instead of relying on horizontal scrolling
- audio usefulness is materially stronger because the lesson now has broad per-item support across the major property, buying, renovation, DIY, and dialogue language instead of leaving large sections unvoiced
- still needs MP3 generation for the refreshed items

Day 47 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day47.html
```

## Day 48 Status

Reference comparison:
- `day48.html`: increased from `5` to `58` `data-text` entries

Day 48 changes completed:
- added a stronger scene-setting introduction so the lesson starts with why business Bulgarian matters in real Bulgarian work life, not just a glossary
- expanded the meeting-language section with more per-item playback and corrected the broken romanisation in `Предлагам да преминем към...` and `Договорихме се, че...`
- rebuilt the negotiation section with individual audio for proposing, refusing, counter-offers, conditions, internal consultation, and clarification language
- rebuilt the presentation section with individual audio for openings, structure, transitions, evidence, conclusions, and question prompts, while correcting the damaged romanisation strings
- expanded the business-culture section with Bulgaria-specific context around hierarchy, relationship-building, indirect refusal, coffee meetings, and decision-making, plus new per-item audio
- rebuilt the dialogue support with corrected romanisation and line-level playback for the key business phrases instead of relying on a short grouped clip
- replaced the stale pager labels with Day 47 and Day 49 titles and added the mobile table-header labelling script so the stacked card layout works properly on phones

Day 48 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer contains the broken mixed-script romanisation in the meeting, presentation, and dialogue sections
- pedagogy is stronger because the lesson now separates meetings, negotiations, presentations, business culture, and realistic dialogue more clearly
- engagement is stronger because the page now explains the relationship-driven side of Bulgarian business culture instead of staying at the level of translated office phrases
- mobile behavior is materially stronger because the main tables now label stacked cells properly on phones
- audio usefulness is materially stronger because the lesson now has per-item support across the main professional phrases and dialogue lines instead of relying on a handful of grouped clips
- still needs MP3 generation for the refreshed items

Day 48 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day48.html
```

## Day 49 Status

Reference comparison:
- `day49.html`: increased from `5` to `77` `data-text` entries

Day 49 changes completed:
- added a stronger scene-setting introduction so the lesson begins with the reality of Bulgarian admin life, not just vocabulary tables
- corrected the outdated citizenship-exam guidance by replacing the old language-plus-integration framing with the current official Institute of Education language-test framing
- rebuilt the immigration vocabulary, institutions, pathway, office-language, and document-checklist sections with dense per-item playback
- replaced the wrong institution attribution by removing the claim that the State Agency for Bulgarians Abroad runs the exam and instead pointing learners to the current official Institute of Education information
- tightened the legal/process section so it stays useful without pretending every route follows one simple identical timeline
- rebuilt the residence-office dialogue with cleaner Bulgarian, corrected romanisation, and line-level playback
- replaced the old mobile horizontal-scroll fallback with labelled stacked-card behavior and added the mobile table-header labelling script
- corrected the stale pager labels to Day 48 and Day 50 and fixed the broken quiz option containing mixed-script garbage
- added a dedicated British-nationals section explaining the practical difference before and after `1 January 2021`
- added a much deeper visa-and-residence section covering `Visa D`, work/study/family routes, long-term residence, permanent residence, and the need for a proper legal basis
- added a direct official-sources section inside the lesson and linked GOV.UK, MVR, MFA, Ministry of Justice, and Institute of Education pages
- expanded the writing and recap sections so they now reflect the stronger British-national and visa/residence content

Day 49 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer teaches the outdated combined-exam/institution wording
- pedagogy is stronger because the lesson now separates vocabulary, institutions, route overview, office language, documents, and dialogue more clearly
- engagement is stronger because the page now explains how Bulgarian bureaucracy actually feels, where learners get stuck, and how the British-national position changed after Brexit
- mobile behavior is materially stronger because the main tables now stack into labelled cards instead of relying on horizontal scrolling
- audio usefulness is materially stronger because the lesson now has broad per-item support across the major admin, British-national, visa, and route phrases instead of only grouped clips
- still needs MP3 generation for the refreshed items

Day 49 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day49.html
```

## Overnight Handover Note

User direction for next session:
- do not move forward with Day 49 as-is
- Day 49 needs a much deeper second pass
- existing useful content should be kept and expanded, not reduced
- almost every Bulgarian word or phrase should have its own audio support
- the lesson should become a major practical module for immigration and bureaucracy in Bulgaria
- add a dedicated Britain / British nationals section
- explain the difference before and after `1 January 2021`
- explain visas in much more detail
- explain the route to residence, long-term residence, permanent residence, and citizenship in much more detail
- include clearly marked official source links
- search for additional official immigration information before editing

New handover file created:
- `DAY49_EXPANSION_BRIEF.md`

Important next-session rule:
- reopen and verify the official immigration/citizenship sources before continuing Day 49 because this is legally and administratively time-sensitive

Partial work warning:
- `day50.html` has partial local edits from this session and should be treated as in-progress, not complete
- before continuing Day 50, verify its local state carefully

## Day 50 Status

Reference comparison:
- `day50.html`: increased from `4` to `29` `data-text` entries

Day 50 changes completed:
- finished the partial local edit state and converted the page into a more guided reading-skills lesson rather than three unsupported text blocks
- added a stronger scene-setting introduction so the module frames B1 reading as work with register, not just translation
- expanded the mobile selector through Day 51 and corrected the stale pager labels to Day 49 and Day 51
- added dense phrase-level playback to the key vocabulary from the news text, literary extract, and official-style notice
- replaced the brittle fake-specific official notice with a clearly marked practice notice in the style of Bulgarian administrative language
- synced the comprehension and writing sections to the new practice notice
- added the mobile table-header labelling script so the stacked-card table layout works properly on phones

Day 50 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer presents a fake-specific service notice as if it were live public information
- pedagogy is stronger because the lesson now teaches reading strategy, register recognition, and phrase-level extraction more explicitly
- engagement is stronger because the module feels more guided and less like three raw text dumps
- mobile behavior is materially stronger because the tables now stack into labelled cards instead of relying on horizontal scrolling
- audio usefulness is materially stronger because the lesson now includes phrase-level support across the three text registers instead of only four long clips
- still needs MP3 generation for the refreshed items

Day 50 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day50.html
```

## Day 51 Status

Reference comparison:
- `day51.html`: increased from `5` to `44` `data-text` entries

Day 51 changes completed:
- added a stronger scene-setting introduction so the lesson frames fluency as managing real conversation, not just speaking faster
- expanded the mobile selector through Day 52 and corrected the stale pager labels to Day 50 and Day 52
- rebuilt the spoken-particle, filler-word, conversation-strategy, photo-description, and dialogue sections with much denser per-item playback
- corrected broken or mixed-script romanisation in the filler section, conversation-strategy table, and extended dialogue
- improved the balancing-opinions line to a more natural spoken Bulgarian model
- added the mobile table-header labelling script so the stacked-card table layout works properly on phones

Day 51 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer contains broken romanisation artifacts in core fluency material
- pedagogy is stronger because the lesson now separates particles, fillers, recovery phrases, exam description phrases, and real dialogue patterns more clearly
- engagement is stronger because the module now feels more like real spoken Bulgarian and less like a short reference sheet
- mobile behavior is materially stronger because the tables now stack into labelled cards instead of relying on horizontal scrolling
- audio usefulness is materially stronger because the lesson now has broad phrase-level support across the key spoken-Bulgarian tools instead of only a few grouped clips
- still needs MP3 generation for the refreshed items

Day 51 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day51.html
```

## Day 52 Status

Reference comparison:
- `day52.html`: increased from `4` to `33` `data-text` entries

Day 52 changes completed:
- added a stronger scene-setting introduction so the history lesson starts with why Bulgarian history matters in daily life, identity, travel, and citizenship preparation
- expanded the mobile selector through Day 53 and corrected stale selector text such as `Day 20: Recipes`
- added per-item audio support for major historical names and places, including `траки`, `Одриско царство`, `Сердика`, `Плиска`, `Преслав`, `Хан Аспарух`, `Борис I`, `Цар Симеон`, and `Търново`
- added per-item audio support for National Revival and liberation-era references, including `Паисий Хилендарски`, `Българска екзархия`, `Априлско въстание`, `Баташко клане`, `Васил Левски`, `Христо Ботев`, and `Шипка`
- corrected the modern-history section so it now reflects the real post-2024 and post-2026 timeline instead of stale future-tense Schengen and euro wording
- added per-item audio support for the key modern dates `3 март 1878`, `9 септември 1944`, `10 ноември 1989`, `1 януари 2007`, `31 март 2024`, and `1 януари 2026`
- added per-item audio support for key cultural and political figures, including `Иван Асен II`, `Паисий Хилендарски`, `Васил Левски`, `Христо Ботев`, `Иван Вазов`, and `Тодор Живков`
- corrected mixed-script phonetic text in the modern grouped audio and added the mobile table-header labelling script so stacked cards behave properly on phones
- added the missing phrase-grid styling so Bulgarian and English labels in the history phrase cards display with proper visual spacing instead of collapsing together
- corrected stale pager labels to Day 51 and Day 53

Day 52 QA status:
- Pass for current stage
- accuracy is materially stronger because the page now reflects Bulgaria's real EU, Schengen, and euro timeline and warns learners that older materials may still describe these as future changes
- pedagogy is stronger because the lesson now teaches history through names, places, dates, and figures that learners actually encounter in Bulgarian life
- engagement is stronger because the page now opens with real context instead of dropping straight into a chronology
- mobile behavior is materially stronger because the tables now stack into labelled cards instead of relying on horizontal scrolling
- audio usefulness is materially stronger because the lesson now has individual playback for the core people, places, and dates rather than only a few broad grouped clips
- still needs MP3 generation for the refreshed items

Day 52 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day52.html
```

## Day 53 Status

Reference comparison:
- `day53.html`: increased from `4` to `43` `data-text` entries

Day 53 changes completed:
- added a stronger scene-setting introduction so the grammar revision day starts with real Bulgarian usage contexts instead of reading like a compressed rules sheet
- corrected stale mobile selector text by changing `Day 20: Recipes` to `Day 20: Daily Routine`
- added missing phrase-card styling so the new Bulgarian and English grammar labels display clearly and consistently
- rebuilt the tense revision section with per-item audio for the major tense names
- expanded the aspect revision with per-item audio for core labels and signal phrases such as `несвършен вид`, `свършен вид`, `всеки ден`, and `ако прочета`
- expanded the passive section with per-item audio for high-frequency fixed expressions such as `говори се`, `продава се`, `търси се`, and `не се пуши`
- expanded the conditionals section with per-item audio for both real and hypothetical patterns
- expanded the reported-speech section with per-item audio for core markers and command structures including `че`, `дали`, `да дойда`, and `да не говоря`
- corrected the relative-clauses section by replacing the stale `Který system.` subtitle, fixing `чиити` to `чиито`, and adding per-item audio for the main pronoun forms
- expanded the comparison section with per-item audio for structures such as `по-стар`, `най-високият`, `толкова висок, колкото`, and `все по-скъпо`
- corrected the recap wording from `Che + clause` to `Че + clause`
- corrected stale pager labels to Day 52 and Day 54
- added the mobile table-header labelling script so stacked cards behave properly on phones

Day 53 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer contains the stale relative-clause typo and the possession form is now correct
- pedagogy is stronger because the revision now surfaces the high-value labels and trigger phrases learners actually need to recognise quickly
- engagement is stronger because the page now frames grammar as real Bulgarian usage rather than abstract terminology
- mobile behavior is materially stronger because the tables now support labelled stacked-card rendering on phones
- audio usefulness is materially stronger because the lesson now has broad phrase-level coverage instead of only four grouped clips
- still needs MP3 generation for the refreshed items

Day 53 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day53.html
```

## Day 54 Status

Reference comparison:
- `day54.html`: increased from `5` to `59` `data-text` entries

Day 54 changes completed:
- added a stronger scene-setting introduction so the vocabulary revision day starts with real Bulgarian use cases instead of feeling like a flat glossary
- corrected stale mobile selector text by changing `Day 20: Recipes` to `Day 20: Daily Routine`
- added missing phrase-card styling so Bulgarian and English labels in the new revision cards display clearly
- rebuilt the essential-words section with per-item audio for the highest-value conversational items
- expanded the people-and-relationships section with per-item audio for key family and social vocabulary
- expanded the places-and-directions section with per-item audio for core navigation and city words
- expanded the time-expressions section with per-item audio for high-frequency time markers
- expanded the health section with per-item audio for the most useful illness and medical words
- corrected the money vocabulary from `лев / стотинка` to `евро / цент` and added a current-status note explaining that Bulgaria adopted the euro on `1 January 2026`
- expanded the food, shopping, work, formal-life, opinion, and idioms sections with dense phrase-level audio
- corrected the proverb from `Без труд нема плод` to `Без труд няма плод` in the main table, grouped audio, quiz, and recap
- corrected stale pager labels to Day 53 and Day 55
- added the mobile table-header labelling script so stacked cards behave properly on phones

Day 54 QA status:
- Pass for current stage
- accuracy is materially stronger because the page now reflects the euro era and no longer teaches the old proverb spelling
- pedagogy is stronger because the revision now isolates high-value items for active recall instead of leaving whole sections as silent tables
- engagement is stronger because the module now feels like a guided fluency drill rather than a raw list of words
- mobile behavior is materially stronger because the tables now support labelled stacked-card rendering on phones
- audio usefulness is materially stronger because most major vocabulary groups now have phrase-level playback instead of only five grouped clips
- still needs MP3 generation for the refreshed items

Day 54 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day54.html
```

## Day 55 Status

Reference comparison:
- `day55.html`: increased from `5` to `31` `data-text` entries

Day 55 changes completed:
- added a stronger scene-setting introduction so the lesson starts with practical Bulgarian uses for dates, deadlines, floors, forms, and event planning
- added missing phrase-card styling so the new Bulgarian and English labels display clearly
- corrected the larger ordinal form from `стоти` to `стотен`
- corrected the main ordinal grouped-audio phonetic string by removing mixed-script corruption
- corrected the date explanation so it no longer wrongly teaches that Bulgarian dates use the neuter ordinal plus a genitive month; the page now teaches the normal spoken pattern such as `пети юни` and `трети март`
- corrected damaged romanisation in the date phrases table
- added per-item audio for key ordinal labels and date expressions
- corrected the collective-numbers table by removing the broken `And двете / тримата` row and replacing it with a clearer `Both` row
- corrected damaged romanisation in the collective-numbers section and added per-item audio for the main collective forms
- corrected the counting-expressions section by fixing the damaged `хилядина` romanisation and replacing the outdated grouped example `стотина лева` with `стотина души`
- corrected mixed-script corruption in the dialogue romanisation and grouped dialogue audio
- added per-item audio for key dialogue phrases such as `двадесет и трети февруари`, `на третия етаж`, and `до петия февруари`
- corrected the recap so it now describes the date pattern more accurately
- added the mobile table-header labelling script so stacked cards behave properly on phones

Day 55 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer teaches the wrong date-grammar explanation and several damaged forms are now corrected
- pedagogy is stronger because the lesson now isolates the most useful ordinal, date, and counting patterns for active recall
- engagement is stronger because the module now frames numbers inside real deadlines, events, and official life rather than just listing forms
- mobile behavior is materially stronger because the tables now support labelled stacked-card rendering on phones
- audio usefulness is materially stronger because the lesson now has phrase-level coverage across ordinals, dates, collective numbers, counting expressions, and the dialogue instead of only five grouped clips
- still needs MP3 generation for the refreshed items

Day 55 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day55.html
```

## Day 56 Status

Reference comparison:
- `day56.html`: increased from `4` to `30` `data-text` entries

Day 56 changes completed:
- added a stronger scene-setting introduction so the debate lesson starts with real Bulgarian use cases such as interviews, oral exams, serious discussion, and formal tasks
- corrected stale mobile selector text by changing `Day 20: Recipes` to `Day 20: Daily Routine`
- added missing phrase-card styling so the new Bulgarian and English labels display clearly
- expanded the strong-opinion section with per-item audio for the main high-value opinion structures
- expanded the argument-connectors section with per-item audio for the most useful structuring phrases
- corrected damaged romanisation in the conceding section and expanded it with denser per-item audio
- corrected the debate-phrases table by replacing the too-colloquial `Тва е твърде опростено виждане.` with `Това е твърде опростено виждане.`
- corrected the euro dialogue from `спекула` to `спекулации` and cleaned the corresponding romanisation
- added per-item audio for high-value debate phrases and key euro-debate expressions such as `приемането на еврото`, `двойното обозначаване на цените`, `общественото доверие`, and `злоупотреби и спекулации`
- added the mobile table-header labelling script so stacked cards behave properly on phones

Day 56 QA status:
- Pass for current stage
- accuracy is materially stronger because the lesson now uses cleaner standard Bulgarian in the debate phrases and the euro dialogue no longer ends with the wrong noun form
- pedagogy is stronger because the core opinion, concession, and connector phrases now have much better phrase-level recall support
- engagement is stronger because the module now frames argument language as real Bulgarian public-life language, not abstract exam filler
- mobile behavior is materially stronger because the tables now support labelled stacked-card rendering on phones
- audio usefulness is materially stronger because the lesson now has broad phrase-level support instead of only four grouped clips
- still needs MP3 generation for the refreshed items

Day 56 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day56.html
```

## Day 57 Status

Reference comparison:
- `day57.html`: increased from `6` to `30` `data-text` entries

Day 57 changes completed:
- added a stronger scene-setting introduction so the complex-sentence lesson starts with real Bulgarian use cases in essays, oral exams, explanations, and connected speech
- corrected stale mobile selector text by changing `Day 20: Recipes` to `Day 20: Daily Routine`
- added missing phrase-card styling so the new Bulgarian and English labels display clearly
- expanded the purpose-clause section with per-item audio for the key `за да` structures
- corrected the result-clause section by fixing damaged romanisation and replacing the broken final example with the clearer `Спечели толкова много, че можа да се пенсионира рано`
- expanded the result-clause section with denser phrase-level audio
- expanded the concessive-clause section with per-item audio and corrected the grouped-audio transliteration for `езикът си заслужава`
- corrected the temporal-clause grouped-audio transliteration from `shcheom` to `shtom` and expanded the section with phrase-level audio
- corrected the complex-sentence grouped audio by improving punctuation and fixing damaged transliteration in `изяде вечерята`
- corrected multiple mixed-script and damaged romanisation issues in the dialogue block
- expanded the dialogue support with phrase-level audio for the most useful complex structures
- corrected stale pager labels to Day 56 and Day 58
- added the mobile table-header labelling script so stacked cards behave properly on phones

Day 57 QA status:
- Pass for current stage
- accuracy is materially stronger because the damaged romanisation and broken result-clause example are now corrected
- pedagogy is stronger because the main subordinate-clause patterns now have clear phrase-level recall support instead of relying only on grouped clips
- engagement is stronger because the module now frames complex clauses as living Bulgarian rather than abstract grammar theory
- mobile behavior is materially stronger because the tables now support labelled stacked-card rendering on phones
- audio usefulness is materially stronger because the lesson now has broad phrase-level support across purpose, result, concession, time, stacked clauses, and dialogue
- still needs MP3 generation for the refreshed items

Day 57 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day57.html
```

## Day 58 Status

Reference comparison:
- `day58.html`: increased from `4` to `40` `data-text` entries

Day 58 changes completed:
- added a stronger scene-setting introduction so the lesson starts with real Bulgarian health situations rather than going straight into a symptoms list
- corrected stale mobile selector text by changing `Day 20: Recipes` to `Day 20: Daily Routine`
- added missing phrase-card styling so the new Bulgarian and English labels display clearly
- expanded the symptoms section with per-item playback for the highest-value illness phrases
- expanded the body-parts section with per-item playback for the key pain-location vocabulary
- expanded the healthcare-system section with per-item playback for `личен лекар`, `специалист`, `направление`, `Бърза помощ`, and the other core institutional terms
- corrected the GP co-payment wording from the old lev amount to current euro-era wording: `1.48 euro` per GP visit, or `0.51 euro` for people who have reached retirement age
- corrected damaged language and romanisation in the doctor-phrases section, including `От кога имате оплаквания?`
- expanded the doctor-phrases section with per-item playback for appointments, symptoms, allergy, prescription, and follow-up phrases
- corrected the emergency section romanisation from `infakt` to `infarkt` and expanded it with denser per-item playback
- corrected mixed-script and damaged romanisation in the GP dialogue, including `Iztrapna mi...`, `zacherveno`, `vkashti`, `Piyte`, and `bolnichen`
- corrected stale pager labels to Day 57 and Day 59
- added the mobile table-header labelling script so stacked cards behave properly on phones

Day 58 QA status:
- Pass for current stage
- accuracy is materially stronger because the page now reflects the euro-era patient fee and the damaged medical romanisation has been corrected
- pedagogy is stronger because the lesson now isolates the phrases learners actually need under pressure instead of leaving large silent tables
- engagement is stronger because the page now frames health Bulgarian as real life knowledge for living in Bulgaria, not just survival vocabulary
- mobile behavior is materially stronger because the tables now support labelled stacked-card rendering on phones
- audio usefulness is materially stronger because the lesson now has phrase-level playback across symptoms, body parts, healthcare-system terms, doctor phrases, and emergency phrases instead of only four grouped clips
- still needs MP3 generation for the refreshed items

Day 58 source used:
- NHIF euro FAQ: `https://www.nhif.bg/bg/euro/answers/58159`

Day 58 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day58.html
```

## Day 59 Status

Reference comparison:
- `day59.html`: increased from `5` to `35` `data-text` entries

Day 59 changes completed:
- added stronger scene-setting material so the page now frames the oral exam as real-time communication rather than a rigid script
- removed overconfident wording that presented one exact named exam format as if it were universally fixed, and reframed the lesson as B1 oral-preparation training with a reminder to check the live institution-specific instructions
- corrected stale mobile selector text by changing `Day 20: Recipes` to `Day 20: Daily Routine`
- added missing phrase-card styling so the new Bulgarian and English labels display clearly
- expanded the self-introduction section with per-item audio for the main high-value opening phrases
- expanded the photo-description section with per-item audio for the core scene-description phrases
- corrected the market-scene model from `хората са пазаруват` to `хората пазаруват`
- expanded the discussion section with per-item audio for the main argument-building phrases
- expanded the roleplay section with per-item audio for the main scenario openings
- corrected the hotel roleplay grouped transliteration by removing the mixed-script corruption in `имейл`
- expanded the exam-day tips section with per-item audio for fillers, clarification phrases, full-answer starters, and the closing line
- corrected the writing-task answer from `запишa` to `запиша`
- corrected stale pager labels to Day 58 and Day 60
- added the mobile table-header labelling script so stacked cards behave properly on phones

Day 59 QA status:
- Pass for current stage
- accuracy is materially stronger because the page no longer overclaims a fixed official structure without a current primary source, and the damaged Bulgarian lines are corrected
- pedagogy is stronger because each oral-exam part now has reusable high-value starter phrases with individual playback
- engagement is stronger because the page now feels more like coached speaking preparation than a compressed exam memo
- mobile behavior is materially stronger because the tables now support labelled stacked-card rendering on phones
- audio usefulness is materially stronger because the lesson now has phrase-level playback across self-introduction, image description, discussion, roleplay, and performance-management language instead of only a handful of grouped clips
- still needs MP3 generation for the refreshed items

Day 59 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day59.html
```

## Day 60 Status

Reference comparison:
- `day60.html`: increased from `4` to `10` `data-text` entries

Day 60 changes completed:
- corrected stale mobile selector text by changing `Day 20: Recipes` to `Day 20: Daily Routine`
- added missing phrase-card styling so the new Bulgarian and English labels display clearly
- reframed the page more honestly as the course's own final B1-style mock instead of presenting it as a fixed named institutional exam
- added stronger scene-setting and test-taking guidance so the final page feels like a real end-of-course assessment, not just a quiz dump
- added per-item audio for high-value final-review phrases such as `Според мен`, `На първо място`, `С уважение`, `Разрешение за пребиваване`, `Боли ме гърлото`, and `Без труд няма плод`
- corrected the Day 60 quiz header from `score 6+` to `score 12+`
- corrected the proverb spelling from `Без труд нема плод` to `Без труд няма плод` in both the quiz review audio and the quiz answer option
- corrected the Day 29 recap row from `boarding pass` to `бордна карта`
- corrected the Day 42 recap row to the standard proverb form `Без труд няма плод`
- softened the Day 59 recap row so it no longer teaches a rigid `4-part exam structure` claim as if it were universally fixed
- softened the final graduation message so it no longer overclaims readiness for a specific named exam
- added the mobile table-header labelling script so the big recap table behaves better on phones

Day 60 QA status:
- Pass for current stage
- accuracy is materially stronger because stale labels, the wrong final pass threshold, the old proverb spelling, and a few brittle exam claims are now corrected
- pedagogy is stronger because the page now gives clearer end-of-course guidance and isolates a small set of high-value final-review phrases for audio practice
- engagement is stronger because the final page now reads like a real graduation checkpoint rather than only a multiple-choice screen
- mobile behavior is materially stronger because the recap table now supports labelled stacked-card rendering on phones
- audio usefulness is stronger because the final page now has per-phrase playback for the most reusable B1 review items instead of only four grouped clips
- still needs MP3 generation for the refreshed items

Day 60 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day60.html
```

## Day 17 Engagement Pass

Reference comparison:
- `day17.html`: increased from `84` to `85` `data-text` entries

Day 17 retroactive engagement changes completed:
- added a stronger scene-setting introduction so the lesson now explains why restaurants matter socially in Bulgaria rather than jumping straight into a vocabulary list
- added a Bulgarian restaurant-culture section covering `механа`, local dining habits, regional food differences, and iconic dishes such as `шопска салата`, `мусака`, `кебапчета`, `кюфтета`, `таратор`, and `баница`
- added a new grouped audio item for the Bulgarian restaurant-culture section
- corrected stale euro-era issues in the tipping guidance by replacing the old lev example with a euro example
- corrected the model dialogue total from `тридесет и два лева` to `шестнадесет евро и тридесет цента`
- corrected the corresponding dialogue transliteration and English translation so the three versions stay aligned

Day 17 retroactive QA status:
- Pass for current stage
- engagement is materially stronger because the page now teaches Bulgarian food culture and social habits, not just restaurant utility phrases
- accuracy is stronger because the stale lev-era restaurant examples are now corrected to the euro era
- audio usefulness is slightly stronger because the new cultural framing also has playback support
- still keeps the dense per-item vocabulary audio from the earlier rebuild

Day 17 next command:

```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day17.html
```

## Programme Reset: Full-Course Review Roadmap

Strategic decision:
- the retroactive pass should start from `day01.html`, not continue from the later A2 modules
- the whole course now needs a programme-managed review, not just page-by-page editing

Reason for the reset:
- users love the course's unusually wide vocabulary and phrase coverage
- the course must keep that strength
- but it must not feel like a phrase book or reference spreadsheet
- the new goal is for every module to be accurate, engaging, informative, entertaining, and pleasant to read
- the audience is highly motivated and often living in Bulgaria or planning to move there, so Bulgarian context matters

New programme files created:
- `COURSE_REVIEW_ROADMAP.md`
- `PROJECT_MANAGER_AGENT.md`
- `RESEARCH_AGENT.md`
- `FACT_CHECK_AGENT.md`

Workflow update completed:
- `DAY_UPGRADE_WORKFLOW.md` now includes research, engagement, quality, and fact-check stages
- the project now has a defined team flow: research -> engagement -> content rebuild -> QA -> factual review -> PM sign-off

Programme-level next steps:
1. start the retroactive engagement pass from `day01.html`
2. run research-led enrichment before editing
3. run a full factual sweep before sign-off on modules with real-world claims
4. keep updating `PROJECT_STATUS.md` and `PROJECT_INFO.html` as the controlling handover files

## Day 1 Engagement Pass

Completed:
- `day01.html`: increased from `75` to `76` `data-text` entries
- added a new scene-setting introduction that explains why Cyrillic matters in daily life in Bulgaria: signs, menus, pharmacies, stations, and official documents
- added a cultural note on `24 май` so the first lesson already connects the alphabet to Bulgarian identity and public life
- added a new grouped audio item, `Cyrillic in real Bulgarian life`, so the lesson opens with practical context as well as letters
- added a Day 1 mindset note so learners understand the goal is confidence and recognition before speed
- corrected stale Day 1 mobile-selector labels so the A2 entries now reflect the current lesson titles and level wording

Roadmap context:
- this is the first module updated under the new roadmap-driven retroactive pass from the start of the course
- the Day 1 standard is now: accurate, welcoming, context-rich, and still dense in word-level audio

Next step on the user side:
```bat
cd /d "C:\Users\Dj4be\Desktop\New Bulgarian"
venv\Scripts\python.exe generate_pro_audio.py --force day01.html
```

Next editing target:
- continue the retroactive roadmap pass with `day02.html`
