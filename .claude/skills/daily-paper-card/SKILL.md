---
name: daily-paper-card
description: >-
  Generate the user's daily 5-minute paper card — a visual-first, bilingual (English-default /
  한국어-toggle) HTML card in their artifacts_paper archive: signal badges, a 4-bullet TL;DR
  (Motivation → Analysis → Method → Results), an intuition box, the paper's key figure with a 3-step
  summary, custom charts/diagrams each led by a one-sentence takeaway, one key table, 3 numbers, a
  takeaway and caveat, and the rating widget — then registers it in the
  archive (done.log + build_index.py). Also picks WHICH paper when asked (wishlist first, then a
  notability score: top venue, listed labs/authors, frontier-lab reports, hot on alphaXiv/HF/GitHub).
  Use this WHENEVER the user wants a paper turned into the daily card / 5-min summary ("오늘의 논문
  카드", "이 논문 5분 요약 카드로", "daily paper", an arXiv link + "카드 만들어줘"), wants to pick
  today's paper, or a scheduled morning paper-review session runs. Reads the paper faithfully via
  paper-reader or alphaXiv. Prefer this over an ad-hoc chat summary whenever the output belongs in
  the archive.
---

# Daily paper card (v2.1 · visual-first + guiding text)

Produce one `papers/<YYYY-MM-DD>-<slug>.html` in the user's paper archive. The card is a **5-minute
skim**: pictures carry the paper, and a few well-placed sentences (intuition, one lead per visual,
a 3-step summary) make them readable at a glance. Follow the template, the budgets, and the
archive registration steps exactly.

## Archive layout (operate on these — don't reinvent)
Default project dir: the root of this repository (if moved, locate by finding
`template.html` + `build_index.py` together). Key paths:
- `template.html` — the v2 card layout (`{{PLACEHOLDER}}`s; map in `references/card-fill.md`).
- `papers/<date>-<slug>.html` — cards. `papers/fig/<arxivId>/` — figure images (PNG or the arXiv SVG).
- `reviews/<arxivId>.html` — optional deep "Full Review" (index links it automatically).
- `done.log` — one arXiv id per line = already covered. **Check before writing; append after.**
- `wishlist.md` (user queue, first priority) · `mustread.md` · `sources.md` (selection signals, user-editable).
- `assets/` — style.css/app.js linked relatively (`../assets/...`); never inline styles or scripts.
- `build_index.py` — deterministic archive index rebuild. **Always run after adding a card.**
- Scripts in this skill: `scripts/paper_signals.py` (score candidates) · `scripts/check_card.py` (lint a card).

## Workflow

1. **Resolve the paper.**
   - Given an arXiv link/id or PDF → use it. If the id is in `done.log`, say so and ask before duplicating.
   - **The user's priority topics (2026-09-26)** — P1 *Small–Large Alignment*: compressed / distilled /
     small-pretrained models that match a large model on benchmarks but not in their output (logit)
     distribution, and methods that measure or close that gap (keywords: flips, KL/fidelity, on-policy
     distillation, closed-loop). P2 *Video & World Generation*: efficient video diffusion and world-model
     generation, autoregressive first (Self/Causal Forcing, few-step AR distillation, video KV cache,
     sparse/linear attention). Rotation 6:1 — `paper_signals.py --slot` prints today's slot (P1 / P2 / legacy).
   - Asked to pick → `wishlist.md` first: the top-most id not in `done.log` whose `[P1]`/`[P2]` tag
     matches the slot (legacy slot → skip the wishlist). If none, run **notability selection**: gather candidates (alphaXiv `discover_papers` with `prioritize: "popular"` and
     `"recency"` over the interest axes; Hugging Face `https://huggingface.co/api/daily_papers?limit=100`
     filtered by axis keywords), then score the unread ones from the archive root:
     ```bash
     python3 .claude/skills/daily-paper-card/scripts/paper_signals.py "ID:axVotes:axViews@Org A|Org B" ...
     ```
     (votes/views/orgs come from the alphaXiv result line). Rules live in `sources.md`: priority-topic
     keyword in title/abstract +3 (tags P1/P2), main-track venue +3 (+1 oral/spotlight), workshop +1,
     listed author/lab +3, frontier-lab report +3, hot +2 (+1 very hot). Prefer candidates tagged with
     today's slot; confirm the fit from the abstract. Pick the highest score ≥ 3; tie-break on an axis the last 2 cards didn't cover,
     then hotter, then newer. Only if nothing reaches 3, take the best and say so in the footer.

2. **Read it faithfully — no memory-based summaries.**
   - Local PDF or exact numbers matter: **paper-reader** skill. Hosted arXiv paper: alphaXiv
     `get_paper_content` (fullText) / `answer_pdf_queries`.
   - Figures: arXiv HTML (`https://arxiv.org/html/<ID>v1`). Images are `<img src=…png>` or
     `<object data=….svg>` — resolve relative to `https://arxiv.org/html/<ID>v1/` and use `curl -f`.
     Save 1–3 to `papers/fig/<ID>/` (the method overview first; a key result plot if it beats a
     custom chart). SVGs work directly in `<img>`.

3. **Fill `template.html` — visual-first + guiding text** (full map: `references/card-fill.md`):
   - **TL;DR = 4 labeled bullets, in this order:** Motivation → Analysis (the key observation) →
     Method (**bold core** + one-line intuition) → Results (numbers). ≤ 25 words each, Method ≤ 40.
   - **Visuals are the body:** paper figure(s) 1–3 · ≥ 1 custom chart or diagram (`figure.chart`
     bars / inline SVG) · 1 key table (≤ 6 rows) · 3 stat tiles. Captions 1–2 lines.
   - **Guiding text (required):** 💭 intuition box (2–3 sentences, an analogy) · one `p.vlead` above
     each visual (**bold point** + why) · `ol.steps.compact` 3-step summary after the paper figure ·
     💡 takeaway + ⚠️ caveat (1–2 sentences each). No long essays or v1 mechanism cards.
   - **Signal badges** in the hero show why the paper was picked (venue / lab / hot); the footer's
     "why picked" is one line and keeps `venue: <Conf YYYY>` for venue tabs (omit for preprints;
     write workshops as `Workshop @ Conf'YY` so they don't land in a main-conference tab).
   - Every reading string is an EN/KO pair (`t-en`/`t-ko`); numbers, names, ids, table cells and
     chart values are shared. Gloss acronyms on first use in both languages.

4. **Check, then register** — this is what makes it real:
   ```bash
   python3 .claude/skills/daily-paper-card/scripts/check_card.py papers/<file>.html   # must print OK
   echo <arxivId> >> done.log
   python3 build_index.py
   ```
   `check_card.py` enforces 350–600 English reading words (title, Korean, tables, chart labels
   excluded), the 4-bullet TL;DR order, the intuition box, ≥ 2 visual leads, ≥ 1 custom visual,
   EN/KO pairing, rating id, noindex. Then look at the
   render (headless Chrome screenshot at desktop and inside a 390 px iframe) for overflow/collisions.
   Tell the user the card path and a 2-line gist (headline claim + the caveat).

5. **Optional deep review**: `reviews/<arxivId>.html` (separate long form; unchanged by v2).

## Conventions that matter
- **Numbers must be real.** Stats, chart values and the table come from the paper's own text/tables.
  A value you *derive* (e.g. a ratio from a table) is labeled as computed, with its source.
- **Charts are honest:** bars start at 0, `--w = value / axis max`, one axis per chart, "ours" in the
  accent (`.bar.hl`, or `.bars.mono` when every bar is ours), baselines gray, every bar direct-labeled.
- **Faithful, not creative**: the look comes from `assets/`; don't restyle per card.
- **Keep `noindex`** and the `data-arxiv` rating section — app.js persists ratings per arXiv id.

## References
- `references/card-fill.md` — placeholder → content map, chart recipes, EN/KO rules.
