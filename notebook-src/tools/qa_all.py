# -*- coding: utf-8 -*-
"""Run the verifier on every finished chapter and check spec coverage.
Usage: python3 -I qa_all.py [id ...]
"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from chapters_def import CH

want = [a for a in sys.argv[1:] if not a.startswith("-")]
rows = []
for c in CH:
    if want and c["id"] not in want:
        continue
    path = os.path.join(ROOT, "chapters", f"{c['id']}.html")
    if not os.path.exists(path):
        rows.append((c["id"], "MISSING", "", "", ""))
        continue
    p = subprocess.run([sys.executable, "-I", os.path.join(HERE, "verify_chapter.py"), path, "--quiet"],
                       capture_output=True, text=True, timeout=1800)
    try:
        js = json.loads(p.stdout[p.stdout.index("{"):])
    except Exception:
        rows.append((c["id"], "VERIFY-CRASH", p.stdout[-300:] + p.stderr[-300:], "", ""))
        continue
    html = open(path, encoding="utf-8").read()
    pids_in = set(re.findall(r'class="prob"[^>]*data-pid="(\d+)"', html)) | set(re.findall(r'data-pid="(\d+)"[^>]*class="prob"', html))
    assigned = [pid for _, pid, _ in c["problems"]]
    missing_p = [pid for pid in assigned if pid not in pids_in]
    extra_p = sorted(pids_in - set(assigned))
    h3 = len(re.findall(r"<h3\b", html))
    q = len(re.findall(r'class="q"', html))
    status = "OK" if not js["problems"] else f"{len(js['problems'])} PROBLEMS"
    rows.append((c["id"], status, f"{len(html.encode('utf-8'))//1024}KB h3={h3} code={js['code_blocks']} checked={js['checked']} q={q} warn={len(js['warnings'])}",
                 f"missing={missing_p}" if missing_p else "", f"extra={extra_p}" if extra_p else ""))
    if js["problems"]:
        for pr in js["problems"][:6]:
            print(f"  [{c['id']}] {pr[:300]}")
for r in rows:
    print(" | ".join(x for x in r if x != ""))
