# -*- coding: utf-8 -*-
"""Build STATUS.md and state/progress.json for the C/C++ notebook.

Sources (merged, newest wins):
  1. state/progress.json from earlier runs (committed to git, survives new sessions)
  2. workflow journals of the current session (if the directory exists):
     /root/.claude/projects/*/subagents/workflows/*/journal.jsonl
  3. chapter files present in chapters/

Usage: python3 -I status.py [--journals GLOB] [--artifact-url URL] [--artifact-slug SLUG]
"""
import datetime, glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from chapters_def import CH

args = sys.argv[1:]
def opt(name, default=None):
    if name in args:
        i = args.index(name)
        return args[i + 1] if i + 1 < len(args) else default
    return default

jglob = opt("--journals", "/root/.claude/projects/*/*/subagents/workflows/*/journal.jsonl")
state_dir = os.path.join(ROOT, "state")
os.makedirs(state_dir, exist_ok=True)
pfile = os.path.join(state_dir, "progress.json")
prog = {}
if os.path.exists(pfile):
    try:
        prog = json.load(open(pfile, encoding="utf-8"))
    except Exception:
        prog = {}
art = prog.get("_artifact", {})
if opt("--artifact-url"):
    art["url"] = opt("--artifact-url")
if opt("--artifact-slug"):
    art["slug"] = opt("--artifact-slug")
if art:
    prog["_artifact"] = art

def entry(cid):
    return prog.setdefault(cid, {"write": None, "review": None})

def find_result(obj):
    """Return the structured result dict from a journal line, whatever the field name is."""
    for k in ("result", "output", "value", "data", "returned"):
        v = obj.get(k)
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            try:
                d = json.loads(v)
                if isinstance(d, dict):
                    return d
            except Exception:
                pass
    return None

for jf in sorted(glob.glob(jglob)):
    try:
        lines = open(jf, encoding="utf-8").read().splitlines()
    except Exception:
        continue
    agent_label = {}
    for ln in lines:
        try:
            o = json.loads(ln)
        except Exception:
            continue
        if o.get("type") == "started" and o.get("agentId"):
            agent_label[o["agentId"]] = o.get("label") or ""
    for ln in lines:
        try:
            o = json.loads(ln)
        except Exception:
            continue
        label = o.get("label") or agent_label.get(o.get("agentId"), "")
        m = re.match(r"(write|review):([A-Za-z0-9]+)", label)
        if not m:
            continue
        stage, cid = m.group(1), m.group(2)
        e = entry(cid)
        typ = o.get("type")
        if typ == "started":
            if e.get(stage) != "done":
                e[stage] = "running"
            e[stage + "_workflow"] = os.path.basename(os.path.dirname(jf))
        elif typ == "result":
            res = find_result(o)
            if res is not None:
                e[stage] = "done"
                e[stage + "_report"] = res
            elif e.get(stage) != "done":
                e[stage] = "failed"
        elif typ and ("err" in typ or "fail" in typ):
            if e.get(stage) != "done":
                e[stage] = "failed"

now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9)))
rows = []
nw = nr = 0
for c in CH:
    cid = c["id"]
    e = entry(cid)
    path = os.path.join(ROOT, "chapters", f"{cid}.html")
    exists = os.path.exists(path)
    size = os.path.getsize(path) // 1024 if exists else 0
    e["file_kb"] = size
    if e.get("write") == "done" or (exists and e.get("review") == "done"):
        nw += 1
    if e.get("review") == "done":
        nr += 1
    wr = e.get("write_report") or {}
    rr = e.get("review_report") or {}
    issues = rr.get("issues")
    crit = sum(1 for i in issues if i.get("severity") == "critical") if isinstance(issues, list) else None
    state = ("완료(검토 끝)" if e.get("review") == "done" else
             "완료(작성자 자체 검토)" if e.get("write") == "done" and e.get("write_report", {}).get("verifier_clean") else
             "검토 중" if e.get("review") == "running" else
             "작성 완료, 검토 대기" if e.get("write") == "done" else
             "작성 중" if e.get("write") == "running" else
             "실패 — 다시 실행 필요" if "failed" in (e.get("write"), e.get("review")) else
             "파일만 있음(상태 불명)" if exists else "아직 시작 안 함")
    ver = rr.get("verifier_clean", wr.get("verifier_clean"))
    rows.append((cid, c["title"], state, f"{size} KB" if exists else "-",
                 "" if ver is None else ("깨끗함" if ver else "문제 있음"),
                 "" if issues is None else f"{len(issues)}개 (치명 {crit})",
                 ", ".join((wr.get("concerns") or [])[:2])[:160] + (" / " if (wr.get("concerns") and rr.get("remaining_concerns")) else "") + ", ".join((rr.get("remaining_concerns") or [])[:2])[:160]))
prog["_updated"] = now.isoformat(timespec="seconds")
json.dump(prog, open(pfile, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

md = ["# STATUS — C/C++ 코딩 노트 진행 상황 (자동 생성)", "",
      f"- 마지막 갱신: {now.strftime('%Y-%m-%d %H:%M')} (KST)",
      f"- 챕터 34개 중 작성 완료 {nw}개, 검토까지 완료 {nr}개",
      f"- 게시된 노트(artifact): {art.get('url', '아직 게시 전')}" + (f"  (slug `{art['slug']}`)" if art.get('slug') else ""),
      "- 이 표는 tools/status.py가 workflow 기록(journal)과 chapters/ 파일로 만든다. 새 세션에서는 state/progress.json의 마지막 기록을 이어받는다.",
      "- '완료(검토 끝)'이 아닌 챕터는 HANDOFF.md의 '이어서 하는 법'대로 다시 돌리면 된다.", "",
      "| id | 제목 | 상태 | 파일 | 검증기 | 검토에서 찾은 문제 | 메모 |", "|---|---|---|---|---|---|---|"]
for r in rows:
    md.append("| " + " | ".join(x.replace("|", "/") for x in r) + " |")
open(os.path.join(ROOT, "STATUS.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print(f"written={nw} reviewed={nr} -> STATUS.md")
