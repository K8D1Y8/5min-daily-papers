#!/usr/bin/env python3
"""Score candidate papers by notability signals (venue · listed author/lab · frontier report · hot).

usage (run from the archive root, where sources.md and done.log live):
  python3 paper_signals.py ID[:axVotes[:axViews]][@org1|org2] ...  [--sources sources.md] [--json]
  python3 paper_signals.py --slot      # which topic today's card is due for: P1 / P2 / legacy

  axVotes/axViews/orgs come from the alphaXiv discover_papers result line, e.g.
    "Published 2026-08-17 by University of California, Berkeley, UT Austin · 103 votes · 1409 views"
  → 2608.16157:103:1409@University of California, Berkeley|UT Austin

Fetches arXiv metadata (title, authors, comment/journal-ref, date) and Hugging Face paper stats
(upvotes, GitHub stars). Rules and lists live in sources.md so the user can edit them.
"""
import json, os, re, sys, unicodedata, urllib.request, urllib.error
import xml.etree.ElementTree as ET
from datetime import date, datetime

UA = {"User-Agent": "daily-paper-card/2 (paper_signals)"}

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def norm(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    toks = [t for t in re.split(r"[^a-z]+", s) if len(t) > 1]      # drop initials like "E."
    return " ".join(toks)

def load_sources(path):
    sec, out = None, {}
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            sec = line[3:].strip().lower(); out.setdefault(sec, []); continue
        m = re.match(r"-\s+(.*)", line)
        if sec and m:
            out[sec].append([x.strip() for x in m.group(1).split(" — ", 1)])
    get = lambda key: next((v for k, v in out.items() if k.startswith(key)), [])
    th = {k.lower(): float(v[0]) for k, *v in get("hot thresholds") if v}
    return {
        "p1": [e[0].lower() for e in get("p1 keywords")],
        "p2": [e[0].lower() for e in get("p2 keywords")],
        "venues": [e[0] for e in get("venues")],
        "authors": {norm(e[0]): e[0] for e in get("authors")},
        "labs": [e[0] for e in get("labs")],
        "frontier": [e[0] for e in get("frontier")],
        "th": th,
    }

def arxiv_meta(ids):
    xml = fetch("https://export.arxiv.org/api/query?max_results=%d&id_list=%s" % (len(ids), ",".join(ids)))
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    out = {}
    for e in ET.fromstring(xml).findall("a:entry", ns):
        aid = re.sub(r"v\d+$", "", e.findtext("a:id", "", ns).rsplit("/", 1)[-1])
        out[aid] = {
            "title": " ".join(e.findtext("a:title", "", ns).split()),
            "authors": [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)],
            "published": e.findtext("a:published", "", ns)[:10],
            "summary": " ".join(e.findtext("a:summary", "", ns).split()),
            "comment": " ".join((e.findtext("x:comment", "", ns) or "").split()),
            "jref": " ".join((e.findtext("x:journal_ref", "", ns) or "").split()),
        }
    return out

def hf_stats(aid):
    try:
        d = json.loads(fetch("https://huggingface.co/api/papers/" + aid, timeout=10))
        return d.get("upvotes") or 0, d.get("githubStars") or 0
    except Exception:
        return 0, 0

def venue_signal(text, venues):
    for v in venues:
        m = re.search(r"\b%s\W{0,3}(?:20)?(\d\d)(?!\d)" % re.escape(v), text, re.I)
        if m:
            label = "%s'%s" % (v, m.group(1))
            if re.search(r"workshop", text, re.I):
                return 1, label + " workshop"
            bonus = 1 if re.search(r"\b(oral|spotlight|best paper)\b", text, re.I) else 0
            tag = re.search(r"\b(oral|spotlight|best paper)\b", text, re.I)
            return 3 + bonus, label + (" " + tag.group(1).title() if tag else "")
    if re.search(r"workshop", text, re.I):
        return 1, "workshop"
    return 0, ""

