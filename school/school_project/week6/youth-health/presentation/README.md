# 발표 덱: 20대는 정말 아파지고 있나

1920 × 1080 단일 HTML 덱, 16장, 발표 약 5분.

## 구조

```
index.html              장 순서대로 <section class="slide">
design-standard.html    표준 확인 화면 (6장)
contact.html            전 장 컨택트시트 생성용
src/tokens.css          값 (SEED 공식 배포본에서 전사한 색 + 공통 발표 표준 타이포)
src/deck.css            공통 컴포넌트
src/charts.js           chart-data에서 SVG 차트를 그림
src/motion.js           장 안 단계 빌드 모션 (Anime.js, 일시정지 타임라인)
src/fit.js              화면 맞춤 + 넘침·작은 글자 검사(?check=1) + 단장 모드(?slide=N)
src/present.js          쪽 번호, 방향키 이동, Esc 개요, F 전체화면
assets/vendor/          Anime.js 4.5.0 UMD (MIT) + 라이선스 전문 — 로컬 번들, CDN 미사용
scripts/build.ts        ../../chart-data.json을 index.html에 주입
scripts/render.ts       Chrome으로 전 장 PNG(+--pdf)
scripts/snap-motion.ts  모션 시작·중간·최종·모션감소 스냅샷 + 상태 검사
scripts/probe-nav.ts    방향키 이동이 전 장 정확한지 실제 키 입력으로 검사
scripts/check-numbers.ts 덱 본문 수치를 원본 파일과 대조
design-standard/        표준 문서 6종 + SEED 원본 CSS 스냅샷
assets/fonts/           Pretendard Variable (OFL 1.1) + 라이선스 전문
renders/                렌더 결과
```

## 디자인

- 참고 시스템은 수업 지정 **SEED**. 색 값은 `@seed-design/stylesheet@1.1.2/global.css`(Apache-2.0)에서 전사했고 원본 스냅샷을 `design-standard/seed-global-1.1.2.css`로 보관했다. SEED `primary`(carrot)는 당근 브랜드 값이라 쓰지 않았다.
- 의미 색은 **채움용과 글자용을 분리**했다. SEED 의미 색 5개가 전부 흰 배경에서 4.5:1을 못 넘기기 때문이다. 측정값은 `design-standard/color.md`.
- 글꼴은 SEED가 권장하는 Pretendard를 프로젝트에 두고 `@font-face`로 부른다.

## 차트 규칙

- 모든 차트는 `chart-data.json`에서만 그린다. 스크린샷 차트 없음.
- y축은 항상 0에서 시작한다.
- **가로축이 연도일 때 실제 연도 간격으로 그린다.** 2013·2022·2023을 등간격으로 두면 9년과 1년이 같은 폭이 된다.
- 계열은 색 + 선 종류 + 직접 라벨로 구분한다(범례 없음).
- 값 라벨의 소수 자릿수는 출처 표기를 보존한다(45.0을 45로 줄이지 않음).

## 모션

`docs/data-to-slides-workflow.md` §5의 빌드 순서를 그대로 구현했다. 장마다 **일시정지된 Anime.js 타임라인**을 만들고, 그 장이 화면에 들어올 때 재생한다.

빌드 순서: 헤드라인 → 축·기준선·눈금 → 데이터(막대 성장 · 선 그리기 · 점 stagger) → 계열 이름 → 값 라벨 → 강조 주석 → 결론 띠. 한 번에 한 가지만 움직인다.

| 상황 | 동작 |
| --- | --- |
| 발표 중 | 장이 들어오면 자동 재생. `R` 키 또는 우하단 "다시 재생" 버튼으로 재생 |
| `prefers-reduced-motion` | 재생하지 않고 **최종 상태를 바로** 보여 준다 |
| 인쇄 · PDF | `beforeprint`에서 모든 타임라인을 끝으로 보낸다. 최종 상태 |
| 렌더(`?slide=N`, `?check=1`) | 최종 상태. 그래서 PNG·넘침 검사가 모션의 영향을 받지 않는다 |
| 스냅샷 | `?slide=N&anim=0.4` 처럼 **타임라인을 비율로 멈춰** 중간 프레임을 찍을 수 있다 |

금지 사항도 지켰다: 값·축·분모를 바꾸는 모션 없음(막대는 scaleY, 선은 draw만), 장식 루프 없음, 3D 없음, 읽기 전에 사라지는 숫자 없음(한 번 나타나면 유지).

## 실행

```sh
bun scripts/build.ts
bun scripts/render.ts index.html
bun scripts/snap-motion.ts 5,8,11   # 모션 스냅샷
bun scripts/check-numbers.ts
```

## 검증 기록 (2026-10-03)

- `bun scripts/render.ts index.html` → 16장, `issues: []` (JS 오류 수집 포함)
- `bun scripts/render.ts design-standard.html` → 6장, `issues: []`
- 컨택트시트와 5·7·8·10·12쪽을 원본 크기로 눈으로 확인
- 쪽 번호 채워짐 확인(1/16 ~ 16/16)
- `bun scripts/snap-motion.ts` → 시작(`anim=0`)에서 결론 띠 opacity 0 · 막대 scaleY 0, 최종(`anim=1`)에서 opacity 1 · scaleY 1 · 선 dashoffset 0, 모션 감소 모드에서 즉시 최종 상태. 5·8·11쪽의 0 / 0.4 / 1 프레임을 눈으로 확인
- `bun scripts/check-numbers.ts` → 미검증 수치 0
- `bun scripts/probe-nav.ts <w> <h>` → 1512×900 · 1280×800 · 1920×1080(zoom 0.75 · 0.63 · 0.97)에서 현재 장 판정 오차 0, 방향키로 1→16쪽 정확히 이동, 위로도 정확

## 알려진 범위

- 발표자 노트 토글(S)은 덱에 넣지 않았다. 대본은 `../speaker-notes.md`에 있다.
- 장 사이 전환 모션(같은 데이터를 다른 기준으로 다시 보여 주는 이동)은 넣지 않았다. 현재 덱은 장마다 데이터가 달라 해당 패턴이 필요한 지점이 없다.
- PDF는 요청이 없어 만들지 않았다. `--pdf`로 만들 수 있다.
