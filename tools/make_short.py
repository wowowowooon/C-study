# -*- coding: utf-8 -*-
"""Generate OUTLINE_SHORT.md (one-screen curriculum map) and problems_txt/<id>.txt (plain text statements)."""
import glob, html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from chapters_def import CH, PARTS

def first_clause(t):
    head = re.split(r"[:：]", t, 1)[0]
    return (head if len(head) <= 70 else t[:70]).strip()

lines = ["# OUTLINE_SHORT — 커리큘럼 한눈에 보기", "",
         "자세한 내용은 OUTLINE.md와 specs/<id>.md. 장 N의 예제는 장 ≤ N에서 배운 것만 쓴다.", ""]
cur = None
for c in CH:
    if c["part"] != cur:
        cur = c["part"]
        lines += ["", f"## {PARTS[cur]}"]
    label = "부록" if c["num"] is None else f"{c['num']}장"
    lines.append(f"- [{c['id']}] {label} {c['title']} — " + "; ".join(first_clause(t) for t in c["topics"]))
open(os.path.join(ROOT, "OUTLINE_SHORT.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

def to_text(md):
    head = ""
    m = re.match(r"<!-- problem bank: (.*?) -->\n", md)
    if m:
        head, md = "META: " + m.group(1) + "\n", md[m.end():]
    s = re.sub(r"(?is)<br\s*/?>", "\n", md)
    s = re.sub(r"(?is)</(p|li|h\d|tr|div|pre|table|ul|ol|thead|tbody)>", "\n", s)
    s = re.sub(r"(?is)<li[^>]*>", "- ", s)
    s = re.sub(r"(?is)<t[dh][^>]*>", " | ", s)
    s = re.sub(r'(?is)<img[^>]*alt="([^"]*)"[^>]*>', r"[그림: \1]", s)
    s = re.sub(r"(?s)<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return head + s.strip() + "\n"

os.makedirs(os.path.join(ROOT, "problems_txt"), exist_ok=True)
n = 0
for p in glob.glob(os.path.join(ROOT, "problems", "*.md")):
    pid = os.path.basename(p)[:-3]
    open(os.path.join(ROOT, "problems_txt", pid + ".txt"), "w", encoding="utf-8").write(to_text(open(p, encoding="utf-8").read()))
    n += 1
print(f"OUTLINE_SHORT.md written; {n} problems_txt files")
