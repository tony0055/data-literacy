# 데이터리터러시의이해 도메인 지식

요청 이해: 공개 저장소의 이 과목 자료를 빠짐없이 보존·정독하고, 실습·시험·팀 분석·발표에서 같은 판단·명세·검증 흐름을 재사용한다.

## 정본과 범위

- 출처: [shain1912/pnu-lectures-2026](https://github.com/shain1912/pnu-lectures-2026), 조성호, SF1101084.
- 수집 기준: 2026-10-02, 커밋 `f25491512e69c264097fb1d10b650f0ceb135f7c`.
- [원본 스냅샷](../../school_materials/pnu-lectures-2026/f25491512e69/): 99파일. `dataliteracy/` 전체 87파일, 상세 계획 1파일, 과목별 배포 안내 10파일, 공통 PDF 출력 의존 코드 1파일. SHA-256·Git blob·원격 경로는 `manifest.json`.
- [5–16주 상세 계획 원문](../../school_materials/pnu-lectures-2026/f25491512e69/plans/데이터리터러시-5-16주-계획.md)을 우선 대조한다.
- 컴퓨터그래픽스, 별도 `datascience/`, 관련 없는 과제 안내는 수입하지 않았다. 혼합된 루트 README·목록·배포 README는 범위 판별에만 읽었다.
- 기존 `school/school_materials/`의 PDF 3개는 수정하지 않았다.

스냅샷 밖에서 2026-10-03 추가로 읽은 것(같은 커밋, 저장소에 복사하지 않음):

- [`datascience/TEACHING_DIRECTION.md`](https://github.com/shain1912/pnu-lectures-2026/blob/f25491512e69c264097fb1d10b650f0ceb135f7c/datascience/TEACHING_DIRECTION.md): 교수가 2026-09-10 PLATO 교수계획표를 읽고 남긴 교육 방향. 선수지식 없음, 주교재는 제공 PDF, 실습은 OpenCode·Antigravity CLI 등 AI 코딩 에이전트 바이브코딩, 평가 비중(출석 10·실습 30·중간 20·기말 팀 40), 목표는 "수치·그래프가 무엇을 뜻하고 어디까지 주장할 수 있는지 판단". 실습 순서는 개념 → 적용 → 결과 비교·해석.
- 같은 폴더의 `COURSE_DESIGN.md`·`PLAN.md`는 문서 스스로 "기존 가안 보류"라고 밝힌 다른 과목 가안이다. 주차·평가로 쓰지 않는다. 단, 매주 기록 6항목(질문·데이터·방법·증거·검증·한계)은 보고서 뼈대로 쓸 만하다.
- 루트 README의 제작 도구(슬라이드 reveal.js, 도해 matplotlib, 애니메이션 manim)와 문체 기준(개조식·명사 종결). `assignments/`는 컴퓨터그래픽스 과제라 제외.

2–6주 HTML·PDF·ZIP·도해는 실제 배포 자료다. 7–16주는 **계획 문서만 존재**한다. 계획에 이름이 적힌 미래 데모·데이터·채점표를 이미 확보한 것으로 취급하지 않는다. 1주 자료와 학교 제출 교수계획표, 실제 시험 데이터는 원격 저장소에 없다.

## 사용할 지식

| 문서 | 읽는 때 |
| --- | --- |
| [질문→방법→수식 결정표](method-selector.md) | 분석 방법·함께 보고할 값·차트·결론 등급·AI 함정 12개 |
| [개념·공식·AI 함정](concepts.md) | 개념 설명과 원문 근거 |
| [강의 덱 표현 패턴](presentation-patterns.md) | 덱 구조·도해·데모·모션을 강의 방식으로 만들 때 |
| [실습·중간고사·팀 평가 대비](assessments.md) | 주차 과제, 시험 연습, 팀 프로젝트 |
| [실행 워크플로우](../../../docs/course-workflow.md) | “분석해줘”, “시각화자료 만들어줘”, “발표슬라이드 만들어줘” |
| [데이터 덱 층](../../../docs/data-to-slides-workflow.md) | 공통 덱 스킬 위에 더하는 차트·모션·데모·검증·허가된 배포 |
| [읽기·변환·차이 기록](reading-ledger.md) | 원문 확인, 자료 신뢰도와 누락 검토 |
| `pdf-text/` | PDF 전체 텍스트 검색; 도해는 원본 그림과 함께 확인 |
| `zip-text/` | ZIP 내부 고유 안내문·소스 차이·도해 변형 |
| `templates/` | 새 프로젝트로 가져가 실제 입력에 맞게 작성 |

도메인 노트는 원문의 탐색·실행 보조이지 학교 공지의 대체물이 아니다. 학교에서 새 공지가 오면 해당 과제의 최신 공지를 계획안보다 우선한다. 성적·시험 규칙의 확정 여부는 [평가 대비](assessments.md)에 구분했다.

## 실행과 갱신

```sh
# 로컬 보존 자료의 변조·누락·범위 검사
python3 scripts/course_materials.py check

# 새 읽기용 체크아웃으로 당시 원격 트리와도 대조
git clone https://github.com/shain1912/pnu-lectures-2026.git /tmp/pnu-course-source
python3 scripts/course_materials.py check /tmp/pnu-course-source

# 요청별로 읽을 문서·단계·산출물 계약 확인 (모델명은 실행 예시)
python3 scripts/course_workflow.py analysis gpt-6.1-sol-fast
python3 scripts/course_workflow.py visualization gpt-6.1-sol-fast
python3 scripts/course_workflow.py slides gpt-6-astra
python3 scripts/course_workflow.py midterm gpt-6-astra
python3 scripts/course_workflow.py team gpt-6-astra

# 저장소 검사
python3 scripts/checks
```

명령은 저장소 루트에서 실행한다. `course_workflow.py`는 실행 지시용 JSON을 출력하는 계약 검사기다. 모델 호출·데이터 분석·덱 생성을 대신 완료했다고 표시하지 않는다. 에이전트는 그 계약과 스킬을 읽고 실제 입력을 처리해야 한다.

원본 수입은 `python3 scripts/course_materials.py import <체크아웃>`으로 재현한다. 이 명령은 위 커밋에 고정돼 있으며 충돌하는 로컬 파일을 덮어쓰지 않는다. `archives` 하위 명령은 ZIP 비교 색인과 서로 다른 내부 파일을 생성한다. 최신 자료 갱신은 새 커밋의 범위를 다시 조사하고 새 스냅샷을 만들어 이전 기록과 구분한다. 기존 스냅샷을 최신 자료로 바꾸지 않는다.

PDF 변환은 `kordoc` 스킬에 따라 `npx -y kordoc@^4 <원본PDF들> -d <프로젝트의 변환폴더> --no-images`로 수행했다. 텍스트층을 읽되 그림 자체의 내용은 원본 SVG/PNG·HTML·도해 코드로 보완했다. 변환문을 원본 PDF 자리에 두지 않는다.

## 산출물의 소유권

이 폴더는 학기 전체 지식·양식·자료 감사만 소유한다. 실제 분석·과제·발표는 `school/school_project/weekN/<project>/`에 두고 각 README에 입력, 실행법, 결과, 검증과 제출 범위를 남긴다. 샘플의 수치·결론을 새 데이터 결과로 복사하지 않는다.
