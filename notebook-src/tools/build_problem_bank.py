# -*- coding: utf-8 -*-
"""Rebuild problems/<id>.md for every id in meta.tsv, then problems_txt/ (via make_short.py).

Statements are NOT stored in git (third-party content). They are re-extracted from public
BaekjoonHub-style GitHub repos (folder 프로그래머스/<level>/<id>. <title>/README.md).
In a Claude Code cloud session you may need to call add_repo(owner, repo, access="read")
for each repo first (public repos are normally readable anonymously through the git proxy).

Usage: python3 -I tools/build_problem_bank.py [--cache DIR]
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPOS = ["kkangmen/problem_solving", "err-cho404/programmers-coding-test", "charles0304/baekjoonhub",
         "keunwon/study", "soggeum/coding-test", "nopicklesbigmac/programmers"]
args = sys.argv[1:]
cache = args[args.index("--cache") + 1] if "--cache" in args else os.path.join(ROOT, "repos_cache")
pat = re.compile(r"프로그래머스/(?:lv)?(\d)/(\d+)\.\s*([^/]+)/README\.md$")
meta = {}
for line in open(os.path.join(ROOT, "meta.tsv"), encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    p = line.rstrip("\n").split("\t")
    meta[p[0]] = p
os.makedirs(os.path.join(ROOT, "problems"), exist_ok=True)
need = {pid for pid in meta if not os.path.exists(os.path.join(ROOT, "problems", pid + ".md"))}
print("statements to fetch:", len(need))
env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")
for repo in REPOS:
    if not need:
        break
    d = os.path.join(cache, repo.replace("/", "__"))
    if not os.path.isdir(os.path.join(d, ".git")):
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout",
                        f"https://github.com/{repo}", d], env=env)
    out = subprocess.run(["git", "-C", d, "-c", "core.quotepath=off", "ls-tree", "-r", "--name-only", "HEAD"],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        m = pat.search(line)
        if not m or m.group(2) not in need:
            continue
        txt = subprocess.run(["git", "-C", d, "show", "HEAD:" + line], capture_output=True, text=True, env=env).stdout
        if "문제 설명" not in txt:
            continue
        pid = m.group(2)
        row = meta[pid]
        body = re.sub(r"### 성능 요약.*?(?=### 구분)", "", txt, flags=re.S)
        body = re.sub(r"### 채점결과.*?(?=### 문제 설명)", "", body, flags=re.S)
        hdr = f"<!-- problem bank: id={pid} title={row[1]} level={row[2]} (level source: {row[3]}) category={row[5]} statement-source={repo} -->\n"
        open(os.path.join(ROOT, "problems", pid + ".md"), "w", encoding="utf-8").write(hdr + body)
        need.discard(pid)
print("still missing:", sorted(need, key=int))
subprocess.run([sys.executable, "-I", os.path.join(HERE, "make_short.py")])
