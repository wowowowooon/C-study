# -*- coding: utf-8 -*-
"""Save progress: mirror the course dir into the git repo (cpp-notes/), commit, push.

Usage:  python3 -I tools/checkpoint.py [--msg "c01 written"] [--no-push]
Env:    COURSE_REPO_DIR  (default /home/user/.github)
        COURSE_BRANCH    (default claude/adoring-brown-d1m978)
        COURSE_COAUTHOR  (default "Claude Opus 5.5 <noreply@anthropic.com>")
Never copies problems/, problems_txt/ (third-party statements), work/ or repos_cache/.
"""
import fcntl, os, shutil, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.environ.get("COURSE_REPO_DIR", "/home/user/c-c-study")
BRANCH = os.environ.get("COURSE_BRANCH", "main")
COAUTHOR = os.environ.get("COURSE_COAUTHOR", "Claude Opus 5.5 <noreply@anthropic.com>")
SESSION = "https://claude.ai/code/session_018JUNShtbkDhHCLT7XL2FAF"
DST = REPO   # the whole repo is the course
SKIP = {"problems", "problems_txt", "work", "__pycache__", "repos_cache", ".git", "backup"}
args = sys.argv[1:]
msg = args[args.index("--msg") + 1] if "--msg" in args else "checkpoint"
push = "--no-push" not in args

lock = open("/tmp/cpp-notes-checkpoint.lock", "w")
fcntl.flock(lock, fcntl.LOCK_EX)
subprocess.run([sys.executable, "-I", os.path.join(HERE, "status.py")], check=False)

def same(a, b):
    try:
        return os.path.getsize(a) == os.path.getsize(b) and open(a, "rb").read() == open(b, "rb").read()
    except OSError:
        return False

def mirror(src, dst):
    keep = set()
    for d, dirs, files in os.walk(src):
        rel = os.path.relpath(d, src)
        dirs[:] = [x for x in dirs if x not in SKIP]
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            if f.endswith((".pyc", ".swp", ".lock")):
                continue
            s, t = os.path.join(d, f), os.path.normpath(os.path.join(dst, rel, f))
            keep.add(t)
            if not same(s, t):
                shutil.copy2(s, t)
    for d, dirs, files in os.walk(dst, topdown=False):
        if os.sep + ".git" in d + os.sep or d.endswith(".git"):
            continue
        for f in files:
            t = os.path.normpath(os.path.join(d, f))
            if t not in keep:
                os.remove(t)
        if d != dst and not os.listdir(d):
            os.rmdir(d)

has_head = subprocess.run(["git", "-C", REPO, "rev-parse", "--verify", "-q", "HEAD"], capture_output=True).returncode == 0
probe = subprocess.run(["git", "-C", REPO, "push", "--dry-run", "-q", "origin", f"HEAD:refs/heads/{BRANCH}"],
                       capture_output=True, text=True)
if has_head and probe.returncode != 0:
    print("checkpoint: no GitHub push permission (" + (probe.stderr.strip().splitlines() or ["?"])[-1][:120] + ")")
    print("checkpoint: skipped git (nothing committed). Durable copy = backup artifact; files stay in", ROOT)
    sys.exit(0)

if os.path.realpath(ROOT) != os.path.realpath(DST):
    mirror(ROOT, DST)

def git(*a, check=True):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True, check=check)

git("add", "-A")
if git("diff", "--cached", "--quiet", check=False).returncode == 0:
    print("checkpoint: nothing new to commit")
else:
    git("commit", "-q", "-m", f"cpp-notes: {msg}\n\nCo-Authored-By: {COAUTHOR}\nClaude-Session: {SESSION}\n")
    print("checkpoint: committed:", msg)
if push:
    for wait in (0, 2, 4, 8, 16):
        if wait:
            time.sleep(wait)
        p = git("push", "-q", "-u", "origin", BRANCH, check=False)
        if p.returncode == 0:
            print("checkpoint: pushed to", BRANCH)
            break
        print("checkpoint: push failed:", p.stderr.strip()[:200])
        if "access" in p.stderr or "permission" in p.stderr.lower() or "403" in p.stderr:
            print("checkpoint: no push permission - work is committed locally only")
            break
