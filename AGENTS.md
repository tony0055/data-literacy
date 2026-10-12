# Data Literacy

데이터리터러시의이해(조성호, SF1101084) 수업의 분석·시각화·발표·과제 저장소다. 한국어로, 결과와 실제 확인한 근거부터 전한다. 사용자가 정하거나 확인할 것이 있으면 맨 앞에 둔다.

## 필요한 문맥만 읽기

- 지금 하는 일과 열린 결정은 [지도](docs/ontology.md)에 있다. 과거 기록(`docs/archive/`)은 그 일을 다시 열 때만 읽는다.
- 과제·실습은 그 프로젝트 폴더의 README부터 읽는다. 목표·입력·실행법·산출물·검증은 프로젝트 README가 갖는다.
- **스킬 본문이 그 일의 정본이다.** 이 파일과 `harness/`는 스킬을 다시 설명하지 않고, 어디로 가는지와 경계만 둔다.

| 지금 할 일 | 읽을 것 |
| --- | --- |
| 데이터 분석·시각화·주차 실습·시험 대비·팀 프로젝트 | `course-workflow` 스킬 → [단계 워크플로우](docs/course-workflow.md). 요청 범위까지만 한다 — 분석 요청에 덱·배포를 붙이지 않는다 |
| 분석 방법·수식·결론 등급 고르기 | [방법 결정표](school/school_project/course-domain/method-selector.md) |
| 수업 개념·과제 기준·강의 원문 | [수업 도메인](school/school_project/course-domain/README.md) |
| 덱·발표자료·발표 링크 제출 | 공통 `designing-decks-and-motion`(`../../.agents/skills/`) → [데이터 덱 층](docs/data-to-slides-workflow.md)(SEED·차트·모션·배포) |
| 조사·수집·문서 변환 도구 고르기 | [Capabilities](harness/capabilities.md) |
| OmO 배정 — 카테고리·위임·만드는 쪽과 검증하는 쪽 | [Routing](harness/routing.md) |
| 다음 할 일 추천 / 문맥 정리 | 전역 `harness-next` / `harness-context-clean` |
| 하네스·스킬 수정, **실수가 드러나거나 바로잡혔을 때** | 전역 `harness-design`. 실수는 그 스킬의 `references/update-loop.md`대로 고치는 턴 안에서 [실패 대장](harness/failures.jsonl)에 한 줄 남긴다 |

## 저장소 지도

| 경로 | 역할 |
| --- | --- |
| `school/school_project/` | 수업 프로젝트 정본. 주차 과제는 `weekN/<project>/`, **과제가 아닌 시험·탐색은 `workflow-test/<project>/`**. 각자 독립적이고 README를 갖는다 |
| `school/school_materials/` | 교수 제공 원자료와 강의 저장소 스냅샷. 요청 없이 수정·이름 변경·재생성하지 않는다 |
| `school/school_project/course-domain/` | 강의 저장소에서 구조화한 도메인 지식(개념·방법 결정표·평가·발표 패턴·원문) |
| `harness/` | 라우팅·도구·검사 등록(`checks.json`)·실패 대장(`failures.jsonl`) |
| `web/` | 별도 과제(2D 마인크래프트). 그 요청이 아니면 섞지 않는다 |

새 최상위 `school_project/`·`school_materials/`를 만들지 않는다. 경로는 `school/...` 기준이다.

## 공통 계약

- 수업 자료의 사실은 파일명과 가능하면 페이지를 붙여 인용한다. 2–6주는 배포 자료, 7–16주는 **계획 문서뿐**이다 — 계획에 적힌 미래 데모·데이터·채점표를 확보한 것으로 쓰지 않는다.
- 강의 원문에는 실행할 때 고쳐 써야 할 오류가 있다(n과 n−1 혼재, 한쪽만 보는 ±3σ, 대칭=정규 단순화 등). 목록은 [reading-ledger](school/school_project/course-domain/reading-ledger.md).
- 실제 데이터가 없으면 결과를 만들지 않는다. 합성 데이터는 "교육용 합성"과 생성 규칙·시드를 붙인다.
- 차트 값이 분석 코드 출력과 같다는 것은 수치 정확성의 증거가 아니다. 손계산이나 독립 집계로 대조한다.
- 완료는 요청한 산출물이 실제로 열리고 읽히는 것으로 본다 — 화면·노트북·덱이면 실행·렌더 결과까지 본다. 실행하지 못한 확인을 통과로 보고하지 않는다.
- **저장소 검사는 사용자가 청할 때 돌린다** — `python3 scripts/checks`(등록 검사 전부, 0 통과 · 1 실패 · 2 미설정). 통과·실패를 그대로 보고하고, 통과시키려고 검사나 실패 대장을 고치지 않는다.

## 진행 방식

- 입력이 필요 없는 단계는 계속 진행한다. 결과를 바꾸는 미정 결정, 파괴적 작업, 제출·배포·커밋·유료 생성 전에만 멈추고 묻는다.
- 기존 사용자 변경·무관한 파일·자격 증명·브랜치를 건드리지 않는다. 같은 실패를 반복하지 말고 가설을 바꾼다.

## 실행 환경

- 기본 실행 환경은 OmO다. Claude Code와 Codex도 이 파일을 직접 읽는다. **프로젝트에 CLAUDE.md·CLAUDE.local.md를 두지 않는다** — 두면 Claude Code가 이 파일 대신 그것을 읽는다.
- 로컬 스킬 원본은 `.agents/skills/`이고 Claude Code는 `.claude/skills/`의 상대 링크로 같은 원본을 본다. school-projects 공통 스킬은 `../../.agents/skills/`, 전역 스킬은 `~/.agents/skills/`에 있다.
- 사용자의 모델·effort 선택(세션, `~/.omo/omo.jsonc`, 로컬 `.codex/config.toml`)을 임의로 바꾸지 않는다. OmO가 명시적으로 호출되면 오케스트레이션과 루프 상태는 OmO가 갖는다.
- 커밋·푸시는 사용자가 하라고 할 때만 한다. 그 전까지는 작업트리에 남기고 무엇이 미커밋인지 알린다. `origin`(`tony0055/data-literacy`)은 **공개** 저장소다.

## Compact instructions

대화를 압축할 때 아래는 줄이거나 바꿔 말하지 않고 그대로 남긴다: 사용자의 말 원문(따옴표째)과 날짜, 사용자가 정하거나 뺀 것, 작업 중인 과제 경로·단계·제출 기한, 열린 결정, 공개한 URL, 고친 파일 경로와 미커밋 여부, 확인한 것과 확인 못 한 것의 구분.
