export const meta = {
  name: 'cpp-notes-chapters',
  description: 'Write chapters of the Korean C/C++ study notebook, verify them, and save each one to git',
  phases: [
    { title: 'Write', detail: 'one writer per chapter: code compiled, solutions tested, self-reviewed, saved to git' },
    { title: 'Review', detail: 'optional adversarial editor pass (args.review = true)' },
  ],
}

const ROOT = (args && args.root) || '/tmp/claude-0/-home-user--github/c7582eac-8209-501d-9bcf-ff27aaa31704/scratchpad/course'
const DO_REVIEW = !!(args && args.review)

const WRITE_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    bytes: { type: 'integer' },
    h3_sections: { type: 'integer' },
    code_blocks: { type: 'integer' },
    quizzes: { type: 'integer' },
    problems_written: { type: 'array', items: { type: 'string' } },
    problems_dropped: {
      type: 'array',
      items: { type: 'object', properties: { pid: { type: 'string' }, reason: { type: 'string' } }, required: ['pid', 'reason'] },
    },
    solutions_all_examples_pass: { type: 'boolean' },
    verifier_clean: { type: 'boolean' },
    saved_to_git: { type: 'boolean' },
    concerns: { type: 'array', items: { type: 'string' } },
  },
  required: ['id', 'bytes', 'problems_written', 'solutions_all_examples_pass', 'verifier_clean', 'saved_to_git', 'concerns'],
}

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
          kind: { type: 'string' },
          summary: { type: 'string' },
        },
        required: ['severity', 'summary'],
      },
    },
    verifier_clean: { type: 'boolean' },
    bytes: { type: 'integer' },
    remaining_concerns: { type: 'array', items: { type: 'string' } },
  },
  required: ['id', 'issues', 'verifier_clean', 'bytes', 'remaining_concerns'],
}

function writerPrompt(id) {
  return `You are writing ONE chapter of a Korean study notebook that teaches C/C++ from absolute zero up to solving Programmers Lv.3 problems in C++, for a learner who wants an embedded career (robot control, vehicle control). Your chapter id: ${id}.

Course root: ${ROOT}

Read first (once each; do not re-read files you have already read):
  1. ${ROOT}/STYLE.md — the contract: learner profile, tone, pedagogy rules, the exact HTML building blocks, Programmers specifics, verification. Follow it exactly. Where STYLE.md tells you to read OUTLINE.md, read ${ROOT}/OUTLINE_SHORT.md instead, and open OUTLINE.md only for the chapters right before and after yours.
  2. ${ROOT}/specs/${id}.md — what your chapter must teach (in order), its identity values, the confusions to address, embedded connections, and the assigned problems.
  3. ${ROOT}/OUTLINE_SHORT.md — one-screen map of the curriculum: what earlier chapters taught and what later ones will. Only use language features taught up to your chapter; if something later is unavoidable, say so explicitly in the text.
  4. For every assigned problem: ${ROOT}/problems_txt/<problem id>.txt (plain-text statement with constraints and examples; if missing, ${ROOT}/problems/<problem id>.md). Read it before writing hints or a solution.

Write ${ROOT}/chapters/${id}.html containing exactly one <section class="lesson" id="${id}" ...>. Write it in a few large Write/Edit steps (section by section is fine). Every <pre class="code"> needs data-check; every runnable example's output block must be the program's real output.

Verification (mandatory):
  - Test every Programmers solution against ALL examples in its statement with a harness in ${ROOT}/work/${id}/ (C++: g++ -std=c++17 -Wall -Wextra; C: gcc -std=c11 -Wall -Wextra). All must PASS. Think about worst-case constraints (time, overflow, minimal or empty input); from chapter 12 on, always state the time complexity.
  - python3 -I ${ROOT}/tools/verify_chapter.py ${ROOT}/chapters/${id}.html --quiet — iterate until it reports "problems": [] . Fix warnings unless they are intentional and explained in the text.

Self-review before finishing (you are also the editor; assume nobody else will check this chapter):
  A. Technical truth: every claim about C/C++ semantics, types and sizes, undefined vs implementation-defined behaviour, STL behaviour and complexity, compiler messages. Test anything you are not sure of with the compiler; remove what you cannot verify.
  B. Every quiz answer and every shown output is right; each solution's explanation matches its code.
  C. Spec coverage: every topic in order, every listed confusion, the STYLE.md section 7 skeleton, every assigned problem with the CURRENT title from ${ROOT}/meta.tsv and the right level, pcore role and ptype.
  D. A total beginner can follow it: no feature used before it is taught without a note, no unexplained jargon, trace tables or memory diagrams where a beginner would get lost, solutions that explain the idea and not just the code. Natural Korean 합니다체.
  E. Finally read the finished chapter once from top to bottom as the learner would, and fix any gap.

Be economical: read each input once, rely on the verifier's output instead of re-reading the whole chapter repeatedly, and keep scratch output short (pipe long compiler output through head).

When the chapter is verified, save it to git (this protects the work if the session is interrupted):
  python3 -I ${ROOT}/tools/checkpoint.py --msg "${id}: chapter written and verified"

Only create or modify ${ROOT}/chapters/${id}.html and files under ${ROOT}/work/${id}/ (plus running the checkpoint script). Never touch other chapters or shared files.

Your final answer is data for the orchestrator, not text for the learner: fill the schema honestly and put anything unverified or doubtful in concerns.`
}

