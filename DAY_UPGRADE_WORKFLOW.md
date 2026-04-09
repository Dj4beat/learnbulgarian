# One-Day Upgrade Workflow

Use this workflow when rebuilding lessons one day at a time.

Reference standard:
- `day16.html`

Programme planning:
- `COURSE_REVIEW_ROADMAP.md`
- `PROJECT_MANAGER_AGENT.md`
- `RESEARCH_AGENT.md`
- `FACT_CHECK_AGENT.md`

Additional review briefs:
- `QUALITY_CHECK_AGENT.md`
- `ENGAGEMENT_AGENT.md`

## Step 1: Audit The Day

Record:
- `data-text` count
- section structure
- vocabulary sections
- dialogues / reading sections
- exercises and quiz
- CEFR fit
- any Russian or non-Bulgarian contamination
- whether the lesson has a real scene-setting introduction before Section 1
- whether the lesson feels like a lesson or a glossary
- whether the page includes Bulgarian-specific context
- whether factual claims need verification

## Step 2: Run Research Pass

Review against:
- `RESEARCH_AGENT.md`

Gather:
- topic-specific Bulgaria context
- useful local facts
- memorable details
- practical contrasts with English-speaking contexts
- suggested places to enrich the lesson

## Step 3: Upgrade The Teaching Content

Add or improve:
- a strong intro that sets the scene for the topic before Section 1
- practical vocabulary coverage
- clearer explanations for English speakers
- more natural Bulgarian sample sentences
- better section pacing
- stronger recap value
- more engaging content so the page does not read like a bare word list
- Bulgarian-specific facts, habits, etiquette, or cultural details where relevant
- memorable topic-related examples that make the lesson feel alive

## Step 4: Upgrade Audio To Day 16 Standard

Aim for:
- individual audio on core vocabulary items
- audio on key example sentences
- grouped "play all" controls per section
- audio for dialogue highlights

Do not stop at 4-6 grouped buttons if the lesson is vocabulary-heavy.

## Step 5: Run QA Review

Review against:
- `QUALITY_CHECK_AGENT.md`
- `ENGAGEMENT_AGENT.md`
- `FACT_CHECK_AGENT.md`

Fix all critical language, pedagogy, or engagement issues before generating MP3 files.

## Step 6: Generate Audio

From `C:\Users\Dj4be\Desktop\New Bulgarian` run:

```bat
venv\Scripts\python.exe generate_pro_audio.py dayXX.html
```

## Step 7: Final Verification

Confirm:
- page loads
- audio buttons and stop buttons match
- generated files exist
- no broken references
- CEFR label is correct
- lesson feels engaging, not just exhaustive
- facts are verified or safely softened
- handover files are updated
