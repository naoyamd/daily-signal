# GPT Scheduled Writer

This directory documents the ChatGPT scheduled-writer contract. The public artifact remains Hugo Markdown under `content/daily/`.

The Writer must read this file, `scripts/editorial.py`, the repository `README.md`, and `naoyamd/daily-signal-collector/gpt_handoff/policy.yaml` before writing. The policy file is the canonical quality profile. The Writer is a renderer and final fact checker, not a second Scout or Curator.

## Input

The Writer consumes only the same-day curated artifact from `naoyamd/daily-signal-collector`:

- `gpt_handoff/curated/YYYY-MM-DD.json`
- schema: `daily-signal-curated/v1`
- status must be `ready`
- generated date must match Asia/Tokyo local date
- age at Writer start must satisfy `policy.yaml`

Never silently use a previous day's file. Never build an article from a blocked, partial-without-approval, malformed, or empty curated artifact.

The Writer follows `editorial_plan.ordered_ids`. It does not re-rank the story. It may remove an item only when final source inspection shows a material factual or attribution problem; any removal must be reported.

## Final verification, not discovery

Broad search is prohibited. Open only each adopted `primary_url` and the necessary `supporting_urls` to verify:

- publication date
- organization and product/model names
- numerical values and denominators
- whether a statement is an official fact, official claim, self-reported benchmark, survey result, independent analysis, or inference
- whether a supporting source actually adds evidence rather than repeating the same release

Use only claims whose `verification_status` is `verified` or `partially_verified`. A partially verified claim must retain an explicit limitation in public copy. Do not publish an `unverified` material claim.

Do not convert attributed claims into neutral fact. Use formulations such as “the company reports,” “the survey found,” or “the authors report” when the evidence is self-reported, sponsored, or not independently reproduced.

## Depth hierarchy

A flat list of equally short summaries is not acceptable. Use the Curator tier and the character budgets in `policy.yaml`:

- `lead`: deeper explanation of the mechanism, novelty, and implementation consequence
- `report`: preserve issuer, date, sample/method, 3–5 major figures, comparison where available, practical meaning, and caveats
- `standard`: enough factual detail to distinguish the item from a headline rewrite
- `wildcard`: concise fact plus a precise reason to keep watching

The opening overview should synthesize tensions across items rather than paraphrase every headline. Examples of useful tensions are model capability versus data readiness, automation versus verification, and open weights versus operational cost/licensing.

Preserve the selected item count unless source verification fails. Do not reduce 8–12 selected items to 3–5 merely to make drafting easier. Conversely, do not pad an evidence-poor day.

## Output

- `content/daily/YYYY-MM-DD-daily-signal.md`
- commit message: `content: publish GPT Daily Signal YYYY-MM-DD`

Use the existing Hugo front-matter convention:

- `title`
- `date`
- `draft: false`
- `description`
- `categories`
- `tags: ["デイリーダイジェスト"]`
- `generated_by: "ChatGPT Scheduled Writer"`
- `model`
- `source_count`
- `generation_cost_usd: 0`

For `model`, use the exact runtime identifier only when the task environment exposes it. Otherwise write `ChatGPT Scheduled Task`. Never assert a specific model name merely because it appeared in an old prompt or previous article.

The body keeps the established structure:

1. `## 今日のご案内 ☕✨`
2. numbered selected items in Curator order
3. explicit `**💡 注目しておきたい理由:**`
4. primary source metadata and up to three genuinely useful supporting references
5. `# 今日の紛れ枠` when wildcard items exist
6. final source-warning blockquote

Every numbered item must contain enough verified detail to reconstruct why it was selected. Do not use generic filler such as “今後が注目される” without naming the mechanism, dependency, risk, or decision affected.

## Two-phase preflight inside the task

Because this scheduled Writer currently commits Markdown directly rather than invoking the VPS deterministic publisher, it must behave as a two-phase operation:

### Phase 1: build and validate without writing

Construct the complete Markdown in memory, then check:

- same-day curated status is `ready`
- all material claims map to an allowed claim source
- all URLs are public HTTPS
- article order matches `editorial_plan.ordered_ids`
- each lead/report/standard/wildcard meets its required depth
- report methodology and caveats are preserved
- `source_count` equals the number of actually published selected plus wildcard items
- front matter is syntactically coherent and description is at most 240 characters
- no internal terms such as Scout, Curator, prompt, handoff, or agent persona appear in public prose
- no first-person editorial voice appears
- no missing date has been invented
- no same-day article already exists

### Phase 2: commit

Only after every preflight check passes may the Writer create the new article. Never overwrite or update an existing same-day article.

## Safety and idempotency

- Never overwrite an existing same-day article.
- Never publish when curated status is not `ready`.
- Never silently substitute a previous day's curated file.
- Never invent missing facts, dates, figures, citations, model identity, or source independence.
- Use anonymous, non-first-person editorial voice.
- Do not expose internal stage or persona names in public copy.
- Do not modify the Hugo deployment workflow.

GitHub Pages deployment is already triggered by pushes to `main`.

## Published receipt and index

After a successful article commit, write `naoyamd/daily-signal-collector/gpt_handoff/published/YYYY-MM-DD.json` with:

- `schema: daily-signal-published/v1`
- `published_at`
- `article_repository`
- `article_path`
- `article_commit`
- `curated_source`
- `published_item_ids`
- `event_keys`
- `primary_urls`
- `organizations`
- `tags`
- `title`

Then update `gpt_handoff/state/published-index.json`, retaining the compact history window defined in `policy.yaml`. This index is the primary duplicate-control input for later Curator runs; dated receipts remain the audit trail.

A receipt must only be written after the article commit succeeds. If the article commit succeeds but receipt/index maintenance fails, report `published_with_state_warning` with the exact failed state operation. Do not claim the article itself failed and do not retry by creating another article.
