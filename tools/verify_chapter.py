#!/usr/bin/env python3
"""Verify one chapter fragment of the C/C++ course notebook.

Usage:  python3 -I verify_chapter.py <chapter.html> [--keep] [--quiet]

Checks
  1. HTML structure: exactly one <section class="lesson">, balanced tags,
     unique ids (all ids must start with the section id + '-'),
     no <script>/<style>/<iframe>/<img src=http...>, no inline event handlers.
  2. Every <pre class="code"> block carries a data-check attribute and is
     compiled according to it:
        run      complete program; compiled, run (stdin = data-stdin), and its
                 stdout must equal the text of the NEXT <div class="run"> <pre>.
        compile  complete translation unit; must compile without errors.
        sol      Programmers solution (must include its own headers);
                 must compile (-c). Test it separately with a harness.
        error    must FAIL to compile (used to show compiler errors).
        ub       compiles; output is not checked (undefined behaviour demo).
        none     not compiled (fragments, pseudo code, shell, output).
     data-lang="c" compiles with gcc -std=c11, otherwise g++ -std=c++17.
     Warnings from -Wall -Wextra are reported (not fatal) so you can decide.
  3. Programmers links: every link to school.programmers.co.kr/.../lessons/ID
     must use an ID that exists in meta.tsv, and the link text must equal the
     official title (whitespace/fullwidth-insensitive).
Exit code 0 = all good, 1 = problems found.
"""
import html
import html.parser
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(os.path.dirname(HERE), "meta.tsv")

VOID = {"br", "hr", "img", "input", "meta", "link", "wbr", "col", "source"}
CHECKS = {"run", "compile", "sol", "error", "ub", "none"}


def norm_title(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", "", s)
    return s


def load_meta():
    meta = {}
    if not os.path.exists(META):
        return meta
    with open(META, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                meta[parts[0]] = parts[1]
    return meta


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.ids = []
        self.sections = []
        self.blocks = []          # dicts for <pre class=code>
        self.runs = []            # (order, text) for <div class=run><pre>
        self.order = 0
        self.links = []           # (href, text)
        self._in_pre = None
        self._in_run_div = 0
        self._run_pre = None
        self._link = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "iframe", "object", "embed"):
            self.errors.append(f"forbidden tag <{tag}> at line {self.getpos()[0]}")
        if tag == "img" and re.match(r"https?:", a.get("src", "") or ""):
            self.errors.append(f"remote image at line {self.getpos()[0]}")
        for k in a:
            if k.startswith("on"):
                self.errors.append(f"inline event handler {k} at line {self.getpos()[0]}")
        if "id" in a:
            self.ids.append((a["id"], self.getpos()[0]))
        cls = (a.get("class") or "").split()
        if tag == "section" and "lesson" in cls:
            self.sections.append(a)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0], cls))
        if tag == "pre" and "code" in cls:
            self.order += 1
            self._in_pre = {"attrs": a, "line": self.getpos()[0], "text": [], "order": self.order}
        elif tag == "pre" and self._in_run_div and self._run_pre is None:
            self._run_pre = []
        if tag == "div" and "run" in cls and "in" not in cls and "err" not in cls:
            self._in_run_div += 1
            self.order += 1
            self._run_order = self.order
        if tag == "a":
            self._link = [a.get("href", ""), []]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at line {self.getpos()[0]}")
            return
        top, line, cls = self.stack[-1]
        if top != tag:
            # try to recover: find matching open tag
            idx = None
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    idx = i
                    break
            if idx is None:
                self.errors.append(f"stray </{tag}> at line {self.getpos()[0]} (open: <{top}> from line {line})")
                return
            unclosed = [f"<{t}> (line {l})" for t, l, _ in self.stack[idx + 1:]]
            self.errors.append(f"unclosed {', '.join(unclosed)} before </{tag}> at line {self.getpos()[0]}")
            self.stack = self.stack[:idx + 1]
            top, line, cls = self.stack[-1]
        self.stack.pop()
        if tag == "pre" and self._in_pre is not None and "code" in cls:
            b = self._in_pre
            b["text"] = "".join(b["text"])
            self.blocks.append(b)
            self._in_pre = None
        elif tag == "pre" and self._run_pre is not None:
            self.runs.append((self._run_order, "".join(self._run_pre)))
            self._run_pre = None
        if tag == "div" and "run" in cls and "in" not in cls and "err" not in cls:
            self._in_run_div -= 1
        if tag == "a" and self._link is not None:
            self.links.append((self._link[0], "".join(self._link[1]).strip()))
            self._link = None

    def handle_data(self, data):
        if self._in_pre is not None:
            self._in_pre["text"].append(data)
        if self._run_pre is not None:
            self._run_pre.append(data)
        if self._link is not None:
            self._link[1].append(data)


def clean_out(s):
    lines = s.replace("\r\n", "\n").split("\n")
    lines = [l.rstrip() for l in lines]
    while lines and lines[-1] == "":
        lines.pop()
    while lines and lines[0] == "":
        lines.pop(0)
    return "\n".join(lines)


