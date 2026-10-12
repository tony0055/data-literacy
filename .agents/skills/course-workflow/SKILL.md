---
name: course-workflow
description: 데이터리터러시의이해 수업 맥락에서 "이 데이터 분석해줘", "시각화자료 만들어줘", "발표슬라이드/덱 만들어줘", "데이터 분석하고 발표까지", 주차 실습·과제, 중간고사 대비, 기말 팀 프로젝트 요청에 사용한다. 질문 설계 → 데이터 확보·진단·정제 → 방법 선택(수식) → 독립 검증 → 인사이트 → 시각화 → SEED 기반 애니메이션 HTML 덱까지 단계별 도구와 산출물을 정한다.
---

# 데이터리터러시 실행

경로는 저장소 루트 기준이다.

## 읽는 순서 (필요한 것만)

| 지금 하는 일 | 읽을 것 |
| --- | --- |
| 범위·단계·산출물 정하기 | `docs/course-workflow.md` |
| 분석 방법·수식·결론 등급 고르기 | `school/school_project/course-domain/method-selector.md` |
| 개념 설명·원문 근거 | `school/school_project/course-domain/concepts.md` |
| 주차 과제·시험·팀 기준 | `school/school_project/course-domain/assessments.md` + 학교 공지 |
| 덱·발표 | 공통 `designing-decks-and-motion` → `docs/data-to-slides-workflow.md` → `course-domain/presentation-patterns.md` |
| 원문 확인·자료 오류 | `course-domain/reading-ledger.md`, `pdf-text/`, 원본 스냅샷 |

## 흐름

1. 요청을 모드(analysis·visualization·slides·practice·midterm·team)로 정하고 그 모드의 끝에서 멈춘다. 필요하면 `python3 scripts/course_workflow.py <mode> <모델>`로 읽을 파일·단계·산출물 계약을 본다.
2. 프로젝트 폴더에 4칸 명세(`course-domain/templates/`)를 실제 입력으로 채운다.
3. 실제 데이터를 확보·진단하고, 허용한 처리만 정제하고, method-selector에서 고른 방법의 "함께 보고" 항목까지 계산한다.
4. 핵심 수치를 손계산 또는 독립 집계로 대조하고, 민감도와 결론 문장 등급으로 인사이트를 쓴다.
5. 차트는 검증된 집계로만 그리고 렌더를 직접 본다. 발표면 덱 갈래로 넘어간다.
6. 요청한 산출물을 실제로 열어 확인하고 파일/URL·검증·한계를 보고한다. 저장소 검사(`python3 scripts/checks`)는 사용자가 청할 때 돌린다.

## 함정

- 7–16주 내용은 계획안이다. 확정/계획/확인 필요를 산출물에 남긴다.
- 강의 원문 오류(ddof 혼재, 한쪽만 보는 이상치 탐지, 대칭=정규)를 그대로 옮기지 않는다.
- 4–6주 실습의 특수 조건(기본색·20구간, 비교표·3줄 판단, 같은 값 차트 쌍)은 그 과제에만 적용한다.
- 원자료(`school/school_materials/`)를 수정하지 않는다.
