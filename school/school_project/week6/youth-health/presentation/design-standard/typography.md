# 타이포그래피

실제 값의 기준은 `../src/tokens.css`다.

## 글꼴

| 항목 | 값 |
| --- | --- |
| 글꼴 | Pretendard Variable |
| 파일 | `../assets/fonts/PretendardVariable.woff2` (2,057,688 bytes) |
| 출처 | npm `pretendard@1.3.9` / `dist/web/variable/woff2/PretendardVariable.woff2` |
| 사용권 | SIL Open Font License 1.1 — 전문 `../assets/fonts/Pretendard-LICENSE.txt` |
| 고른 이유 | SEED 공식 Typography 문서가 권장 글꼴로 Pretendard를 지정 |
| 불러오는 법 | `tokens.css`의 `@font-face`. 경로는 **CSS 파일 기준 상대 경로**라서 `index.html`과 `design-standard.html`이 같은 `src/tokens.css`를 써도 맞는다 |

프로젝트 안에 글꼴 파일을 두고 `@font-face`로 부른다. CDN이나 시스템 글꼴에 기대지 않는다. 대체 글꼴로 렌더되면 줄 길이가 달라져 한 줄 헤드라인이 넘친다.

## 프리셋

굵기 3단계(400 · 600 · 800), 행간은 4px 기준선.

| 역할 | 토큰 | 굵기 크기/행간 | 쓰는 곳 |
| --- | --- | --- | --- |
| Display | `--t-display` | 800 64/80 | 표지 제목, 파트 표지, 질문 장 |
| Headline | `--t-headline` | 800 44/56 | 내용 장 결론형 헤드라인 (**한 줄**) |
| Title | `--t-title` | 800 28/40 | 카드 안 큰 값, 수식 |
| Subtitle | `--t-subtitle` | 600 22/32 | 카드 제목, 차트 제목 |
| Body | `--t-body` | 400 20/32 | 본문 |
| Body strong | `--t-body-strong` | 600 20/32 | 결론 띠 |
| Small | `--t-small` | 400 18/28 | 카드 본문, 목록 |
| Kicker | `--t-kicker` | 600 16/24 | 머리글 꼬리표, eyebrow |
| Caption | `--t-caption` | 400 14/24 | 출처, 쪽 번호 |
| Label | `--t-label` | 600 14/16 | 주장 라벨 |
| Tick | `--t-tick` | 400 18/24 | 차트 축 눈금, 직접 라벨 |
| Number L / XL | `--t-num-l` / `--t-num-xl` | 800 56/64 · 96/96 | 핵심 수치 |

- **본문 하한 18px.** 14~15px은 출처 · 쪽 번호 · 주장 라벨 · 차트 캡션에만 쓴다.
- `src/fit.js`의 검사가 이 규칙을 강제한다. 14px 미만은 무조건, 14~17px은 위 3차 역할 밖이면 보고한다.

## SEED 단계와의 차이

SEED는 모바일 UI 기준이라 그대로 쓰면 발표 화면에서 너무 작다. 두 체계는 **용도가 다르므로 값을 맞추지 않고, 매핑과 차이를 기록**한다.

| SEED 토큰 | SEED 값 (1rem=16px) | 이 덱에서 가장 가까운 역할 | 이 덱 값 | 배율 |
| --- | ---: | --- | ---: | ---: |
| `$font-size.t1300` | 4.5rem = 72px | Display | 64px | 0.89 |
| `$font-size.t1000` (semantic `h1`) | 3rem = 48px | Headline | 44px | 0.92 |
| `$font-size.t900` (`h2`) | 2.625rem = 42px | — | — | — |
| `$font-size.t800` (`h3`) | 2.125rem = 34px | Title | 28px | 0.82 |
| `$font-size.t600` (`h4`) | 1.625rem = 26px | Subtitle | 22px | 0.85 |
| `$font-size.t400` (`title2`) | 1.25rem = 20px | Body | 20px | 1.00 |
| `$font-size.t300` (`title3`) | 1.125rem = 18px | Small / Tick | 18px | 1.00 |
| `$font-size.t200` (`subtitle1`) | 1rem = 16px | Kicker | 16px | 1.00 |
| `$font-size.t100` (`subtitle2`) | 0.875rem = 14px | Caption / Label | 14px | 1.00 |

- **차이와 이유:** SEED의 큰 단계(t800 이상)는 모바일 한 화면에 제목 하나를 세우는 값이라 1920 × 1080에서 제목·부제 간 위계가 뭉친다. 그래서 큰 단계는 공통 발표 표준 값을 쓰고, 본문 이하(t400~t100)는 SEED와 같은 값으로 뒀다.
- 행간: SEED는 `135% / 150% / 162%` 비율 토큰을 쓰고, 이 덱은 4px 기준선에 맞춘 **고정 px**을 쓴다. 발표 덱은 글자 크기가 바뀌지 않아 비율보다 기준선 정렬이 낫다.
- 굵기: SEED 정적 토큰은 `regular` / `bold` 두 단계다. 이 덱은 발표 위계를 위해 600을 더해 3단계로 쓴다.
- 자간: SEED `--seed-scale-letter-spacing-narrow-200 = -0.02em`을 참고해 본문 -0.01em, 헤드라인 -0.025em, Display -0.035em으로 크기가 커질수록 더 좁혔다.

## 한글 조판

- `word-break: keep-all` — 단어 중간에서 끊지 않는다.
- `font-variant-numeric: tabular-nums` — 표·차트에서 숫자 자리를 맞춘다.
- 헤드라인은 **한 줄**. 넘치면 문장을 줄이지 말고 장을 나눈다.
- 본문은 `text-wrap: balance`, 여러 줄 문장은 의미 단위로 직접 끊는다.
- `<br>` 대신 요소를 나눈다.
