# HANDOFF — C/C++ 코딩 노트 제작 인수인계

세션이 끊기거나 모델이 바뀌어도 이 문서 하나로 이어서 작업할 수 있게 정리했습니다. 진행 상황은 같은 폴더의 `STATUS.md`(자동 생성)에 있습니다.

## 1. 무엇을 만드는가
- **사용자**: 임베디드 경험(PCB 제작, STM32, ESP32, 라즈베리파이, 젯슨 나노/NX)과 시스템 구조 지식은 있지만, AI로 바이브코딩만 해서 코드를 직접 한 줄도 못 쓰는 대학생. 기초부터 제대로 배우고 싶어 함.
- **목표**: 임베디드(로봇 제어, 차량 제어) 취업. C/C++(필요하면 C#)를 기초부터 배워 어느 기업 코딩테스트든 통과, 프로그래머스 Lv.3까지 막힘없이.
- **요청한 형식**: 사용자가 보낸 artifact "스프링·캠 설계 노트"(https://claude.ai/artifact/BcfieVsNQonViik75n4N2J)와 같은 노트 — 위쪽 단계 버튼, 한 번에 한 단계, 파란 개념 상자, 빨간펜 주의, 접히는 답, 체크리스트. 챕터별로 나누고, 챕터마다 좋은 프로그래머스 문제(https://school.programmers.co.kr/learn/challenges)를 넣어 실전 감각을 기르게. "하나도 모른다고 생각하고 정말정말 구체적으로, 헷갈리는 부분 하나하나 짚어서".
- **결과물**: HTML 페이지 하나(claude.ai artifact). 0장 + 1–31장 + 부록 A·B(에이전트 작성) + 부록 C(문제 목록, 페이지 스크립트가 자동 생성).
- 사용자는 시간 날 때 노트로 공부하고 문제를 풀다가 Claude에게 질문하러 온다.
- 사용자의 첫 질문은 [PCCE 기출문제] 1번 / 문자 출력(340207, C++ 빈칸 채우기)이었고, 1장 첫 문제로 넣었다.

## 2. 폴더 구조 (이 폴더 = course root)
| 경로 | 내용 |
|---|---|
| `STYLE.md` | 작성 계약서: 학습자, 말투, 교육 원칙, HTML 블록, 프로그래머스 규칙, 검증 절차 |
| `OUTLINE.md` / `OUTLINE_SHORT.md` | 전체 커리큘럼(자세히 / 한 화면 요약) |
| `specs/<id>.md` | 챕터별 설계서(가르칠 주제 순서, 꼭 짚을 혼동, 임베디드 연결, 배정 문제) |
| `meta.tsv` | 검증된 문제 표 687개: 번호, **현재** 제목, 레벨(2026-11 확인), 출처 |
| `tools/chapters_def.py` → `tools/make_specs.py` | 커리큘럼 정의 → specs/, OUTLINE.md 생성(중복·존재 검사 포함) |
| `tools/verify_chapter.py` | 챕터 검증기: HTML 구조, id, 모든 코드 블록 컴파일·실행·출력 비교, 문제 링크 제목 |
| `tools/qa_all.py` | 모든 챕터 검증 + 배정 문제 누락 검사 |
| `tools/assemble.py` | chapters/*.html + shell → `dist/index.html` (전역 링크·id 검사) |
| `tools/status.py` | STATUS.md, state/progress.json 생성 |
| `tools/checkpoint.py` | git 저장: 이 폴더를 `/home/user/c-c-study/`로 복사 → commit → push |
| `tools/build_problem_bank.py`, `tools/make_short.py` | 문제 원문(problems/, problems_txt/) 재생성, OUTLINE_SHORT 생성 |
| `shell/template.html`, `shell/apxC.html` | 노트 페이지 틀(CSS·JS: 챕터 버튼, 진도 저장, 코드 색칠, 복사 버튼, 문제 체크) |
| `workflow/cpp-notes-chapters.js` | 챕터 작성 워크플로(작성자 1명/챕터, 자체 검토, 끝나면 git 저장; args.review=true면 검토자 추가) |
| `chapters/<id>.html` | 완성된 챕터(섹션 하나씩) |
| `dist/index.html` | 조립된 최종 페이지 |

git에 넣지 않는 것: `problems/`, `problems_txt/`(프로그래머스 문제 원문 — 저작권, 저장소가 공개라서), `work/`(테스트 하네스), `repos_cache/`.

## 3. 이어서 하는 법 (새 세션 또는 다른 모델)
1. 저장소 브랜치 받기: `git -C /home/user/.github fetch origin claude/adoring-brown-d1m978 && git -C /home/user/.github checkout claude/adoring-brown-d1m978`
2. 작업 폴더 만들기: `COURSE=<scratchpad>/course; mkdir -p "$COURSE" && cp -r /home/user/c-c-study/. "$COURSE"/`
3. 옛 절대 경로 바꾸기:
   `grep -rl '/tmp/claude-0/-home-user--github/c7582eac-8209-501d-9bcf-ff27aaa31704/scratchpad/course' "$COURSE" | xargs -r sed -i "s#/tmp/claude-0/-home-user--github/c7582eac-8209-501d-9bcf-ff27aaa31704/scratchpad/course#$COURSE#g"`
4. 문제 원문 다시 받기: `python3 -I "$COURSE/tools/build_problem_bank.py"` (필요하면 먼저 add_repo로 6개 공개 저장소 읽기: kkangmen/problem_solving, err-cho404/programmers-coding-test, Charles0304/BaekjoonHub, keunwon/study, Soggeum/Coding-Test, nopicklesbigmac/programmers)
5. `STATUS.md`에서 "완료"가 아닌 챕터 확인 (`python3 -I "$COURSE/tools/status.py"`로 갱신 가능)
6. 남은 챕터 작성: `Workflow({scriptPath: "$COURSE/workflow/cpp-notes-chapters.js", args: {root: "$COURSE", lanes: [["c04","c06"],["c05","c07"]]}})`
   - 워크플로 도구가 없으면 같은 파일의 `writerPrompt` 문장을 Agent 도구 프롬프트로 써서 챕터마다 에이전트 하나씩.
   - **사용량 한도 주의**: 첫 실행 때 에이전트 14명을 동시에 돌려 15분 만에 5시간 한도를 다 썼다. 동시 2명 정도, 챕터 순서대로.
7. 점검·조립: `python3 -I tools/qa_all.py` → `python3 -I tools/assemble.py` (초안 단계에서 빈 챕터를 "준비 중"으로 넣으려면 `--allow-missing`)
8. 게시: `mcp__claude-artifacts__publish_files`에 `files: [{as: "index.html", path: "$COURSE/dist/index.html"}]`, title "C/C++ 코딩 노트", icon "code". 이미 게시된 slug가 STATUS.md에 있으면 `get_artifact`로 version을 받아 `slug` + `base_version`으로 재게시. 게시 후 `python3 -I tools/status.py --artifact-url URL --artifact-slug SLUG`로 기록.
9. 저장: `python3 -I tools/checkpoint.py --msg "무엇을 했는지"` — 모델이 바뀌면 `COURSE_COAUTHOR="Claude <모델 이름> <noreply@anthropic.com>"` 환경 변수로 공동 저자 줄을 맞춘다.

## 4. 품질 기준과 결정 사항
- 계약서는 `STYLE.md`. 모든 코드 블록은 verify_chapter.py로 컴파일·실행하고 화면에 적힌 출력과 비교한다. 프로그래머스 풀이는 문제 원문의 예제로 하네스 테스트한다.
- 문제 제목·레벨은 meta.tsv가 기준(2026-11 BaekjoonHub 커밋으로 확인). 바뀐 제목 예: 42578 "의상"(옛 위장), 42587 "프로세스"(옛 프린터), 67258 "[카카오 인턴] 보석 쇼핑". N-Queen(12952)은 현재 Lv.2. 레벨은 사이트에서 바뀔 수 있다고 0장에서 한 번 안내.
- 이 작업 환경의 네트워크에서는 프로그래머스 사이트가 막혀 있다. 원문은 공개 BaekjoonHub 저장소에서 가져왔다.
- PCCE 기출(빈칸 채우기·한 줄 고치기)은 초기 코드를 볼 수 없어서 완성 코드를 보여 주고 빈칸 위치를 설명한다.
- 프로그래머스 C 템플릿: 가변 길이 배열 반환 형식이 불확실하므로 C로 다시 풀기는 문자열 반환·입력과 같은 길이 배열 반환 문제만 쓴다.
- artifact 뷰어에서는 Google Fonts·cdnjs(Prism 1.29.0)가 로드된다. 이 샌드박스 브라우저에서는 막혀서 스크린샷엔 기본 글꼴과 색칠 없는 코드로 보인다.
- 2026-11-05 첫 실행: 사용량 한도 초과로 모든 에이전트가 실패(완성 챕터 0개). 그 뒤 방식: 동시 2명, 작성자가 자체 검토까지, 챕터마다 git 저장, 앞 챕터부터 게시.

## 5. 저장 위치
- **git**: tools/checkpoint.py는 푸시 권한이 있을 때만 `/home/user/.github` 브랜치 `claude/adoring-brown-d1m978`의 `cpp-notes/`에 커밋·푸시한다. 2026-11-05 기준 battery-korail 조직에 Claude GitHub 앱이 없어 푸시가 403으로 막혀 있으므로 git에는 아무것도 남기지 않는다(푸시 못 하는 커밋이 쌓이면 종료 훅이 반복 경고함). 앞서 만든 두 커밋은 `backup/cpp-notes-commits.bundle`로 보관. 권한이 생기면 checkpoint.py를 한 번 실행하면 전부 올라간다.
- **백업 artifact(비공개)**: https://claude.ai/artifact/XcDHmRkRbP7YeYiMXhDQ2h (slug `f7dcc3e1-58cc-4c41-b6ba-c7c9fc59943e`). 이 폴더의 설계서·도구·인수인계 문서가 `src/<경로>.txt`로 들어 있다(문제 원문 제외). 새 세션에서는 `mcp__claude-artifacts__list_files` / `read_file`로 읽어 파일로 되살린 뒤 `.txt`를 떼면 된다. 챕터가 늘면 `chapters/*.html`도 같은 방식으로 추가 게시한다(publish_files, mode patch).
- **노트 artifact**: https://claude.ai/artifact/Va8eWowGk6n3oAG4tPhQUN (slug `e76023af-405b-4651-9d44-e791db641e2f`). 재게시는 `get_artifact`로 현재 version을 받아 `publish_files`에 slug + base_version + files [index.html]. 최신 version은 state/progress.json `_artifact.version`.

## 6. 다음 할 일 (2026-11-05 15:00 UTC 기준)
- 완료: start(0장), c01, c02, c03 — 작성자 자체 검토 + 검증기 통과, 노트 artifact에 게시됨.
- **사용자 요청으로 일시 정지.** 사용자가 0–3장을 공부한 뒤 "다음 제작"을 요청하면 이어서 한다.
- 다음 묶음 추천: `lanes: [["c04","c06","c08"],["c05","c07","c09"]]` (동시 2명). 끝나면 qa_all → assemble → 노트 재게시 → 백업 artifact에 chapters 추가.
- 첫 묶음(4챕터) 사용량: 하위 에이전트 약 142만 토큰, 약 63분.

## 7. 저장소 이전 (2026-11-14)
- 저장 위치를 사용자의 새 저장소 **wowowowooon/C-C-study** (공개, 브랜치 `main`)로 옮겼다. 저장소 루트 = 이 course 폴더(문제 원문·work·backup 제외).
- 새 세션에서 이어 하려면: add_repo(owner "wowowowooon", repo "C-C-study", access "push") → `git clone https://github.com/wowowowooon/c-c-study /home/user/c-c-study` → 그 폴더를 course root로 쓰고(경로 치환 불필요하게 하려면 COURSE=/home/user/c-c-study), `python3 -I tools/build_problem_bank.py`로 문제 원문 재생성.
- tools/checkpoint.py 기본값: COURSE_REPO_DIR=/home/user/c-c-study, COURSE_BRANCH=main.
- 이전 저장소(battery-korail/.github)는 GitHub 앱 권한이 없어 쓰지 않는다.

## 8. 포트폴리오 구조 (2026-11-14)
- 저장소는 사용자 포트폴리오다. 루트의 README.md, STUDY_LOG.md, solutions/, practice/, .gitignore는 저장소 쪽 파일이고 자동 저장이 덮어쓰지 않는다.
- tools/export_portfolio.py가 course → 저장소로 내보낸다: chapters → notes/chapters, dist/index.html → notes/index.html, docs/curriculum.md·docs/problems.md 생성, 나머지 도구·설계서 → notebook-src/, README의 PROGRESS 블록 갱신. checkpoint.py가 이걸 부른 뒤 커밋·푸시한다.
- 새 세션에서 course 복원: notebook-src/의 내용을 course 폴더로 복사하고, notes/chapters/*.html을 course/chapters/로 복사한 다음 build_problem_bank.py 실행.
- solutions/의 코드는 사용자가 직접 쓴다. AI가 대신 채우지 않는다.
