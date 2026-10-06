#!/usr/bin/env python3
"""Lint a v2 "visual-first" 5-min paper card. Exit 1 on any FAIL.

usage: python3 check_card.py papers/<date>-<slug>.html [--min-words 350] [--max-words 600]

Counts only English *reading* text: skips the paper title, Korean (.t-ko), tables, chart bars/legends,
inline SVG, the meta/badge lines, the rating widget, footer source links, and alt text.
"""
import re, sys, html
from html.parser import HTMLParser

VOID = {"meta", "link", "img", "br", "hr", "input", "source", "wbr"}
SKIP_CLASSES = {"t-ko", "bars", "legend", "meta", "badges", "rating", "src", "kicker", "langtoggle", "figsrc", "k", "home", "n"}
SKIP_TAGS = {"script", "style", "svg", "table", "title", "head"}
SKIP_IDS = {"bar"}
WORD = re.compile(r"[A-Za-z][A-Za-z'’]+(?:-[A-Za-z]+)*")   # real words: ≥2 letters; numbers/units don't count
UNITS = {"tok", "gb", "mb", "tb", "ms", "gib", "vs"}

class Words(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.skip = 0; self.words = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        a = dict(attrs); cls = set((a.get("class") or "").split())
        s = tag in SKIP_TAGS or bool(cls & SKIP_CLASSES) or a.get("id") in SKIP_IDS
        self.stack.append((tag, s)); self.skip += s
    def handle_endtag(self, tag):
        if tag in VOID: return
        while self.stack:
            t, s = self.stack.pop(); self.skip -= s
            if t == tag: break
    def handle_data(self, d):
        if not self.skip: self.words += [x for x in WORD.findall(d) if x.lower() not in UNITS]

def main():
    args = sys.argv[1:]
    if not args: sys.exit(__doc__)
    path = args[0]; maxw = int(args[args.index("--max-words") + 1]) if "--max-words" in args else 600
    minw = int(args[args.index("--min-words") + 1]) if "--min-words" in args else 350
    t = open(path, encoding="utf-8").read()
    fails, warns = [], []

    w = Words(); w.feed(re.sub(r"<h1>.*?<br>", "<h1>", t, count=1, flags=re.S)); n = len(w.words)  # paper title is fixed, not counted
    if n > maxw: fails.append(f"English reading text is {n} words (max {maxw}) — cut prose, keep the visuals")
    if n < minw: fails.append(f"English reading text is {n} words (min {minw}) — too bare: add the intuition box, a lead sentence per visual, the 3-step summary")
    if 'class="intuit"' not in t: fails.append("missing the 💭 intuition box (.intuit)")
    vl = len(re.findall(r'class="vlead[^"]*t-en"', t))
    if vl < 2: fails.append(f"only {vl} visual lead sentence(s) (.vlead) — put one bold takeaway sentence above each visual")
    if 'class="steps compact"' not in t: warns.append("no 3-step how-it-works summary (ol.steps.compact)")

    tl = re.search(r'<ul class="tl">(.*?)</ul>', t, re.S)
    if not tl:
        fails.append("TL;DR must be <ul class=\"tl\"> with 4 bullets")
    else:
        keys = re.findall(r'<span class="k"><span class="t-en">([^<]+)</span>', tl.group(1))
        if keys != ["Motivation", "Analysis", "Method", "Results"]:
            fails.append(f"TL;DR bullets must be Motivation, Analysis, Method, Results in order (got {keys})")
        for li in re.findall(r"<li.*?</li>", tl.group(1), re.S):
            en = re.search(r'<span class="k">.*?</span></span><span><span class="t-en">(.*?)</span><span class="t-ko">', li, re.S)
            if en:
                k = re.search(r'class="t-en">([^<]+)', li).group(1)
                c = len(WORD.findall(re.sub(r"<[^>]+>", " ", en.group(1))))
                cap = 45 if k == "Method" else 32
                if c > cap: warns.append(f"TL;DR '{k}' bullet is {c} words (aim ≤ {cap - 7})")

    figs = len(re.findall(r'<figure class="fig(?: [^"]*)?">\s*(?:<a[^>]*>\s*)?<img', t))
    custom = len(re.findall(r'<figure class="chart">', t)) + len(re.findall(r"<svg[\s>]", t))
    tables = t.count('class="ptable"')
    if figs < 1: warns.append("no paper figure (<figure class=\"fig\"><img>) — required when arXiv HTML exists")
    if custom < 1: fails.append("no custom visual (<figure class=\"chart\"> or inline <svg>)")
    if tables < 1: warns.append("no key table (.ptable)")
    if figs > 3: warns.append(f"{figs} paper figures (max 3)")

    en_n = len(re.findall(r'class="t-en"', t)); ko_n = len(re.findall(r'class="t-ko"', t))
    if en_n != ko_n: fails.append(f"t-en ({en_n}) and t-ko ({ko_n}) counts differ — every reading string needs a pair")

    arx = re.search(r"arXiv:([0-9]{4}\.[0-9]{4,5})", t)
    rat = re.search(r'class="rating" data-arxiv="([^"]+)"', t)
    if not rat: fails.append("missing rating section")
    elif arx and rat.group(1) != arx.group(1): fails.append(f"rating data-arxiv {rat.group(1)} ≠ {arx.group(1)}")
    if "noindex" not in t: fails.append("missing noindex")
    if "{{" in t: fails.append("unfilled {{PLACEHOLDER}} left")
    chip = re.search(r'<span class="chip"><span class="t-en">([^<]*)', t)
    if chip and re.match(r"[^\w\s]", chip.group(1).strip()): fails.append("topic chip starts with an emoji/symbol")
    for m in re.finditer(r'<span class="bf" style="--w:([0-9.]+)%', t):
        if float(m.group(1)) > 100: fails.append(f"bar width {m.group(1)}% > 100%")

    print(f"{path}: {n} EN words · paper figures {figs} · custom visuals {custom} · tables {tables}")
    for x in warns: print("  WARN", x)
    for x in fails: print("  FAIL", x)
    print("  OK" if not fails else "  → fix the FAILs")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
