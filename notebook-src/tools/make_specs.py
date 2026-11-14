# -*- coding: utf-8 -*-
import os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from chapters_def import CH, PARTS

meta = {}
for line in open(os.path.join(ROOT, "meta.tsv"), encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    p = line.rstrip("\n").split("\t")
    meta[p[0]] = dict(id=p[0], title=p[1], level=p[2], lsrc=p[3], st=p[4], cat=p[5], old=p[6] if len(p) > 6 else "")

errors = []
seen = collections.defaultdict(list)
for c in CH:
    for role, pid, note in c["problems"]:
        if pid not in meta:
            errors.append(f"{c['id']}: {pid} not in meta")
            continue
        m = meta[pid]
        if not m["st"]:
            errors.append(f"{c['id']}: {pid} has no statement")
        if not m["level"]:
            errors.append(f"{c['id']}: {pid} has no level")
        seen[pid].append((c["id"], role))
for pid, uses in seen.items():
    non_c = [u for u in uses if u[1] != "C로 다시"]
    if len(non_c) > 1:
        errors.append(f"duplicate problem {pid} {meta[pid]['title']}: {uses}")
if errors:
    print("\n".join(errors))
    sys.exit(1)

def cid(c):
    return c["id"]

def chap_label(c):
    if c["num"] is None:
        return c["title"].split(":")[0]
    if c["num"] == 0:
        return "0장"
    return f"{c['num']}장"

# OUTLINE.md
out = ["# 커리큘럼 전체 지도 (OUTLINE)", "",
       "각 장의 id, 제목, 다루는 내용. 장 N의 예제는 장 ≤ N에서 배운 것만 사용한다.", ""]
cur = None
for c in CH:
    if c["part"] != cur:
        cur = c["part"]
        out += ["", f"## {PARTS[cur]}", ""]
    out.append(f"### [{c['id']}] {chap_label(c)} — {c['title']}  ({c['en']})")
    out.append(f"- rail: data-title=\"{c['dtitle']}\" data-short=\"{c['short']}\"")
    for t in c["topics"]:
        out.append(f"- {t}")
    if c["problems"]:
        ps = ", ".join(f"{pid} {meta[pid]['title']}(Lv.{meta[pid]['level']})" for _, pid, _ in c["problems"])
        out.append(f"- 문제: {ps}")
    out.append("")
open(os.path.join(ROOT, "OUTLINE.md"), "w", encoding="utf-8").write("\n".join(out))

# specs
idx = {c["id"]: i for i, c in enumerate(CH)}
for i, c in enumerate(CH):
    prev = CH[i - 1] if i > 0 else None
    nxt = CH[i + 1] if i + 1 < len(CH) else None
    if c["num"] is None:
        kicker = f"{c['title'].split(':')[0]} · 부록"
    elif c["num"] == 0:
        kicker = "Chapter 0 · 시작 전에"
    else:
        kicker = f"Chapter {c['num']} · {PARTS[c['part']]}"
    s = []
    s.append(f"# Spec for chapter `{c['id']}` — {c['title']}")
    s.append("")
    s.append("Read STYLE.md and OUTLINE.md first. This spec lists WHAT to teach; STYLE.md says HOW.")
    s.append("")
    s.append("## Identity (use exactly)")
    s.append(f"- section id: `{c['id']}`")
    s.append(f"- data-title: `{c['dtitle']}`   data-short: `{c['short']}`")
    s.append(f"- kicker: `{kicker}`")
    s.append(f"- h2: `{c['title']}`  with  <span class=\"en-t\">{c['en']}</span>")
    s.append(f"- output file: chapters/{c['id']}.html   scratch dir: work/{c['id']}/")
    s.append("")
    s.append("## Position in the course")
    if prev:
        s.append(f"- Previous: [{prev['id']}] {prev['title']}. The learner has finished everything up to and including it (see OUTLINE.md).")
    if nxt:
        s.append(f"- Next: [{nxt['id']}] {nxt['title']}. Point to it in the final .out box.")
    s.append(f"- Feature constraint for code in this chapter: {c['allowed']}")
    s.append("")
    s.append("## Topics to teach (in this order; each normally becomes one or more numbered h3 sections)")
    for n, t in enumerate(c["topics"], 1):
        s.append(f"{n}. {t}")
    s.append("")
    if c["confusions"]:
        s.append("## Confusions you MUST address explicitly (each in a .pen box or a quiz)")
        for t in c["confusions"]:
            s.append(f"- {t}")
        s.append("")
    if c["emb"]:
        s.append("## Embedded connections to use (.emb boxes, only where natural)")
        for t in c["emb"]:
            s.append(f"- {t}")
        s.append("")
    if c["problems"]:
        s.append("## Assigned Programmers problems (all verified to exist; use the CURRENT title for the link text)")
        s.append("")
        s.append("| role | id | current title | level | statement file | category | note |")
        s.append("|---|---|---|---|---|---|---|")
        for role, pid, note in c["problems"]:
            m = meta[pid]
            s.append(f"| {role} | {pid} | {m['title']} | Lv.{m['level']} | {m['st']} | {m['cat']} | {note} |")
        s.append("")
        s.append("Rules: read each statement file before writing; keep the role (필수/추가/도전/C로 다시) as the "
                 "pcore label; decide 함수형/입출력형/빈칸채우기(PCCE) from the statement; you may drop a problem only "
                 "if it truly cannot be solved with what has been taught (report it); do not add problems "
                 "that are not in this table.")
        s.append("")
    if c.get("notes"):
        s.append("## Extra notes")
        s.append(c["notes"])
        s.append("")
    open(os.path.join(ROOT, "specs", f"{c['id']}.md"), "w", encoding="utf-8").write("\n".join(s))

print("chapters:", len(CH), "problems:", sum(len(c['problems']) for c in CH), "unique:", len(seen))
for c in CH:
    print(c["id"], c["short"], len(c["topics"]), "topics,", len(c["problems"]), "problems")
