# Card fill guide — v2.1 template.html (visual-first + guiding text)

Fill every `{{PLACEHOLDER}}`, write to `papers/<YYYY-MM-DD>-<slug>.html` (slug = short kebab of the
method name), keep `../assets/` links, `noindex`, and the `#bar` + `.langtoggle` blocks. No inline
`<style>`/`<script>`; only data variables in `style="--w:…"` / `--x` / `--vw`.
Reference card: `papers/2026-09-26-freetoken.html`.

## Budgets (check_card.py enforces the hard ones)
| Element | Budget |
|---|---|
| English reading text (title, KO, tables, chart labels excluded) | **350–600 words** (hard); aim ~500 |
| TL;DR | 4 bullets: Motivation → Analysis → Method → Results (hard); ≤ 25 words each, Method ≤ 40 |
| 💭 Intuition box (`.intuit`) | 2–3 sentences, required (hard) |
| Visual leads (`p.vlead`) | one per visual section, ≥ 2 (hard): **bold point.** + one "why" clause |
| 3-step summary (`ol.steps.compact`) | after the paper figure: bold one-liner + ≤ 20-word detail each |
| Paper figures | 1–3, method overview first; caption 1–2 lines |
| Custom visuals | ≥ 1 (hard): `figure.chart` bars, split bars, or a small inline SVG diagram |
| Key table | 1, ≤ 6 rows |
| Stats | exactly 3 (`.stats.three`) |
| 💡 takeaway / ⚠️ caveat | 1–2 sentences each |
| Footer "why picked" | 1 line + `venue: …` when accepted |

## EN/KO rule
English primary, Korean toggle. Reading text goes in sibling pairs (`<p class="t-en">…</p><p class="t-ko">…</p>`,
inline → `<span>`). **Shared (never translate):** numbers, metrics, arXiv id + links, dates, author
names, table cells, chart values, figure images, method names. Gloss acronyms on first use in both
languages (e.g. "LRU (least-recently-used)", "LRU(가장 오래 안 쓴 것부터 버리는)").

## Hero
- `{{PAPER_TITLE}}` (shared) · `{{SUBTITLE_EN/KO}}` one-line hook (≤ 20 words).
- `{{TOPIC_EN/KO}}` chip — archive vocabulary, no leading emoji. **The first segment is load-bearing**:
  it picks the archive column and drives the daily slot (`paper_signals.py --slot`).
  - P1 cards: `Small–Large Alignment · <sub>` (e.g. "Small–Large Alignment · On-Policy Distillation")
  - P2 cards: `Video & World Generation · <sub>` (e.g. "Video & World Generation · AR Diffusion Distillation")
  - legacy cards: `Model Compression …`, `Efficient Inference …`, `Multi-Agent …`, `World Model …`
  - The KO chip keeps the same English first segment (e.g. "Small–Large Alignment · 온폴리시 증류").
- **Badges** — keep only the ones that apply:
  - `.badge.venue` "ICML'26 Oral" (main track) · `.badge.pre` "Preprint" / "Workshop @ NeurIPS'26"
  - `.badge.lab` "🏛 Berkeley · Stoica · Zaharia · Song Han" (matched lab/authors)
  - `.badge.hot` "▲ 103 alphaXiv · 112 HF · ★ 13.8k GitHub"
- Meta: first author bold, others plain, `(corresponding: …)` pair, affiliations, date, arXiv link.

## TL;DR (`ul.tl`)
Each `li` = `<span class="k">` label pair + `<span>` text pair. The Method `li` has `class="m"`
(highlight) and starts with `<b>core idea</b>` followed by the intuition clause.
- Motivation: the gap / pain (what fails today).
- Analysis: the observation that unlocks the method (a measurement, not a claim).
- Method: **what they do** + why it works, one breath.
- Results: 2–3 headline numbers with baselines named.

