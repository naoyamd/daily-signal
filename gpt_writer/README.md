# GPT Scheduled Writer

This directory documents the ChatGPT scheduled-writer contract. The actual published artifact remains Hugo Markdown under `content/daily/`.

## Input

The writer consumes only the same-day curated artifact from `naoyamd/daily-signal-collector`:

- `gpt_handoff/curated/YYYY-MM-DD.json`
- schema: `daily-signal-curated/v1`
- status must be `ready`

The writer must not perform broad discovery. It may open the selected primary/supporting URLs only to re-check facts, dates, figures, and attribution before publication.

## Output

- `content/daily/YYYY-MM-DD-daily-signal.md`
- commit message: `content: publish GPT Daily Signal YYYY-MM-DD`

The Hugo front matter follows the existing Daily Signal convention:

- `title`
- `date`
- `draft: false`
- `description`
- `categories`
- `tags: ["デイリーダイジェスト"]`
- `generated_by`
- `model`
- `source_count`
- `generation_cost_usd: 0`

The body keeps the existing structure: opening overview, numbered items, explicit why-it-matters text, primary source metadata, and up to three additional HTTPS references. Important survey/report items may be longer and retain methodology, sample size, key metrics, comparisons, and caveats.

## Safety / idempotency

- Never overwrite an existing same-day article.
- Never publish when curated status is not `ready`.
- Never silently substitute a previous day's curated file.
- Never invent missing facts, dates, figures, or citations.
- Use anonymous, non-first-person editorial voice.
- Do not expose internal agent/persona names in public copy.

GitHub Pages deployment is already triggered by pushes to `main`; the writer does not modify the Hugo deployment workflow.

## Published receipt

After a successful article commit, the writer also records a small receipt in `naoyamd/daily-signal-collector` at `gpt_handoff/published/YYYY-MM-DD.json`. This gives later curator runs an explicit publication history without coupling them to Hugo internals.
