# 도메인 근거

## 이 덱이 따른 원칙

| 원칙 | 출처 | 적용 |
| --- | --- | --- |
| 내용 → 브랜드 → 참고 시스템 → 표준 → 제작 → 전 장 렌더 | school-projects 공통 `designing-decks-and-motion` | 이 순서대로 진행 |
| 참고 디자인 시스템은 수업 지정 SEED | `docs/data-to-slides-workflow.md` §2–3 | SEED 공식 배포본에서 값 확인 |
| 색을 교육 장치로 쓰기 | `course-domain/presentation-patterns.md` §0 | 근거 / 악화 / 개선 / 미확정 4역할 |
| 차트 글자 하한, 필수 부품 | `docs/data-to-slides-workflow.md` §4 | `components.md` 차트 표 |
| 주장 라벨 = 결론 등급 + 확인 상태 | `docs/data-to-slides-workflow.md` §1 | `components.md` 라벨 표 |
| 스토리 뼈대 질문 → 데이터 → 근거 → 검증 → 한계 → 결론 | 같은 문서 §1 | `../../README.md`의 장 구성 |

## 확인한 출처와 날짜

| 대상 | URL | 확인일 | 결과 |
| --- | --- | --- | --- |
| SEED Foundations · Color | https://seed-design.io/docs/foundation/color | 2026-10-03 | 역할 기반 색 구조와 접근성(APCA) 기준 확인. **값 칸은 클라이언트 렌더라 마크다운 추출로는 비어 있었다** |
| SEED Foundations · Typography | https://seed-design.io/docs/foundation/typography | 2026-10-03 | 토큰 구성(크기·행간·굵기), 권장 글꼴 Pretendard, 폰트 크기 t1~t14 단계 확인 |
| SEED Foundations · Color Palette | https://seed-design.io/foundations/color/palette | 2026-10-03 | 팔레트 구성(gray·carrot·blue·green·yellow·red, 00~1000) 확인. 값 칸은 역시 비어 있었다 |
| SEED 공식 배포본 CSS | https://cdn.jsdelivr.net/npm/@seed-design/stylesheet@1.1.2/global.css | 2026-10-03 | **실제 토큰 값의 출처.** 라이트 테마 블록에서 추출 |
| SEED 토큰 변수 패키지 | https://registry.npmjs.org/@seed-design/design-token/latest (1.0.5) | 2026-10-03 | 변수 **이름만** 들어 있고 값은 없음을 확인 |
| Pretendard | https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/variable/woff2/PretendardVariable.woff2 | 2026-10-03 | 글꼴 파일과 OFL 1.1 전문 내려받음 |

공식 문서 페이지에서 토큰 **값**을 직접 읽지 못해, 같은 조직이 배포하는 **공식 npm 패키지의 CSS**에서 값을 가져왔다. 기억으로 만든 값은 하나도 없다. 원본 파일을 [seed-global-1.1.2.css](seed-global-1.1.2.css)로 보관했다.

## SEED primary를 쓰지 않은 이유

SEED `--seed-semantic-color-primary`는 `carrot-500 (#ff6f0f)`이고, carrot 팔레트는 당근(Karrot)의 브랜드 색이다. 공통 스킬은 참고 시스템에서 **구조는 빌리고 브랜드 값은 복제하지 않는다**고 정한다. 그래서:

- 빌린 것: 역할 기반 색이라는 **구조**, 스케일 단계, 접근성 우선 기준, gray · blue · red · green · yellow 스케일 **값**.
- 쓰지 않은 것: carrot 팔레트 전체와 그것을 가리키는 `primary` 역할.
- 대신 쓴 것: SEED가 시스템 강조(`--seed-semantic-color-accent`)로 정의한 **blue 계열**을 이 덱의 근거·강조 역할에 매핑.

## 이 덱에서 바꾼 것과 이유

| 바꾼 것 | 이유 |
| --- | --- |
| 의미 색을 채움/글자/옅은바탕 3단으로 분리 | SEED 의미 색은 모바일 면·아이콘용이라 5개 전부 흰 배경 글자 대비 4.5:1 미만 ([color.md](color.md) 표) |
| 행간을 비율(135/150/162%) 대신 고정 px | 발표 덱은 글자 크기가 바뀌지 않아 4px 기준선 정렬이 낫다 |
| 굵기 2단계 → 3단계 | 발표 화면 위계에 600이 필요 |
| 큰 글자 단계를 공통 발표 표준 값으로 | SEED 큰 단계는 모바일 한 화면 기준이라 1920×1080에서 위계가 뭉친다 ([typography.md](typography.md) 비교표) |

## 데이터 다루기 원칙 (이 주제에 특히 걸리는 것)

| 함정 | 이 덱의 대응 |
| --- | --- |
| 연령 구간 혼용 (19~29 / 20~29 / 청년 19~34) | 숫자마다 연령대를 명시하고 다른 구간을 한 추세선에 섞지 않는다 |
| 진료 인원 증가 = 유병률 증가 | 두 값을 다른 지표로 표기하고, 진료 인원에는 대안 설명을 같은 장에 둔다 |
| 분모 없는 환자 수 | 20~29세 인구로 나눈 조율을 `직접 계산` 라벨과 함께 제시 |
| 조사 정의·문항 변경으로 생긴 시계열 단절 | 단절 지점을 차트에 표시하고 두 구간을 한 추세로 잇지 않는다 |
| COVID-19(2020–2022) 구간의 왜곡 | 그 구간을 지나는 비교에는 그 사실을 적는다 |
| 축 자르기 | 자르지 않는다. 불가피하면 그 장에 적는다 |