## Guiding text — the sentences that make the visuals readable
Visuals are the body, but a card with only visuals is hard to read (user feedback 2026-09-26). Put
text where it *orients* the reader, not where it repeats a caption:
- **💭 Intuition** (`.intuit`, right after the TL;DR): the mechanism as an everyday analogy or a
  picture in words, bolding the two or three moves (e.g. "a small desk and a bookshelf: **carry it to
  the desk** or **read it at the shelf**"). No numbers here.
- **Visual lead** (`p.vlead` pair directly under each `h2`, before the figure/chart/table):
  `<b>The one point to notice.</b>` + one clause on why. It states the conclusion the visual proves;
  the caption then only says what is plotted.
- **3-step summary** (`ol.steps.compact`, after the paper figure): how the whole method runs, in
  order — each step a bold one-liner and a short detail. Cover what the figure can't show.
- **Verdict**: 💡 what to carry into your own work (1–2 sentences, with the reason) · ⚠️ the most
  important limitation (1–2 sentences).

## Figure (`figure.fig`)
`<a class="zoom" href="fig/<ID>/<file>" target="_blank"><img …></a>` (tap-to-enlarge on phones),
`{{FIG_LABEL}}` = the paper's number ("Figure 2"), caption 1–2 lines per language, `.figsrc` line.
A small single-panel plot (≲ 600 px wide, e.g. one matplotlib axis) gets `class="fig narrow"` so it isn't
stretched to full width. A paper figure can also sit in a `.vgrid` next to a custom chart.

## Custom charts (`figure.chart`)
```html
<figure class="chart">
  <div class="ct">title pair</div><div class="cs">subtitle pair (source · units · what the line means)</div>
  <div class="bars mono" style="--x:40%">            <!-- mono = single series; --x = reference line -->
    <div class="bar" title="label: value"><span class="bl">label</span><span class="bt"><span class="bf" style="--w:84%"></span></span><span class="bv">2.1×</span></div>
  </div>
  <figcaption class="t-en">…</figcaption><figcaption class="t-ko">…</figcaption>
</figure>
```
- **Emphasis** (ours vs baselines): no `mono`; ours = `class="bar hl"`, baselines plain (gray).
- **Two-part split** (share A vs B): `<span class="bt stack"><span class="seg a" style="--w:25%">25%</span><span class="seg b" style="--w:75%">75%</span></span>`
  plus a `.legend` (`<i class="a"></i>`, `<i class="b"></i>`, `<i class="r"></i>` for the line).
  Leave a segment's text empty when it is < 12% wide.
- Widths: `--w = value / axis_max × 100`, axis max a round number ≥ the largest value. Never truncate the axis.
- Wide values (e.g. "11.8 / 47.5"): widen the value column with `style="--vw:84px"` on `.bars`.
- Two charts side by side: wrap in `<div class="vgrid">` (stacks on phones).
- Derived numbers (computed by you) must say so in `.cs`: "computed from Table 1".

## Table (`.tablewrap > table.ptable`)
≤ 6 rows, winning cells `class="up"`, caption pair states source ("Table 3", "Figure 4b values") and
direction ("lower is better").

## Stats (`.stats.three`)
Exactly 3: `{{Nn}}` value (shared) + `{{Ln_EN/KO}}` ≤ 8-word label naming the comparison.

## Verdict
`.verdict > .v.take` 💡 1–2 sentences (what to carry into your own work, and why) · `.v.warn` ⚠️ 1–2
sentences on the most important limitation (missing ablation/baseline, eval scope) — specific, not a nitpick.

## Footer
"Why picked — <b>signals in one line</b>" + `venue: <Conf YYYY>` (accepted main-track only; workshops
as `Workshop @ Conf'YY`; nothing for preprints — build_index turns `Conf YYYY` into a venue tab).
`{{GEN_DATE}}` = today. Keep the three source links.

## After writing
1. `python3 .claude/skills/daily-paper-card/scripts/check_card.py papers/<file>.html` → OK
2. Screenshot desktop (1100 px) and phone (390 px iframe) with headless Chrome; fix overflow.
3. `echo <arxivId> >> done.log` · `python3 build_index.py` · report path + 2-line gist.
