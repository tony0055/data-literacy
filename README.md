# Data Literacy

데이터리터러시의이해(조성호, SF1101084) 수업의 실습·과제·발표를 모은 저장소입니다. 데이터 수집·정제·분석, 크롤링, 시각화, HTML 발표 덱을 다룹니다.

## 과제와 프로젝트

| 경로 | 내용 | 결과 |
| --- | --- | --- |
| [Week 3](school/school_project/week3/README.md) | 타이타닉·피마 인디언 데이터 수집·정제·EDA·예측, 노트북 보고서 | — |
| [Week 5 크롤링](school/school_project/week5/crawlingTest/README.md) | Firecrawl 수집, 출처 비교, 스마트글래스 리뷰 EDA와 HTML 발표 | [발표](https://tony0055.github.io/data-literacy/presentation/) |
| [Week 5 스킬 실습](school/school_project/week5/skillTest/README.md) | 실습 폴더 안에만 설치한 로컬 스킬 | — |
| [Week 6 20대 건강 (youth-health)](school/school_project/week6/youth-health/README.md) | 공개 통계로 본 20대 건강 변화 — 자료조사·데이터분석·16장 웹 슬라이드. 「발표자료 업로드」 과제 제출본 | [발표](https://tony0055.github.io/data-literacy-youth-health/) |
| [수업 도메인](school/school_project/course-domain/README.md) | 강의 저장소에서 구조화한 개념·방법 결정표·평가 기준·발표 패턴·원문 | — |
| `school/school_materials/` | 교수 제공 원자료(수정하지 않음) | — |
| `web/` | 별도 과제: [2D 마인크래프트](docs/2026-09-11-2d-minecraft-web.md) | — |

입력·출처·실행법·산출물·검증은 각 프로젝트 README에 있습니다.

## 작업 방식

AI 에이전트가 [AGENTS.md](AGENTS.md)를 공통 지침으로 읽습니다. 기본 실행 환경은 OmO이고 Claude Code·Codex도 같은 파일을 읽습니다.

- 분석·시각화·발표 요청: `course-workflow` 스킬이 [단계 워크플로우](docs/course-workflow.md)(질문 → 확보 → 진단 → 정제 → 분석 → 인사이트 → 시각화 → 덱)로 안내합니다. 요청한 범위에서 멈춥니다.
- 덱: school-projects 공통 `designing-decks-and-motion`(참고 디자인 시스템 SEED) 위에 [데이터 덱 층](docs/data-to-slides-workflow.md)(차트·모션·검증·GitHub Pages 배포)을 얹습니다.
- 누가 어떤 일을 맡는지는 [Routing](harness/routing.md), 쓸 도구는 [Capabilities](harness/capabilities.md), 지금 하는 일은 [ontology](docs/ontology.md)에 있습니다.

## 구성

```
AGENTS.md          에이전트 공통 지침 (항상 읽힘)
harness/           routing.md · capabilities.md · checks.json(검사 등록) · failures.jsonl(실패 대장)
docs/              워크플로우 · 현재 문맥(ontology) · archive/(지난 기록)
.agents/skills/    로컬 스킬 정본 (course-workflow). .claude/skills/는 상대 링크
scripts/           checks(검사 실행) · harness_ledger.py · course_workflow.py · course_materials.py
tests/             저장소 검사
school/            수업 프로젝트와 원자료
```

Firecrawl을 쓰려면 `.env.example`을 `.env`로 복사해 키를 넣습니다. `.env`는 커밋하지 않습니다.

## 검증

```sh
python3 scripts/checks
```

`harness/checks.json`에 등록된 검사(루트 `tests/` 단위 테스트, 실패 대장 확인)를 돌립니다. 종료 코드 0은 통과, 1은 실패, 2는 등록된 검사 없음입니다. 덱 렌더·노트북 실행처럼 각 프로젝트의 결과 확인은 그 README의 명령으로 따로 합니다.