def compile_src(src, lang, workdir, name, mode):
    ext = "c" if lang == "c" else "cpp"
    path = os.path.join(workdir, f"{name}.{ext}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    exe = os.path.join(workdir, name)
    if lang == "c":
        cmd = ["gcc", "-std=c11", "-O1", "-Wall", "-Wextra", path, "-o", exe, "-lm"]
    else:
        cmd = ["g++", "-std=c++17", "-O1", "-Wall", "-Wextra", path, "-o", exe]
    if mode == "syntax":
        cmd = [c for c in cmd if c not in ("-o", exe, "-lm")]
        cmd.insert(1, "-c")
        cmd += ["-o", os.devnull]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return p.returncode, p.stderr, exe


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keep = "--keep" in sys.argv
    quiet = "--quiet" in sys.argv
    if not args:
        print(__doc__)
        sys.exit(2)
    path = args[0]
    src = open(path, encoding="utf-8").read()
    p = Parser()
    p.feed(src)
    p.close()
    problems = list(p.errors)
    warnings = []
    if p.stack:
        problems.append("unclosed at EOF: " + ", ".join(f"<{t}> (line {l})" for t, l, _ in p.stack))
    if len(p.sections) != 1:
        problems.append(f"expected exactly one <section class=\"lesson\">, found {len(p.sections)}")
    sec_id = p.sections[0].get("id", "") if p.sections else ""
    for k in ("id", "data-title", "data-short"):
        if p.sections and not p.sections[0].get(k):
            problems.append(f"section is missing {k}")
    seen = {}
    for i, line in p.ids:
        if i in seen:
            problems.append(f"duplicate id '{i}' (lines {seen[i]} and {line})")
        seen[i] = line
        if sec_id and i != sec_id and not i.startswith(sec_id + "-"):
            problems.append(f"id '{i}' (line {line}) must start with '{sec_id}-'")

    # Programmers links
    meta = load_meta()
    for href, text in p.links:
        m = re.search(r"programmers\.co\.kr/learn/courses/30/lessons/(\d+)", href)
        if not m:
            continue
        pid = m.group(1)
        if pid not in meta:
            problems.append(f"Programmers id {pid} ('{text}') is not in meta.tsv - unverified problem")
        elif text and norm_title(text) != norm_title(meta[pid]):
            problems.append(f"Programmers id {pid}: link text '{text}' != official title '{meta[pid]}'")

    # code blocks
    runs = sorted(p.runs)
    workdir = tempfile.mkdtemp(prefix="vc_")
    results = []
    for n, b in enumerate(p.blocks, 1):
        a = b["attrs"]
        chk = a.get("data-check")
        lang = a.get("data-lang", "cpp")
        line = b["line"]
        code = b["text"]
        tag = f"block#{n} (line {line}, data-check={chk})"
        if chk not in CHECKS:
            problems.append(f"{tag}: missing/invalid data-check (use one of {sorted(CHECKS)})")
            continue
        if chk == "none":
            results.append((tag, "skip"))
            continue
        if code.startswith("\n"):
            code = code[1:]
        if chk == "error":
            rc, err, _ = compile_src(code, lang, workdir, f"b{n}", "syntax")
            if rc == 0:
                problems.append(f"{tag}: expected a compile error but it compiled")
            else:
                first = next((l for l in err.splitlines() if "error" in l), err.splitlines()[0] if err else "")
                results.append((tag, "error-ok: " + first.split(f"b{n}.", 1)[-1][:160]))
            continue
        mode = "syntax" if chk in ("compile", "sol") else "build"
        rc, err, exe = compile_src(code, lang, workdir, f"b{n}", mode)
        if rc != 0:
            problems.append(f"{tag}: compile failed:\n" + "\n".join(err.splitlines()[:12]))
            continue
        w = [l for l in err.splitlines() if "warning" in l]
        if w:
            warnings.append(f"{tag}: " + " | ".join(x.split(f"b{n}.", 1)[-1][:140] for x in w[:4]))
        if chk in ("compile", "sol"):
            results.append((tag, "compiled"))
            continue
        stdin = a.get("data-stdin", "")
        try:
            r = subprocess.run([exe], input=stdin, capture_output=True, text=True, timeout=10)
        except subprocess.TimeoutExpired:
            problems.append(f"{tag}: program timed out (10 s)")
            continue
        if chk == "ub":
            results.append((tag, "ub-compiled"))
            continue
        nxt = [t for (o, t) in runs if o > b["order"]]
        if not nxt:
            problems.append(f"{tag}: data-check=run but no following <div class=\"run\"><pre> output block")
            continue
        # the run block must be the very next 'ordered' element after this pre
        following_orders = [o for (o, _) in runs if o > b["order"]]
        next_pre_orders = [x["order"] for x in p.blocks if x["order"] > b["order"]]
        if next_pre_orders and following_orders and next_pre_orders[0] < following_orders[0]:
            problems.append(f"{tag}: the next output block belongs to a later code block - add a <div class=\"run\"> right after this code")
            continue
        expected = clean_out(nxt[0])
        actual = clean_out(r.stdout)
        if expected != actual:
            problems.append(f"{tag}: output mismatch\n--- shown in note ---\n{expected}\n--- actual ---\n{actual}")
        else:
            results.append((tag, "output-ok"))
    if not keep:
        subprocess.run(["rm", "-rf", workdir])
    summary = {
        "file": path,
        "section": sec_id,
        "code_blocks": len(p.blocks),
        "checked": sum(1 for _, s in results if s != "skip"),
        "skipped(none)": sum(1 for _, s in results if s == "skip"),
        "programmers_links": sum(1 for h, _ in p.links if "programmers.co.kr" in h),
        "problems": problems,
        "warnings": warnings,
    }
    if not quiet:
        for t, s in results:
            print(f"  ok  {t}: {s}")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
