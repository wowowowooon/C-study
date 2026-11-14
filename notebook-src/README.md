# notebook-src — 노트 제작·검증 도구

`notes/`의 학습 노트를 만들고 검증하는 데 쓴 파일들입니다. 노트는 Claude와 함께 작성했고, 아래 도구로 품질을 확인했습니다.

| 파일 | 역할 |
|---|---|
| `STYLE.md` | 노트 작성 규칙(학습자 수준, 설명 방식, HTML 구성) |
| `OUTLINE.md`, `specs/` | 전체 커리큘럼과 챕터별 설계서 |
| `meta.tsv` | 프로그래머스 문제 687개의 번호·현재 제목·레벨 |
| `tools/verify_chapter.py` | 챕터 안의 모든 C/C++ 예제를 실제로 컴파일·실행하고, 노트에 적힌 출력과 비교 |
| `tools/assemble.py` | 챕터를 하나의 노트 페이지로 조립 |
| `tools/export_portfolio.py`, `tools/checkpoint.py` | 이 저장소 구조로 내보내고 커밋·푸시 |
| `HANDOFF.md`, `STATUS.md` | 제작 인수인계 문서와 진행 상황 |

프로그래머스 문제 원문은 저작권 때문에 넣지 않았습니다(`tools/build_problem_bank.py`로 다시 받을 수 있음).
