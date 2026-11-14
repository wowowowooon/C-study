# Spec for chapter `apxB` — 부록 B: 에러 메시지와 채점 결과 사전

Read STYLE.md and OUTLINE.md first. This spec lists WHAT to teach; STYLE.md says HOW.

## Identity (use exactly)
- section id: `apxB`
- data-title: `에러·채점 결과 사전`   data-short: `에러사전`
- kicker: `부록 B · 부록`
- h2: `부록 B: 에러 메시지와 채점 결과 사전`  with  <span class="en-t">Compiler errors, runtime errors and verdicts</span>
- output file: chapters/apxB.html   scratch dir: work/apxB/

## Position in the course
- Previous: [apxA] 부록 A: C++ 코딩테스트 치트시트. The learner has finished everything up to and including it (see OUTLINE.md).
- Feature constraint for code in this chapter: 전부. 에러 예시는 data-check=error로 실제 메시지를 확인하고 핵심 줄만 인용.

## Topics to teach (in this order; each normally becomes one or more numbered h3 sections)
1. 컴파일 에러 메시지 25개 내외: g++ 실제 메시지(실제로 컴파일해서 얻은 문구, data-check=error) + 뜻 + 흔한 원인 + 고치는 법. 예: expected ';' before, was not declared in this scope, no matching function for call to, invalid conversion from, cannot convert, expected primary-expression, redefinition of, no member named / has no member, request for member … which is of non-class type, invalid operands to binary expression, lvalue required, discards qualifiers(const), use of deleted function, too many/few arguments, control reaches end of non-void function(경고) 등.
2. 링크 에러: undefined reference to, multiple definition of.
3. 런타임 에러: Segmentation fault(범위 밖, 널, 스택 오버플로), Floating point exception(정수 0 나누기), std::out_of_range(at, substr, stoi), std::invalid_argument(stoi), bad_alloc(메모리), abort/assert, 무한 루프.
4. 프로그래머스 채점 결과 해석: 통과/실패(틀린 답), 시간 초과, 런타임 에러(신호 번호 포함 메시지 형태는 일반론으로), 메모리 초과, 컴파일 에러 — 각 원인과 점검 순서.
5. '예제는 맞는데 제출하면 틀림' 원인 체크리스트(엣지 케이스, 오버플로, 초기화, 전역 변수, 출력 형식, 시간 복잡도).
6. 꼭 고쳐야 하는 -Wall/-Wextra 경고(형식 불일치, 초기화 안 함, 부호 비교, 반환 누락, 사용되지 않는 변수는 단서).

## Extra notes
찾아보기용. 표와 짧은 예시 위주. 확인 문제/문제 카드는 넣지 않음. 마지막은 짧은 문단.
