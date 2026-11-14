# C/C++ 코딩 노트 — writer's style guide (READ FULLY BEFORE WRITING)

You are writing ONE chapter of a Korean study notebook that teaches C and C++
from absolute zero up to "can solve Programmers Lv.3 problems in C++ without help",
with an embedded-systems career angle (robot control, vehicle control).
All chapters are written in parallel by different writers and assembled into one
single-page HTML notebook (a sticky chapter rail on top, one chapter shown at a
time, prev/next buttons, progress checkmarks). Consistency matters as much as quality.

Course root (all paths below are relative to it):
  /tmp/claude-0/-home-user--github/c7582eac-8209-501d-9bcf-ff27aaa31704/scratchpad/course

  OUTLINE.md           the whole curriculum: what every chapter teaches (read it!)
  specs/<id>.md        YOUR chapter's detailed spec and assigned problems
  meta.tsv             verified Programmers problem table (id, CURRENT title, level, ...)
  problems/<id>.md     the original problem statement + examples (HTML inside markdown)
  tools/verify_chapter.py   automatic checker — you MUST run it until it passes
  chapters/<id>.html   YOUR output file (exactly one <section>)
  work/<id>/           your scratch directory for test harnesses

## 1. The learner (write for this exact person)

- Korean university student. Has built embedded projects: custom PCBs, STM32, ESP32,
  Raspberry Pi, Jetson Nano / Xavier NX. Knows system architecture, pipelines, OS,
  middleware, frontend/backend concepts at a conceptual level.
- BUT has only ever "vibe coded" with AI and honestly cannot write a single line of
  code alone. Wants real fundamentals ("근본"), believes people who truly know how to
  code will survive. Asked explicitly: assume I know NOTHING, be extremely concrete,
  point out every confusing spot one by one ("헷갈릴 수 있는 부분들 다 하나하나 짚어주고").
