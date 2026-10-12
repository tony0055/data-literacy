# Project Ontology

지금 하는 일과 열린 결정만 둔다. 지난 기록은 [archive](archive/)에 있고 그 일을 다시 열 때만 읽는다.

## Goal

열린 과제 없음. 다음 사용자 요청을 기다린다.

## Core vocabulary

- **진료 인원 ≠ 유병률**: 진료 통계에는 분모(아픈 사람 전체)가 없다. youth-health 덱의 핵심 축.
- **연령 구간**: 자료마다 19~29 / 20~29 / 18~29 / 19~34. 섞지 않고 매번 적는다.
- **발표 저장소**: 발표 링크 제출용 공개 저장소 `tony0055/data-literacy-<주제>`. 절차는 [배포 절](data-to-slides-workflow.md#7-github-pages-배포-요청승인-있을-때만).

## Decisions

- 하네스는 OmO 기준으로 둔다(2026-10-12, 사용자 「omo를 기준으로 돌아가게끔 세팅해」 · 「AI-native Director System … 경량으로」). 배정은 [Routing](../harness/routing.md), 도구는 [Capabilities](../harness/capabilities.md). 이전의 "하위 에이전트는 GPT 계열로" 정책은 Routing의 만드는 쪽(Claude)·검증하는 쪽(GPT) 분리로 바뀌었다.
- 저장소 검사(`python3 scripts/checks`)는 사용자가 청할 때 돌린다.
- SEED 토큰 값은 공식 배포본 `@seed-design/stylesheet@1.1.2/global.css`에서 가져오고, 의미 색은 채움용/글자용(-text)/옅은바탕(-pale)으로 나눠 쓴다. 근거는 [데이터 덱 층](data-to-slides-workflow.md).

## State

- Done: `week6/youth-health` 덱을 「발표자료 업로드」 과제(제출 기간 2026-10-06 ~ 2026-10-23)용으로 공개했다 — https://tony0055.github.io/data-literacy-youth-health/ (저장소 `tony0055/data-literacy-youth-health`, 2026-10-12). **과제 사이트에 링크를 제출했는지는 확인하지 않았다.**
- Done: 하네스 정리, youth-health를 `workflow-test/`에서 `week6/`으로 이동(2026-10-12, 사용자 「주차 폴더 옮겨줘」).

## Open

- 20대 PHQ-9 우울 유병률 시계열, 제품별 전자담배 사용률, 수면부족 비율, 주관적 건강인지율은 확보하지 못했다. 시도한 경로는 `youth-health/research/*.md`의 '미확인' 절.
