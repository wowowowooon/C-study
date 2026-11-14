# C/C++ Study

> 임베디드(로봇·차량 제어) 개발자를 목표로 C/C++를 기초부터 다시 쌓는 학습 저장소입니다.
> 언어 기초 → 알고리즘(프로그래머스 Lv.3) → 임베디드 C/C++ 순서로 공부하고, 직접 푼 코드와 배운 내용을 기록합니다.

![C++17](https://img.shields.io/badge/C%2B%2B-17-00599C?logo=cplusplus&logoColor=white)
![C11](https://img.shields.io/badge/C-11-A8B9CC?logo=c&logoColor=black)
![g++](https://img.shields.io/badge/compiler-g%2B%2B-informational)
![Programmers](https://img.shields.io/badge/Programmers-Lv.0%20%E2%86%92%20Lv.3-1f4e8c)

## 왜 이 저장소를 만들었나

STM32, ESP32, 라즈베리파이, 젯슨 나노/NX로 PCB 제작부터 여러 프로젝트를 해 봤지만, 코드는 AI에 기대 왔습니다.
현장에서 살아남는 건 코드를 직접 읽고 쓰는 사람이라고 생각해서, C/C++를 처음부터 제대로 익히는 과정을 기록합니다.

**목표**
- C/C++ 문법과 메모리 구조를 설명할 수 있을 만큼 이해하기
- 프로그래머스 Lv.3 문제를 C++로 혼자 풀기 (기업 코딩테스트 대비)
- 임베디드 C 핵심(비트 연산, 포인터, volatile, 메모리 맵, ISR, 링 버퍼)과 제어 코드(PID, 필터, CAN 파싱) 직접 구현

## 진행 상황

<!-- PROGRESS:START -->
| 항목 | 진행 |
|---|---|
| 노트 챕터 | 4 / 34 완성 |
| 프로그래머스 풀이 | 0 / 315 문제 |
<!-- PROGRESS:END -->

- 노트 보기: [`notes/index.html`](notes/index.html)을 내려받아 브라우저로 열거나, GitHub Pages로 확인
- 전체 커리큘럼: [`docs/curriculum.md`](docs/curriculum.md)
- 문제 로드맵과 풀이 현황: [`docs/problems.md`](docs/problems.md)
- 학습 기록: [`STUDY_LOG.md`](STUDY_LOG.md)

## 로드맵

| 단계 | 내용 | 목표 수준 |
|---|---|---|
| Part A. 언어 기초 (1~12장) | 출력·변수·연산자·조건·반복·배열·문자열·함수·포인터·구조체·STL·시간 복잡도 | Lv.0 ~ Lv.2 입문 |
| Part B. 알고리즘 (13~28장) | 구현·정렬·해시·스택/큐·힙·완전탐색·분할 정복·DFS/BFS·이분 탐색·투 포인터·그리디·DP·최단 경로·수학 | Lv.1 ~ Lv.3 |
| Part C. 임베디드 C/C++ (29~31장) | 정수·비트 연산, 메모리 맵·volatile·ISR·링 버퍼, 상태 머신·고정소수점·PID·CAN, 모던 C++ | 실무 기초 |

## 저장소 구조

```
.
├── notes/              학습 노트 (index.html = 전체 노트, chapters/ = 챕터별)
├── solutions/          직접 푼 코드
│   └── programmers/    lv0 ~ lv3
├── practice/           개념 연습 코드 (포인터, 비트 연산, 임베디드 예제 등)
├── docs/               커리큘럼, 문제 로드맵
├── STUDY_LOG.md        날짜별 학습 기록
└── notebook-src/       노트 제작·검증 도구
```

## 공부 방식

1. 노트를 순서대로 읽고, 예제를 **직접 타이핑**해서 컴파일·실행
2. 챕터 문제를 15~30분 혼자 고민 → 힌트 → 풀이 순서로 확인
3. 푼 문제는 `solutions/`에 접근 방법·시간 복잡도·배운 점과 함께 기록
4. 3일 뒤 빈 화면에서 다시 풀기
5. 문제를 풀 때는 AI 코드 생성·자동 완성을 끄고, AI는 개념 질문과 코드 리뷰에만 사용

## 풀이 기록 규칙

- 경로: `solutions/programmers/lv<레벨>/<문제번호>_<문제이름>.cpp` (예: `lv0/181952_문자열출력하기.cpp`)
- 파일 맨 위 주석 형식은 [`solutions/TEMPLATE.cpp`](solutions/TEMPLATE.cpp) 참고
- 풀이를 올리면 [`docs/problems.md`](docs/problems.md)의 '내 풀이' 칸에 자동으로 링크됩니다

## 개발 환경

| 항목 | 내용 |
|---|---|
| 언어 | C++17, C11 |
| 컴파일러 | g++ (MSYS2 UCRT64, Windows) / g++ (Linux) |
| 에디터 | VS Code + C/C++ 확장 |
| 빌드 | `g++ -std=c++17 -Wall -Wextra main.cpp -o main` |

## 노트 제작에 대해

`notes/`의 학습 노트는 Claude와 함께 만들었습니다. 노트 안의 모든 예제 코드는 자동 검증 도구로 실제 컴파일·실행해서 적힌 출력과 일치하는지 확인했습니다([`notebook-src/`](notebook-src)).
`solutions/`와 `practice/`의 코드는 제가 직접 작성합니다.