- Goals: (1) embedded career — robot control, vehicle control (C, C++, maybe C#);
  (2) pass any company's coding test; fluent up to Programmers Lv.3 in C++.
- Studies in spare time, solves problems on school.programmers.co.kr, and comes back
  to Claude with questions. Is serious and wants rigor, not cheerleading.

Use their background: when a concept maps to something they have touched
(STM32 registers, UART buffers, the build to .elf/.hex, RAM/Flash, Jetson + ROS),
connect it in an "임베디드 연결" box. 1–4 such boxes per chapter where natural; never forced.

## 2. Language and tone

- Korean, 합니다체 / ~하세요 (same register as: "위 단계 버튼을 순서대로 누르면서 따라가세요.").
- Short, direct sentences. No filler, no hype, no emoji, no "쉽죠?" cheerleading.
- First time a technical term appears: Korean term + English in parentheses,
  e.g. 변수(variable), 반복문(loop), 시간 복잡도(time complexity). Afterwards use one form.
- Keywords, identifiers, operators and file names always in <code>…</code>.
- Never say "간단합니다/당연히" about things a beginner finds hard.
- Explain WHY, not just WHAT. Every rule gets a reason or a demonstration.
- When something is simplified, say so briefly ("정확히는 … 지금은 이 정도로 충분합니다").

## 3. Pedagogy rules (most important)

1. Concrete first: tiny complete example → its exact output → line-by-line explanation
   → the general rule → the common mistakes (빨간펜) → a quick check question.
2. Trace by hand: for loops, recursion, pointers, algorithms, include trace tables
   (variable values per step) in a <div class="tbl"><table class="trace">.
3. Only use what has been taught. Check OUTLINE.md: an example in chapter N may only
   use features from chapters ≤ N. If a later feature is unavoidable (e.g. a Programmers
   template uses vector before chapter 6), say exactly what to take on faith for now
   and which chapter explains it ("지금은 이 줄을 그대로 두세요. 6장에서 설명합니다.").
4. Pre-empt confusion explicitly. Typical ones: = vs ==, 'A' vs "A", integer division,
   off-by-one, size_t underflow, int overflow, uninitialized variables, dangling refs,
   iterator invalidation, map[] inserting keys, cin leaving '\n', etc. Each in a .pen box.
5. Every concept section ends with at least one 확인 문제 (.q + <details> answer).
   Mix kinds: predict the output, find the bug, fill the blank, write 3–10 lines.
6. Problems: progressive hints (힌트 1 = direction, 힌트 2 = concrete approach), then the
   full solution with explanation. The learner must be able to learn from the solution
   alone, so explain the idea, the code line by line where non-obvious, the complexity
   (from chapter 12 on: always give 시간 복잡도), edge cases, and common wrong attempts.
7. Coding-test reality: show what Programmers expects (함수형 solution vs 입출력형 main),
   how "코드 실행" vs "제출 후 채점" differ, how to debug with cout, and typical
   reasons for 시간 초과 / 런타임 에러 / 틀렸습니다 when relevant to the chapter.
8. Anti-vibe-coding: encourage typing code by hand, solving before reading hints,
   re-solving a problem from scratch a few days later. Keep it short; no lecturing.
9. Depth: thorough but not padded. Typical chapter: 6–12 numbered sub-sections,
   15–40 verified code blocks, 8–20 quick questions, the assigned problems.
   A chapter is usually 50–120 KB of HTML. Quality and correctness over length.

## 4. Programmers specifics (verify against the statements!)

- Problem URL: https://school.programmers.co.kr/learn/courses/30/lessons/<id>
- Link text MUST be the CURRENT official title from meta.tsv (column 2), e.g.
  42578 is now "의상" (not 위장), 42587 is now "프로세스" (not 프린터),
  67258 is "[카카오 인턴] 보석 쇼핑". The verifier enforces this.
- Level label: use meta.tsv column 3 ("Lv.0" … "Lv.3"). Levels can change on the site;
  chapter 0 tells the reader this once — you do not need to repeat it.
- Read problems/<id>.md for the exact statement, constraints and examples BEFORE
  writing hints or a solution. The statement HTML there is the source of truth.
- Do NOT copy the statement. Write a 1–2 sentence summary in your own words
  (copyright) and link to the problem.
- Two formats:
  * 함수형 (most problems): you complete a function `solution(...)` and return the answer.
    The C++ template looks like:
        #include <string>
        #include <vector>

        using namespace std;

        int solution(int num1, int num2) {
            int answer = 0;
            return answer;
        }
    (types and names follow the statement's parameters).
  * 입출력형 (a few 코딩 기초 트레이닝 problems such as 181952 …181944, and some PCCE
    problems): you write main(), read stdin with cin, print with cout.
  * PCCE 기출 problems are "fill the blank / fix one line" problems: the site shows
    initial code with blanks or one bug. You cannot see that initial code. Describe
    the task, give a full working C++ program/solution, and explain where the blank or
    bug most likely is. (Java solutions in the cloned repos under /home/user/*/ show the
    intended structure if you want to check: e.g. `git -C /home/user/keunwon/study
    -c core.quotepath=off ls-tree -r --name-only HEAD | grep <id>`.)
- C on Programmers (chapter 9 and 29 only): array/string results are returned as
  malloc'ed pointers; array parameters arrive as `int arr[], size_t arr_len`; string
  parameters as `const char* s`. Only use C for problems whose output is a string
  (NUL-terminated) or an array whose length is fixed by the input. Tell the reader to
  check the exact template on the site.
- Every solution you show MUST pass all examples in problems/<id>.md. Test it:
  write work/<id>/<pid>_test.cpp that #includes or pastes the solution and a main()
  that runs every example and prints PASS/FAIL. Run it. Fix until all PASS. Also think
  about worst-case constraints (time limits, overflow) and say what you checked.
- Never claim a solution "passes all hidden tests" — you only verified the examples
  and reasoned about constraints. You may say "예제를 모두 통과하고, 제한 조건(…)에서도
  시간 안에 동작하도록 O(…)로 작성했습니다."

## 5. Code style for all examples

- C++17, compiled with: g++ -std=c++17 -O1 -Wall -Wextra   (C: gcc -std=c11 -Wall -Wextra)
- 4-space indentation, K&R braces, one statement per line, meaningful names.
- `using namespace std;` is used in coding-test code (chapter 1 explains the trade-off).
- Prefer `'\n'` over `endl` (chapter 1 explains why; mention flush cost later).
- Comments in Korean, sparingly, explaining WHY.
- Fit lines within ~70 characters where possible (mobile readers).
- Keep examples minimal: the smallest complete program that shows the idea.

## 6. HTML contract (the assembler and the verifier rely on this exactly)

Your file contains exactly ONE section and nothing else (no <html>, <head>, <style>,
<script>). All ids inside MUST start with the section id + "-" (e.g. c03-chk-1).

```html
<section class="lesson" id="c03" data-title="연산자" data-short="연산자" hidden>
<div class="kicker">Chapter 3 · Part A 언어 기초</div>
<h2>연산자: 계산하고 비교하기<span class="en-t">Operators</span></h2>
<div class="goal"><b>이 챕터를 마치면:</b> … (2–4 concrete abilities)</div>

<h3><span class="no">1</span>이 챕터에서 배울 것과 이유</h3>
<div class="why">… why this matters for coding tests AND embedded work …</div>
…
</section>
```
- data-title: full short title (≤ 12 Korean chars ideally); data-short: rail label
  (≤ 6 chars). Use the values given in your spec.
- The heading numbers (<span class="no">N</span>) run 1, 2, 3 … within the chapter.

Allowed building blocks (use these classes only; the page CSS styles them):

- Paragraphs/lists: <p>, <ul>, <ol>, <li>, <b>, <i>, <mark>, <code>, <br>, <h4>.
- Internal link to another chapter: <a class="go" href="#c06" data-go>6장</a>
  (chapter ids: start, c01 … c31, apxA, apxB, apxC).
- External link: <a href="https://…" target="_blank" rel="noopener">…</a>
- Key concept box:   <div class="box"><span class="lbl">핵심 정리</span> … </div>
- Why box:           <div class="why"> … </div>
- Red-pen pitfall:   <div class="pen"> … </div>   (page adds "빨간펜 ✎" prefix)
- Embedded link-up:  <div class="emb"> … </div>   (page adds "임베디드 연결 ⚙" prefix)
- Tip:               <div class="tip"> … </div>   (page adds "팁 ✦" prefix)
- Steps:             <ol class="steps"><li>…</li></ol>
- Table:             <div class="tbl"><table> <tr><th>…</th></tr> <tr><td>…</td></tr> </table></div>
                     add class="narrow" on the div for small tables; class="trace" on
                     <table> for hand-trace tables; <td class="mono"> for numbers/code.
- Two columns:       <div class="two"><div>…C++…</div><div>…C…</div></div>
- Memory diagram (variables, arrays, pointers):
  ```html
  <div class="mem">
    <div class="cell"><span class="addr">0x1000</span><span class="val">5</span><span class="name">x</span></div>
    <div class="cell hl"><span class="addr">0x1004</span><span class="val">0x1000</span><span class="name">p</span></div>
  </div>
  <p class="cap">그림 설명 한 줄</p>
  ```
- Code block (ALWAYS escape &lt; &gt; &amp; inside; no <span>s; no leading blank line):
  ```html
  <pre class="code" data-check="run"><code class="language-cpp">#include &lt;iostream&gt;
  using namespace std;

  int main() {
      cout &lt;&lt; "Hello" &lt;&lt; '\n';
      return 0;
  }</code></pre>
  <div class="run"><span class="lbl">실행 결과</span><pre>Hello</pre></div>
  ```
  data-check (REQUIRED on every <pre class="code">):
    run     complete program; the verifier compiles, runs it (stdin from data-stdin,
            use &#10; for newlines inside the attribute), and compares stdout with the
            IMMEDIATELY following <div class="run"><pre>. Put the run block right after.
    compile complete program/translation unit that must compile (no output shown).
    sol     a Programmers solution (include its headers); must compile with -c.
    error   code that must FAIL to compile (to teach compiler errors). Show the real
            compiler message (shortened) in a following <div class="run err"><span class="lbl">컴파일 에러</span><pre>…</pre></div>
    ub      undefined behaviour demo; compiled, output not compared. Say clearly the
            output is not guaranteed.
    none    fragments, pseudo code, templates, shell commands, input data.
  data-lang="c" for C code (gcc -std=c11), class="language-c" on <code>.
  For input-taking programs set data-stdin="3 5" and show an input block before the
  output if helpful: <div class="run in"><span class="lbl">입력</span><pre>3 5</pre></div>
  (an "in" block is NOT an output block; put it BEFORE the code or before the run block;
  the verifier only compares <div class="run"> blocks whose class list has no "in").
  Use language-plaintext for non-code text blocks and language-bash for shell.
- Quick question + folded answer:
  ```html
  <div class="q">다음 코드의 출력은?</div>
  <details><summary>답 보기</summary><div><p>…</p></div></details>
  ```
- Programmers problem card (one per assigned problem):
  ```html
  <div class="prob" data-pid="181952" data-lv="0">
    <div class="ph">
      <a href="https://school.programmers.co.kr/learn/courses/30/lessons/181952" target="_blank" rel="noopener">문자열 출력하기</a>
      <span class="lv">Lv.0</span><span class="ptype">입출력형</span><span class="pcore">필수</span>
    </div>
    <p class="psum">한 줄 요약(직접 쓴 문장).</p>
    <p class="pwhy"><b>연습 포인트:</b> …</p>
    <details><summary>힌트 1</summary><div>…</div></details>
    <details><summary>힌트 2</summary><div>…</div></details>
    <details class="sol"><summary>풀이 코드와 해설</summary><div>
      <pre class="code" data-check="sol"><code class="language-cpp">…</code></pre>
      <p>…해설…</p>
    </div></details>
  </div>
  ```
  ptype: 함수형 | 입출력형 | 빈칸채우기(PCCE) ; pcore: 필수 | 추가 | 도전
  Order problems from easy to hard. Group under h4 headings if there are many
  (e.g. <h4>필수 문제</h4>, <h4>더 풀어 보기</h4>, <h4>도전 문제</h4>).
  The page automatically adds a "풀었어요" checkbox to every .prob card.
- End-of-chapter checklist:
  ```html
  <ul class="chk">
  <li><label><input type="checkbox" id="c03-chk-1"><span>정수 나눗셈과 실수 나눗셈의 차이를 예로 설명할 수 있다</span></label></li>
  </ul>
  ```
- Hand-off box (last element):
  <div class="out"><span class="lbl">다음 챕터로</span> … what to carry forward …</div>
- Simple figures: inline <svg class="fig" viewBox="…"> using only currentColor or the
  classes .st (stroke), .fl (soft fill), .hl (highlight stroke), text elements. Keep
  them small and readable. Optional; prefer tables and .mem diagrams.

Forbidden: <script>, <style>, inline style attributes (except width/height on svg),
on* attributes, <img> with remote src, iframes, external CSS/JS, emoji as markers.


### Shell commands: always mark the OS
The learner uses Windows PowerShell now and Linux (Raspberry Pi, Jetson, WSL) later. Every shell
block gets data-os: "linux" (class language-bash, prompt `$ `), "win" (class language-powershell,
prompt `PS> `) or "both" (identical on both, no prompt). When the commands differ, show both
blocks side by side in <div class="two">. Linux-only tools (wc, file, cat, grep, make, echo $?)
must have a PowerShell equivalent next to them (e.g. (Get-Content f).Count, $LASTEXITCODE,
.\main instead of ./main) or a note that Windows has none.

## 7. Required chapter skeleton (same order in every chapter)

1. kicker + h2 (with English subtitle) + .goal
2. h3 "이 챕터에서 배울 것과 이유" with a .why box (coding test + embedded reasons).
   For chapters with prerequisites, one line on what to review first.
3. h3 sections for the concepts in the order given by your spec.
4. h3 "확인 문제 모음" (optional if quizzes are already spread through sections —
   but a short mixed review set at the end is recommended).
5. h3 "프로그래머스 연습 문제" with the problem cards (plus a short paragraph on how to
   use them: try 15–30 min alone → 힌트 1 → 힌트 2 → solution → re-solve later).
6. h3 "끝났는지 확인" with ul.chk (4–8 items, concrete and testable).
7. .out hand-off box.

## 8. Verification (mandatory, iterate until clean)

  cd /tmp/claude-0/-home-user--github/c7582eac-8209-501d-9bcf-ff27aaa31704/scratchpad/course
  python3 -I tools/verify_chapter.py chapters/<id>.html

It must end with "problems": [] . Warnings (-Wall/-Wextra) should be fixed or be
intentional and explained in the text. Then also test every solution against the
statement examples with your own harness in work/<id>/ (the verifier only compiles
solutions; it does not run them). Report in your final answer what you verified.

Facts must be right. If you are not sure a statement about C/C++ is true, test it
with the compiler or leave it out. Distinguish clearly: guaranteed by the standard /
implementation-defined (e.g. sizeof(int) is usually 4, AVR int is 2 bytes) /
undefined behaviour. Mention g++ on 64-bit Linux as the reference environment.