def score(aid, meta, ax_votes, ax_views, orgs, src, done):
    th, parts, why = src["th"], {}, []
    text = (meta["title"] + " " + meta.get("summary", "")).lower()
    tags = [t.upper() for t in ("p1", "p2") if any(k in text for k in src[t])]
    if tags: parts["priority"] = 3; why.append("+".join(tags))
    v, vlabel = venue_signal(meta["comment"] + " " + meta["jref"], src["venues"])
    if v: parts["venue"] = v; why.append(vlabel)
    hit = [src["authors"][norm(a)] for a in meta["authors"] if norm(a) in src["authors"]]
    labs = [l for l in src["labs"] if any(l.lower() in o.lower() for o in orgs)]
    if hit or labs: parts["people"] = 3; why.append("·".join(hit + labs))
    blob = " ".join(meta["authors"])
    fr = [f for f in src["frontier"] if re.search(r"\b%s\b" % re.escape(f), blob, re.I)
          or (re.search(r"technical report", meta["title"], re.I) and re.search(r"\b%s\b" % re.escape(f), meta["title"], re.I))]
    if fr: parts["frontier"] = 3; why.append("frontier:" + fr[0])
    hf, stars = hf_stats(aid)
    hot = (ax_votes >= th.get("alphaxiv votes", 20) or ax_views >= th.get("alphaxiv views", 300)
           or hf >= th.get("hf upvotes", 30) or stars >= th.get("github stars", 500))
    very = (ax_votes >= th.get("very hot: alphaxiv votes", 100) or hf >= th.get("very hot: hf upvotes", 100)
            or stars >= th.get("very hot: github stars", 5000))
    if hot: parts["hot"] = 2 + (1 if very else 0)
    why.append("▲%d ax · %d views · %d HF · ★%d" % (ax_votes, ax_views, hf, stars))
    try: age = (date.today() - datetime.strptime(meta["published"], "%Y-%m-%d").date()).days
    except ValueError: age = -1
    return {"id": aid, "score": sum(parts.values()), "parts": parts, "age_days": age, "done": aid in done,
            "title": meta["title"], "first": (meta["authors"] or [""])[0], "last": (meta["authors"] or [""])[-1],
            "venue": vlabel, "topic": "+".join(tags) or "legacy",
            "signals": " | ".join(w for w in why if w), "hf": hf, "stars": stars}

def card_slot(papers_dir="papers"):
    """P1/P2 alternate; after 6 priority cards in a row, one legacy card (6:1 rotation)."""
    import glob
    kinds = []
    for f in sorted(glob.glob(os.path.join(papers_dir, "*.html"))):
        t = open(f, encoding="utf-8").read()
        m = re.search(r'<span class="chip">\s*<span class="t-en">(.*?)</span>', t, re.S)
        first = (m.group(1) if m else "").split("·")[0].lower()
        kinds.append("P1" if "alignment" in first else "P2" if "video" in first else "legacy")
    last6 = kinds[-6:]
    if len(last6) == 6 and "legacy" not in last6:
        return "legacy", "the last 6 cards were all priority topics"
    prio = [k for k in kinds if k != "legacy"]
    if not prio:
        return "P1", "no priority-topic card yet — start with P1"
    nxt = "P2" if prio[-1] == "P1" else "P1"
    return nxt, "last priority card was %s" % prio[-1]

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"): sys.exit(__doc__)
    if args[0] == "--slot":
        slot, why = card_slot(); print("%s  (%s)" % (slot, why)); return
    as_json = "--json" in args; args = [a for a in args if a != "--json"]
    src_path = "sources.md"
    if "--sources" in args:
        i = args.index("--sources"); src_path = args[i + 1]; del args[i:i + 2]
    src = load_sources(src_path)
    done = set(open("done.log").read().split()) if os.path.exists("done.log") else set()
    cands = []
    for a in args:
        head, _, orgs = a.partition("@")
        bits = head.split(":")
        cands.append((bits[0], int(bits[1]) if len(bits) > 1 and bits[1] else 0,
                      int(bits[2]) if len(bits) > 2 and bits[2] else 0, [o for o in orgs.split("|") if o]))
    meta = arxiv_meta([c[0] for c in cands])
    rows = [score(aid, meta[aid], v, w, o, src, done) for aid, v, w, o in cands if aid in meta]
    missing = [c[0] for c in cands if c[0] not in meta]
    rows.sort(key=lambda r: (r["done"], -r["score"], r["age_days"]))
    if as_json:
        print(json.dumps({"rows": rows, "missing": missing}, ensure_ascii=False, indent=1)); return
    for r in rows:
        flag = " (done)" if r["done"] else ""
        print("%-11s score %2d  %-6s %-40s %3dd  %s%s" % (r["id"], r["score"], r["topic"], json.dumps(r["parts"])[1:-1], r["age_days"], r["title"][:64], flag))
        print("            %s" % r["signals"])
    if missing: print("not found on arXiv:", " ".join(missing))

if __name__ == "__main__":
    main()
