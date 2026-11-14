# -*- coding: utf-8 -*-
"""Export the course working dir into the portfolio repo layout.

repo/
  README.md, STUDY_LOG.md, solutions/, .gitignore   <- owned by the repo (never overwritten)
  notes/index.html, notes/chapters/*.html           <- from dist/ and chapters/
  docs/curriculum.md, docs/problems.md              <- generated
  notebook-src/                                     <- production tools/specs (no problem statements)
README.md block between <!-- PROGRESS:START --> and <!-- PROGRESS:END --> is regenerated.
Usage: python3 -I tools/export_portfolio.py [REPO_DIR]
"""
import glob, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from chapters_def import CH, PARTS
REPO = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("COURSE_REPO_DIR", "/home/user/c-c-study")
SKIP_SRC = {"problems", "problems_txt", "work", "__pycache__", "repos_cache", ".git", "backup", "chapters", "dist"}

def same(a, b):
    try:
        return os.path.getsize(a) == os.path.getsize(b) and open(a, "rb").read() == open(b, "rb").read()
    except OSError:
        return False

def mirror(src, dst, skip=frozenset()):
    keep = set()
    for d, dirs, files in os.walk(src):
        rel = os.path.relpath(d, src)
        dirs[:] = [x for x in dirs if x not in skip]
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            if f.endswith((".pyc", ".swp", ".lock")):
                continue
            s, t = os.path.join(d, f), os.path.normpath(os.path.join(dst, rel, f))
            keep.add(t)
            if not same(s, t):
                shutil.copy2(s, t)
    for d, dirs, files in os.walk(dst, topdown=False):
        for f in files:
            t = os.path.normpath(os.path.join(d, f))
            if t not in keep:
                os.remove(t)
        if d != dst and not os.listdir(d):
            os.rmdir(d)

meta = {}
for line in open(os.path.join(ROOT, "meta.tsv"), encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    p = line.rstrip("\n").split("\t")
    meta[p[0]] = p

def label(c):
    return "부록" if c["num"] is None else f"{c['num']}장"

done_ids = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, "chapters", "*.html"))}

# 1) production sources
mirror(ROOT, os.path.join(REPO, "notebook-src"), SKIP_SRC)
open(os.path.join(REPO, "notebook-src", "README.md"), "w", encoding="utf-8").write(
"""# notebook-src — 노트 제작·검증 도구

`notes/`의 학습 노트를 만들고 검증하는 데 쓴 파일들입니다. 노트는 Claude와 함께 작성했고, 아래 도구로 품질을 확인했습니다.

| 파일 | 역할 |
|---|---|
| `STYLE.md` | 노트 작성 규칙(학습자 수준, 설명 방식, HTML 구성) |
| `OUTLINE.md`, `specs/` | 전체 커리큘럼과 챕터별 설계서 |
| `meta.tsv` | 프로그래머스 문제 687개의 번호·현재 제목·레벨 |
| `tools/verify_chapter.py` | 챕터 안의 모든 C/C++ 예제를 실제로 컴파일·실행하고, 노트에 적힌 출력과 비교 |
| `tools/assemble.py` | 챕터를 하나의 노트 페이지로 조립 |
| `tools/export_portfolio.py`, `tools/checkpoint.py` | 이 저장소 구조로 내보내고 커밋·푸시 |
| `HANDOFF.md`, `STATUS.md` | 제작 인수인계 문서와 진행 상황 |

프로그래머스 문제 원문은 저작권 때문에 넣지 않았습니다(`tools/build_problem_bank.py`로 다시 받을 수 있음).
""")

# 2) notes
os.makedirs(os.path.join(REPO, "notes"), exist_ok=True)
if os.path.exists(os.path.join(ROOT, "dist", "index.html")):
    shutil.copy2(os.path.join(ROOT, "dist", "index.html"), os.path.join(REPO, "notes", "index.html"))
mirror(os.path.join(ROOT, "chapters"), os.path.join(REPO, "notes", "chapters"))

# 3) docs
sol = {}
for p in glob.glob(os.path.join(REPO, "solutions", "**", "*.*"), recursive=True):
    m = re.match(r"(\d+)", os.path.basename(p))
    if m:
        sol.setdefault(m.group(1), os.path.relpath(p, os.path.join(REPO, "docs")).replace(os.sep, "/"))
os.makedirs(os.path.join(REPO, "docs"), exist_ok=True)
cur = ["# 커리큘럼", "", "C/C++ 기초 → 알고리즘(프로그래머스 Lv.1~Lv.3) → 임베디드 C/C++ 순서로 공부합니다. 노트는 [`notes/`](../notes)에 있습니다.", ""]
part = None
for c in CH:
    if c["part"] != part:
        part = c["part"]
        cur += ["", f"## {PARTS[part]}", "", "| 장 | 제목 | 다루는 내용 | 문제 | 노트 |", "|---|---|---|---|---|"]
    topics = "; ".join(re.split(r"[:：(]", t, maxsplit=1)[0].strip()[:40] for t in c["topics"][:4])
    st = "완성" if c["id"] in done_ids else "제작 예정"
    cur.append(f"| {label(c)} | {c['title']} | {topics} | {len(c['problems']) or '-'} | {st} |")
open(os.path.join(REPO, "docs", "curriculum.md"), "w", encoding="utf-8").write("\n".join(cur) + "\n")

pr = ["# 프로그래머스 문제 로드맵", "",
      "챕터별로 고른 문제입니다. 풀이를 `solutions/programmers/lv<레벨>/<문제번호>_<이름>.cpp`로 올리면 '내 풀이' 칸에 자동으로 링크됩니다.",
      "레벨과 제목은 2026년 11월 기준이며 사이트에서 바뀔 수 있습니다.", ""]
total = solved = 0
seen = set()
for c in CH:
    if not c["problems"]:
        continue
    pr += ["", f"## {label(c)} {c['title']}", "", "| 번호 | 문제 | 레벨 | 구분 | 내 풀이 |", "|---|---|---|---|---|"]
    for role, pid, _ in c["problems"]:
        m = meta[pid]
        link = f"[{m[1]}](https://school.programmers.co.kr/learn/courses/30/lessons/{pid})"
        mine = f"[보기]({sol[pid]})" if pid in sol else ""
        pr.append(f"| {pid} | {link} | Lv.{m[2]} | {role} | {mine} |")
        if pid not in seen:
            seen.add(pid); total += 1
            if pid in sol:
                solved += 1
open(os.path.join(REPO, "docs", "problems.md"), "w", encoding="utf-8").write("\n".join(pr) + "\n")

# 4) README progress block
rp = os.path.join(REPO, "README.md")
if os.path.exists(rp):
    s = open(rp, encoding="utf-8").read()
    nd = sum(1 for c in CH if c["id"] in done_ids)
    block = (f"<!-- PROGRESS:START -->\n| 항목 | 진행 |\n|---|---|\n"
             f"| 노트 챕터 | {nd} / {len(CH)} 완성 |\n| 프로그래머스 풀이 | {solved} / {total} 문제 |\n<!-- PROGRESS:END -->")
    s = re.sub(r"<!-- PROGRESS:START -->.*?<!-- PROGRESS:END -->", block, s, flags=re.S)
    open(rp, "w", encoding="utf-8").write(s)
print(f"exported: chapters={len(done_ids)} problems={total} solved={solved}")
