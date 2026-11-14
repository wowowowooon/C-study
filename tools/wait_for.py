# -*- coding: utf-8 -*-
"""Block until every given chapter id has write == done/failed in the workflow journals (poll every 60 s).
Usage: python3 -I tools/wait_for.py start c01"""
import glob, json, re, sys, time
ids = set(a for a in sys.argv[1:] if not a.startswith("--"))
JG = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--journal=")), "/root/.claude/projects/*/*/subagents/workflows/*/journal.jsonl")
t0 = time.time()
while True:
    state = {}
    for jf in glob.glob(JG):
        try:
            rows = [json.loads(x) for x in open(jf, encoding="utf-8") if x.strip()]
            lab = {o["agentId"]: o.get("label") or "" for o in rows if o.get("type") == "started" and o.get("agentId")}
            for o in rows:
                m = re.match(r"write:([A-Za-z0-9]+)$", o.get("label") or lab.get(o.get("agentId"), ""))
                if not m or m.group(1) not in ids:
                    continue
                if o.get("type") == "result":
                    state[m.group(1)] = "done" if o.get("result") else "failed"
                elif o.get("type") and ("err" in o["type"] or "fail" in o["type"]):
                    state.setdefault(m.group(1), "failed")
        except Exception:
            pass
    fresh = {k: v for k, v in state.items() if k in ids}
    if len(fresh) == len(ids) and time.time() - t0 > 30:
        print(json.dumps(fresh, ensure_ascii=False))
        break
    time.sleep(60)
