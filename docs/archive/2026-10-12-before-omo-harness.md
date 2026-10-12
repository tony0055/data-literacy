> 과거 기록. 2026-10-12 OmO 기준 하네스 정리 직전의 `docs/ontology.md` 원문이다. 재개할 때만 읽는다.

# Project Ontology

## Goal

분석·덱 워크플로우 **시험 주행**. 주제는 "요새 20대 건강악화". 산출물은 `school/school_project/workflow-test/youth-health/`. 2026-10-03 완료. 제출용 과제가 아니라 워크플로우 점검이라 주차 계열 밖에 둔다.

완료 조건: 공개 통계로 지표 변화를 확인하고 결론 등급을 붙인 보고서·주장 대장·검증 기록, 그리고 전 장 렌더를 확인한 16장 HTML 덱.

## Core vocabulary

- 공통 지침: [AGENTS.md](../AGENTS.md).
- 로컬 스킬 정본: `.agents/skills/`; Claude 발견 경로: `.claude/skills/`.
- **진료 인원 ≠ 유병률**: 진료 통계는 분모가 없다. 이 구분이 시험 주행의 핵심 축이었다.
- **연령 구간**: 자료마다 19~29 / 20~29 / 18~29 / 19~34. 섞지 않고 매번 명시한다.

## Decisions

- 분석 단계는 [course-workflow](course-workflow.md), 덱 디자인 절차는 공통 `designing-decks-and-motion`(SEED = 참고 디자인 시스템), 수업 추가분·허가된 배포는 [data-to-slides-workflow](data-to-slides-workflow.md)가 소유한다.
- SEED 토큰 값은 공식 문서 페이지가 아니라 **공식 배포본 `@seed-design/stylesheet@1.1.2/global.css`**에서 가져온다. 문서 페이지의 값 칸은 클라이언트 렌더라 추출되지 않는다. 원본 스냅샷을 덱의 `design-standard/`에 보관한다.
- SEED `primary`(carrot)는 당근 브랜드 값이라 쓰지 않는다. 시스템 강조인 blue 계열을 근거·강조 역할에 매핑한다.
- SEED 의미 색 5종은 흰 배경 글자 대비 4.5:1을 넘지 못한다. **채움용 / 글자용(-text) / 옅은바탕(-pale)으로 나눠 쓴다.**
- 덱 차트의 가로축이 연도면 **실제 연도 간격**으로 그린다(등간격 금지).
- 기존 Codex 로컬 모델·effort 선택을 유지하며 저장소 프리셋·활성화는 사용하지 않는다.
- 하위 에이전트는 GPT 계열로 보낸다(사용자 기본 정책).

## State

- Done: workflow-test/youth-health 리서치 4건 + 보고서 + claims.csv + chart-data.json + verification.md + 16장 덱 + 대본. 저장소 검증 33개 통과.
- In progress: 없음.
- Next gate: 다음 사용자 요청. 이 덱의 GitHub Pages 배포는 **요청·승인이 있을 때만** 한다(아직 안 함).

## Open

- 20대 PHQ-9 우울 유병률 시계열, 제품별 전자담배 사용률, 수면부족 비율, 주관적 건강인지율은 확보하지 못했다. 재시도하려면 `workflow-test/youth-health/research/*.md`의 '미확인' 절에 시도한 경로가 있다.

## Archive

[마이그레이션 직전 ontology 원문](archive/2026-10-02-pre-harness-migration.md)은 과거 과제·결정·완료 기록을 보존한다. 관련 작업을 요청받을 때만 읽는다.
