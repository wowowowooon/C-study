# -*- coding: utf-8 -*-
"""Assemble chapters/*.html into dist/index.html using shell/template.html.
Usage: python3 -I assemble.py [--allow-missing]
"""
import html.parser, os, re, sys, unicodedata, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from chapters_def import CH

allow_missing = "--allow-missing" in sys.argv
tpl = open(os.path.join(ROOT, "shell", "template.html"), encoding="utf-8").read()
meta = {}
for line in open(os.path.join(ROOT, "meta.tsv"), encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    p = line.rstrip("\n").split("\t")
    meta[p[0]] = p[1]

def norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))

parts = []
missing = []
for c in CH:
    path = os.path.join(ROOT, "chapters", f"{c['id']}.html")
    if not os.path.exists(path):
        missing.append(c["id"])
        if not allow_missing:
            continue
        frag = (f'<section class="lesson" id="{c["id"]}" data-title="{c["dtitle"]}" data-short="{c["short"]}" hidden>'
                f'<div class="kicker">준비 중</div><h2>{c["title"]}<span class="en-t">{c["en"]}</span></h2>'
                f'<div class="goal">이 챕터는 아직 정리 중입니다. 앞 챕터를 먼저 공부하세요.</div></section>')
    else:
        frag = open(path, encoding="utf-8").read().strip()
    # inject data-part on the section tag (replace if present)
    m = re.search(r"<section\b[^>]*>", frag)
    if not m:
        print("NO SECTION TAG in", c["id"]); sys.exit(1)
    tag = m.group(0)
    newtag = re.sub(r'\sdata-part="[^"]*"', "", tag)
    newtag = newtag[:-1] + f' data-part="{c["part"]}">'
    if " hidden" not in newtag and not re.search(r"\shidden[\s>=]", newtag):
        newtag = newtag[:-1] + " hidden>"
    frag = frag[:m.start()] + newtag + frag[m.end():]
    parts.append(f"<!-- ===== {c['id']} ===== -->\n" + frag)
apx = open(os.path.join(ROOT, "shell", "apxC.html"), encoding="utf-8").read().strip()
apx = apx.replace('<section class="lesson" id="apxC"', '<section class="lesson" id="apxC" data-part="X"', 1)
parts.append("<!-- ===== apxC ===== -->\n" + apx)
body = "\n\n".join(parts)
out = tpl.replace("{{SECTIONS}}", body)

# global checks
class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = collections.Counter(); self.links = []; self.sections = []; self._a = None
    def handle_starttag(self, t, a):
        a = dict(a)
        if "id" in a: self.ids[a["id"]] += 1
        if t == "section" and "lesson" in (a.get("class") or ""): self.sections.append(a.get("id"))
        if t == "a": self._a = [a.get("href", ""), "data-go" in a, []]
    def handle_endtag(self, t):
        if t == "a" and self._a is not None:
            self.links.append((self._a[0], self._a[1], "".join(self._a[2]).strip())); self._a = None
    def handle_data(self, d):
        if self._a is not None: self._a[2].append(d)
p = P(); p.feed(out)
problems = []
for i, n in p.ids.items():
    if n > 1: problems.append(f"duplicate id {i} x{n}")
secs = set(p.sections)
for href, go, text in p.links:
    if href.startswith("#"):
        if href[1:] not in secs and href[1:] not in p.ids:
            problems.append(f"broken internal link {href} ('{text}')")
    m = re.search(r"lessons/(\d+)", href)
    if m:
        pid = m.group(1)
        if pid not in meta: problems.append(f"unknown problem id {pid} ('{text}')")
        elif text and norm(text) != norm(meta[pid]): problems.append(f"title mismatch {pid}: '{text}' vs '{meta[pid]}'")
os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
dst = os.path.join(ROOT, "dist", "index.html")
open(dst, "w", encoding="utf-8").write(out)
print(f"wrote {dst}: {len(out.encode('utf-8'))/1024:.0f} KB, sections={len(p.sections)}, missing={missing}")
print(f"programmers links: {sum(1 for h,_,_ in p.links if 'lessons/' in h)}")
if problems:
    print("PROBLEMS:"); print("\n".join(problems[:80]))
