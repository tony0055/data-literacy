# Historical ontology snapshot

2026-10-02 하네스 마이그레이션 직전 원문이다. 과거 기록이며 작업 재개 지시가 아니다.

---

# Project Ontology

## Goal (What / Why)

- 2026-09-11 2D 마인크래프트 웹 MVP 구현 (`docs/2026-09-11-2d-minecraft-web.md`).
- 2026-09-18 데이터리터러시 Week 3 실습: Kaggle 타이타닉·피마 인디언 데이터 수집, 정제, 상관/인과 분석, 예측 모델 구축 (`school/school_project/week3/README.md`).
- 2026-10-02 Week 5 크롤링 실습: Firecrawl 인증 확인, WAN 3.0·Seedance 2.5 출처 비교, 스마트글래스 상품 리뷰 다중 사이트 CSV 구축 (`school/school_project/week5/crawlingTest/README.md`).

## Core vocabulary (Ontology)

- 월드·타일·핫바·저장: `docs/2026-09-11-2d-minecraft-web.md` 정의 참조.
- 결측치·이상치·중복값·0값 은폐 결측: 데이터 정제(Data Cleaning) 진단 지표.
- 크롤링·스크레이핑·원출처: 사이트 범위 수집, 단일 페이지 추출, 공식 제품 문서에 따른 사실 검증을 구분한다.

## Decision log (Decisions)

- 바닐라 JS + HTML5 Canvas 무의존 정적 파일 구조 채택.
- `school/school_project/week3` 실습을 `titanic/`과 `pima_indians/`로 독립 분리하여 데이터 파이프라인 및 산출물 개별 관리.
- 수업 프로젝트는 `school/school_project/`, 수업 원자료는 `school/school_materials/`를 정본으로 사용한다.
- 크롤링 결과는 커뮤니티 문서와 공식 문서를 구분하고, API 키는 Git에서 제외된 루트 `.env`에만 둔다.
- 스마트글래스 리뷰는 사용자 요청에 따라 해외 쇼핑몰에서 국내 사이트 한국어 글로 범위를 변경했다. 구매후기와 개인 사용기를 구분하고 이전 해외 표본은 프로젝트 archive에 보존한다.
- 슬라이드 요청에는 데이터 분석 → 풍부한 HTML 시각화·모션·생성 에셋 → 검증·수정 → 허가된 Pages 배포 흐름을 적용한다. 간단한 조사·집계는 하위 모델/낮은 effort에 위임하고 주 에이전트는 해석·통합·최종 검증을 맡는다. 절차 정본은 `docs/data-to-slides-workflow.md`, 자동 적용 진입점은 `AGENTS.md`다.
- 슬라이드 디자인 시스템은 사용자 지정 공식 `seed-design` 스킬을 사용한다. 로컬 정본·적용본과 공식 출처는 위 워크플로우 문서에서 관리한다. 이전에 배포한 덱의 소급 변경은 이번 설정 작업에 포함하지 않는다.

## Current state (State)

- Done: `school/school_project/week3/titanic/` 파이프라인(수집·진단·분석·예측) 및 기본 EDA(스크립트·노트북) 구축 완료 (`school/school_project/week3/titanic/README.md`).
- Done: `school/school_project/week3/pima_indians/` 파이프라인(수집·0값 결측 진단·왜곡 실증·예측) 구축 완료 (`school/school_project/week3/pima_indians/README.md`).
- Done: `school/school_project/week3/pima_indians/pima_indians_report.ipynb` (및 `comprehensive_report.ipynb`) 종합보고서 대화형 주피터 노트북(셀 실행 및 시각화 결과 내장) 구축 완료.
- Done: `school/school_project/week3/README.md` 종합 가이드 및 6종 시각화 산출물 정리 완료.
- Done: `school/school_project/week5/crawlingTest/`에 Firecrawl 키 검증 스크립트, WAN 3.0·Seedance 2.5 비교 보고서, 국내 4개 사이트 스마트글래스 리뷰 15건 CSV(구매후기 6·사용기 9), 스냅샷 변환 및 API 발췌 확인 스크립트 구축 완료. 상세 출처·제약은 해당 README 참조.
- Done: Antigravity 전역 스킬(`harness-context-clean`, `harness-next` 등) 등록 및 연동 완료.
- Done: 국내 스마트글래스 리뷰 15건의 EDA, 수동 주제 코딩, 차트 6개·표 3개의 단일 HTML 분석 보고서 생성 및 브라우저 확인 완료 (`school/school_project/week5/crawlingTest/smart_glasses_eda_report.html`).
- Done: 스마트글래스 EDA의 9장 HTML 발표, 10개 시각화, Anime.js 모션·GPT 생성 표지·발표 노트 구현 및 GitHub Pages 배포 완료. 로컬 9장·제어와 공개 URL을 ego-lite로 확인했다 (`school/school_project/week5/crawlingTest/presentation/README.md`).
- In progress: 없음.
- Next gate: 모델 하이퍼파라미터 튜닝 또는 주차별 보고서 제출.

## Open / needs human judgment (Open)

- 없음.
