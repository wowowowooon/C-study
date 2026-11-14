# Spec for chapter `apxA` — 부록 A: C++ 코딩테스트 치트시트

Read STYLE.md and OUTLINE.md first. This spec lists WHAT to teach; STYLE.md says HOW.

## Identity (use exactly)
- section id: `apxA`
- data-title: `C++ 치트시트`   data-short: `치트시트`
- kicker: `부록 A · 부록`
- h2: `부록 A: C++ 코딩테스트 치트시트`  with  <span class="en-t">C++ cheat sheet for coding tests</span>
- output file: chapters/apxA.html   scratch dir: work/apxA/

## Position in the course
- Previous: [c31] 제어 코드 실전과 모던 C++. The learner has finished everything up to and including it (see OUTLINE.md).
- Next: [apxB] 부록 B: 에러 메시지와 채점 결과 사전. Point to it in the final .out box.
- Feature constraint for code in this chapter: 전부. 각 코드 조각은 data-check=compile(main 포함 작은 테스트면 run).

## Topics to teach (in this order; each normally becomes one or more numbered h3 sections)
1. 헤더 목록과 용도, 함수형/입출력형 템플릿, 빠른 입출력.
2. 자료형 범위 표, 리터럴 접미사, 형 변환 요약.
3. string 함수 표(시그니처, 반환, 주의), 문자 함수(<cctype>).
4. 컨테이너 메서드 표 + 시간 복잡도: vector, deque, stack, queue, priority_queue, set/multiset, map, unordered_map/set, pair/tuple, array.
5. <algorithm>/<numeric> 함수 표: sort/stable_sort/reverse/unique/lower_bound/upper_bound/binary_search/next_permutation/max_element/min_element/count/count_if/find/accumulate/fill/iota/gcd/lcm.
6. 비교자/람다 템플릿(오름, 내림, 다중 기준, priority_queue 최소 힙, 사용자 정의 비교자).
7. 자주 쓰는 코드 조각(각각 짧고 컴파일 검증): split, 진법 변환, gcd/lcm, 소수 판정, 에라토스테네스의 체, 고속 거듭제곱, 격자 BFS, DFS, 다익스트라, 유니온 파인드, 이분 탐색(lower_bound 직접), 매개변수 탐색, 누적합/2차원 누적합, 차분 배열, next_permutation 루프, 비트마스크 부분집합.
8. 시간 복잡도 표(입력 크기 → 허용 복잡도), 오버플로/모듈러 메모, 실수 체크리스트.

## Extra notes
찾아보기용 레퍼런스이므로 표 위주, 설명은 짧게. 각 조각 옆에 처음 배운 챕터 링크(data-go). 확인 문제/문제 카드/체크리스트는 필요 없음(넣지 말 것). .out 상자 대신 짧은 사용법 문단으로 끝내도 됨.