function reviewerPrompt(id, w) {
  const report = w ? JSON.stringify(w) : 'no report'
  return `You are the adversarial technical editor for chapter ${id} of a Korean study notebook that teaches C/C++ from absolute zero up to Programmers Lv.3, with an embedded-career angle. Another writer produced ${ROOT}/chapters/${id}.html. Assume it contains mistakes; find them and FIX them directly in the file, so the learner (who has never written code and will trust every word) learns only correct things.

Read first: ${ROOT}/STYLE.md, ${ROOT}/specs/${id}.md, ${ROOT}/OUTLINE_SHORT.md, the chapter, and ${ROOT}/problems_txt/<problem id>.txt for every problem card.
Writer's report (may be optimistic): ${report}

Check and fix in priority order: (A) technical truth — test doubtful claims with g++/gcc in ${ROOT}/work/${id}/review/; (B) re-test every solution against all statement examples, look for edge cases and worst-case failures; (C) spec coverage and current titles/levels from ${ROOT}/meta.tsv; (D) teaching quality for a total beginner; (E) HTML contract. Rewrite what needs rewriting, keep what is good, do not shorten good explanations.
Then run python3 -I ${ROOT}/tools/verify_chapter.py ${ROOT}/chapters/${id}.html --quiet until "problems": [] , and save: python3 -I ${ROOT}/tools/checkpoint.py --msg "${id}: reviewed"
Only modify ${ROOT}/chapters/${id}.html and files under ${ROOT}/work/${id}/.
Your final answer is data for the orchestrator.`
}

async function lane(ids) {
  const out = []
  for (const id of ids) {
    const w = await agent(writerPrompt(id), { label: `write:${id}`, phase: 'Write', schema: WRITE_SCHEMA })
    if (!w) {
      log(`${id}: writer failed (maybe a usage limit) — stopping this lane instead of retrying blindly`)
      out.push({ id, write: null, review: null })
      break
    }
    log(`${id} written: ${w.bytes} bytes, ${(w.problems_written || []).length} problems, verifier ${w.verifier_clean ? 'clean' : 'NOT clean'}, git ${w.saved_to_git ? 'saved' : 'NOT saved'}`)
    let r = null
    if (DO_REVIEW) {
      r = await agent(reviewerPrompt(id, w), { label: `review:${id}`, phase: 'Review', schema: REVIEW_SCHEMA })
      log(`${id} reviewed: ${r ? `${r.issues.length} issues fixed` : 'FAILED'}`)
    }
    out.push({ id, write: w, review: r })
  }
  return out
}

const lanes = (args && args.lanes) || []
const results = await parallel(lanes.map(ids => () => lane(ids)))
return results.filter(Boolean).flat()
