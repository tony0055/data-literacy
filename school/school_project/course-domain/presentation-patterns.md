# 강의 덱 표현 패턴 (조성호 교수 데이터리터러시 2–6주)

교수 덱이 **질문 → 그림 → 조작 → 판단 → 명세 → 검증**을 화면으로 구현한 방식을 정리했다. 통계 개념은 [concepts.md](concepts.md), 방법 선택은 [method-selector.md](method-selector.md), 덱 제작 순서는 공통 `designing-decks-and-motion`과 [데이터 덱 층](../../../docs/data-to-slides-workflow.md)이 소유한다.

## 0. 학생 덱으로 옮기는 법 (요약)

| 교수 덱 | 학생 덱(SEED·공통 표준) |
| --- | --- |
| reveal.js 1280×720 다크 테마, CDN 폰트 | 공통 덱 골격 1920×1080 밝은 장 기본, 로컬 폰트, SEED Foundations를 역할 토큰으로 |
| 색 = 교육 장치(시안 개념, 마젠타 판단, 레드 AI 함정, 라임 실습) | 같은 **역할 구분**을 SEED 의미 색에 매핑(개념·근거 / 판단·강조 / 함정·주의 / 검증·실습). 원본 hex는 쓰지 않음 |
| `.ask` 도입 질문 → 뒤에서 "도입 질문의 답" 도해로 회수 | 첫 장 질문을 결론 장에서 같은 그림으로 회수 |
| `.key` 핵심 박스, `.vs` 나쁜/좋은 요청 대조, `.eq` 수식 블록, `.step` 번호 | 결론 띠·대조 2열·수식+대입 예·단계 번호 컴포넌트로 다시 그림 |
| matplotlib 도해(같은 데이터 다른 표현, 요약+원시값, 그림 안 callout, 공통 축) | `chart-data.json` → SVG 차트에 같은 기법, 모션은 빌드 순서로 읽기 순서를 만듦 |
| canvas 데모(한 변수 슬라이더, 즉시 다시 그림, 숫자 동시 표시) | 같은 계약 + 이벤트 기반 렌더·reduced-motion·PDF 스틸 |
| fragment 없음, 모션은 fade 전환과 데모 재그리기뿐 | 학생 덱은 Anime.js 단계 빌드를 더하되 데이터 왜곡 금지(데이터 덱 층 §5) |
| 개조식(명사 종결) 문체 | 슬라이드 글 기본 개조식, 대본 합니다체 |

아래 §1–9는 원본 분석 전문이다. §9 "재사용 규칙"이 실제 체크리스트다.


## 확인 범위와 읽는 법

- 원본: [강의 저장소 스냅샷](../../school_materials/pnu-lectures-2026/f25491512e69/) (커밋 `f25491512e69c264097fb1d10b650f0ceb135f7c`, 2026-10-03 원격 HEAD와 같음). 2026-10-03 하위 에이전트(GPT-6.1 Sol, 읽기 전용)가 21개 텍스트를 완독·PNG 8장을 확인해 작성했고, 주 에이전트가 장수(22/21/26/26/34)·fragment 부재·d05 상한만 검사·도해 29종을 원본과 대조했다.
- 대상은 **dataliteracy 아래의 2~6주 덱·공유 코드·도해**와 지정 계획 문서·PDF 도구다. 저장소 루트의 컴퓨터그래픽스 덱·도해는 조사하지 않았다.
- 아래 경로는 모두 원본 저장소 기준이다. `W02`~`W06`은 `dataliteracy/slides/w02/index.html`~`w06/index.html`, `T`는 `dataliteracy/slides/_shared/theme.css`, `D`는 같은 폴더의 `deck.js`다.
- `F02`~`F06`은 `dataliteracy/figures/d02_figures.py`~`d06_figures.py`, `S`는 `dataliteracy/figures/_style.py`, `P`는 `plans/데이터리터러시-5-16주-계획.md`다. `파일 § 함수/제목`은 해당 함수 전체 또는 이름이 일치하는 문서 절을 인용한다.
- **확인:** 지정 텍스트 21개 전체, PNG 8장, 주차·데모·도해 디렉터리 목록. **미검증:** HTML을 실제 브라우저에서 조작하거나 전체 덱을 렌더하지 않았고, Python 도해 재생성·PDF/zip 빌드·외부 CDN 접속·배포 사이트 확인도 하지 않았다. 코드에 따른 동작과 실제 PNG 관찰을 구분한다.
- 목적은 통계 개념 사전이 아니라 **질문→그림→조작→판단→명세→검증을 어떻게 발표 화면으로 구현하는가**다. 원본 오류는 따라 할 규칙과 분리했다.

## 1. 덱의 뼈대

### 1.1 실제 슬라이드 수와 순서

각 덱은 `.reveal > .slides > section`의 평면 수평 덱이다. 중첩 `section`은 없다. 표지·파트 표지·다음 주 예고까지 포함한 실제 수는 **22 / 21 / 26 / 26 / 34장**, 합계 **129장**이다. 계획의 25~30장은 목표치이지 실제 장수가 아니다. 도해 참조는 6 / 5 / 6 / 5 / 7개, 데모는 0 / 1 / 1 / 1 / 1개다.

| 주 | 도입 | Part I | Part II | 후반 | 끝 |
|---|---|---|---|---|---|
| 2, 22장 | 1 표지, 2 통학시간 질문, 3 구조·설계·함정 목표 | 4 표지; 5 세 데이터 형태, 6 표의 문법, 7 척도, 8 tidy | 9 표지; 10 수집 설계 순서, 11 조작적 정의, 12 출처, 13 표본 편향, 14 생존자 편향, 15 빠진 사람 점검 | 16 Part III; 17 실습 3단 루프, 18 AI 함정 #1, 19 명세 네 칸, 20 실습 5단 | 21 요약, 22 다음 주 |
| 3, 21장 | 1 표지, 2 같은 데이터·반대 결론 질문, 3 기술·판단·함정 목표 | 4 표지; 5 dirty 표, 6 문자 숫자, 7 인코딩, 8 결측 이유, 9 평균 대치 도해, 10 결측 데모, 11 중복·이상치 | 12 표지; 13 정제별 승자 역전, 14 정제 원칙, 15 로그 | 16 Part III; 17 AI 함정 #2, 18 명세, 19 실습 | 20 요약, 21 다음 주 |
| 4, 26장 | 1 표지, 2 같은 평균 연봉 질문, 3 목표 | 4 표지; 5 질문의 답, 6 평균 장단점, 7 중앙값·최빈값, 8 대표값 데모, 9 같은 평균·다른 산포, 10 전주 대치 회수, 11 분산 단계, 12 SD 해석, 13 분포 4종, 14 이봉, 15 앤스컴 | 16 표지; 17 상황별 대표값, 18 평균 함정 3종, 19 점검 3개, 20 핵심 원칙 | 21 Part III; 22 AI 함정 #3, 23 명세, 24 실습 | 25 요약, 26 다음 주 |
| 5, 26장 | 1 표지, 2 국어·수학 80점 질문, 3 목표 | 4 표지; 5 원점수 한계, 6 기준점·눈금, 7 z 공식, 8 질문의 답, 9 z 읽기, 10 표준화 데모, 11 경험 규칙 도해, 12 성립 조건, 13 기준 집단 | 14 표지; 15 이상치 3기준, 16 기준 비교표, 17 z 실패 도해, 18 제거 전 3문, 19 처리·보고 형식 | 20 Part III; 21 AI 함정 #4, 22 명세, 23 실습, 24 별도 과제 | 25 요약, 26 다음 주 |
| 6, 34장 | 1 표지, 2 같은 매출·다른 막대 질문, 3 목표 | 4 표지; 5 선택 흐름, 6 9종 차트표, 7 비교·추세, 8 분포·관계·구성, 9 오선택, 10 축 자르기, 11 조작 데모, 12 이중 축, 13 bin, 14 면적·3D, 15 색·필수 요소 | 16 표지; 17 차트 4문, 18 왜곡 판정, 19 AI 함정 #5, 20 정직한 표현 | 21 보너스 표지; 22 규칙 추정, 23 지도, 24 비지도, 25 학습·검증 분리, 26 과적합, 27 데이터 품질, 28 정확도 함정, 29 수업 내 위치; 30 Part III, 31 명세, 32 실습 | 33 요약, 34 다음 주 |

근거: W02:15–361, W03:15–347, W04:15–529, W05:15–518, W06:15–725의 모든 `section`. 슬라이드 번호는 원문에 별도 저장된 번호가 아니라 `section` 순서로 집계했다.

**편집상 특징:** 2~5주는 AI 함정이 Part III에 있지만 6주는 Part II에 있다. 2~4주는 별도 과제 슬라이드가 없고, 4주는 실습에 “제출물 없음”이라고 명시한다(W04:491–498). 5주는 별도 과제, 6주는 실습 하단에 공식 과제를 연결한다(W05:470–487, W06:688–693). 모든 주를 같은 장수·같은 꼬리 구조로 강제하지 않는다.

### 1.2 슬라이드 패턴 사전

| 슬라이드 패턴 | HTML 클래스·구조 | 목적 | 예 |
|---|---|---|---|
| 표지 | `section.cover > .week + h1 + p.muted + .meta` | 주차·주제·범위·담당 식별 | W05:15–25 |
| 도입 질문 | `.tag.trap + .ask > .hl`, `aside.notes` | 일상 사례로 기존 직관을 흔들고 정답 공개를 지연 | W03:27–39 |
| 학습 목표 | `.cols3 > .card.gfx/.vr/.trap`, `.step`, `h4`, `p` | 계산 기술·판단·AI 실패를 병렬 제시 | W04:43–61 |
| 파트 표지 | `section.divider.part-i/ii/iii > .kicker + .rule + h1 + .sub` | 시간·내용·색으로 학습 단계를 구획 | W02:60–65, 116–121, 216–222 |
| 개념 비교 카드 | `.cols` 또는 `.cols3 > .card` | 장단점·조건·처리 대안의 비교 | W04:82–105 |
| 도해 중심 | `.tag + h2 + img.fig[alt]`, 선택적 `aside.notes` | 텍스트 설명 대신 한 그림에서 관계 읽기 | W05:115–137 |
| 실시간 데모 | `h3 + .demo-wrap > .demo[data-demo] + .demo-ui`; `<!--/demo-->` | 변수 변경→그림·숫자 동시 변화 | W06:209–230 |
| 결론·원칙 | `.key`, 의미에 따라 `.vr/.trap/.lab`; 보조 `p.small` | 한 문장을 큰 강조 박스로 기억시킴 | W04:368–381 |
| 결정표·점검표 | `table > tr > th/td`, `.gfx-txt/.vr-txt/.lab-txt/.trap-txt` | 상황→선택→이유 또는 문제→검증 매핑 | W04:297–332 |
| AI 함정 | `.tag.trap` 번호 + `h2 + .vs > .bad/.good + .note` | 나쁜 단문 요청→누락/오류와 좋은 요청→확인 가능 정보를 대응 | W03:225–257 |
| 네 칸 명세 | `pre > code[data-trim]` + `.key.lab` | 목표·제약·검증 조건·비목표를 복사 가능한 요청으로 제공 | W02:275–296 |
| 실습 5단 | 표의 `# / 실습 / 확인할 개념`; 1~4 라임, 확장 5 마젠타 | 활동과 배우는 이유 연결, 마지막은 확장 | W05:430–468 |
| 과제 브리핑 | `.tag.lab + h2 + .card.vr + .key` | 제출 항목·판단 근거·조건 명시 | W05:470–487 |
| 한 장 요약 | `.tag.gfx + h2 + table` | 개념명→해석·보고 규칙을 압축 | W06:695–713 |
| 다음 주 예고 | `section.divider.part-i`, `.kicker`가 “다음 주” | 배운 도구를 다음 질문에 연결 | W04:519–529 |
| 발표자 노트 | `aside.notes` | 질문, 공개 시점, 슬라이더 조작 순서, 예상 반응을 화면 밖에 보관 | W05:170–176 |

도입 질문은 이후 **“도입 질문의 답”** 도해로 회수한다(4주 5장, 5주 8장). 3주는 정제 규칙별 승자 역전, 6주는 축 자르기에서 회수한다. “★”는 HTML 태그 안의 문자로 중요 화면을 표시하며 별도 기능은 아니다.

### 1.3 학생 분석 덱으로 옮길 핵심

수업 덱의 긴 설명을 그대로 복제하기보다 **질문→근거 그림→조건 한 가지 변경→판단→한계**를 분석 주제별 한 묶음으로 옮긴다. 계획의 14주 발표 원칙은 “1장 1메시지·제목에 결론·그림 1개”다(P §1 ‘14주’). 실제 교수 덱에는 다중 패널 도해와 밀도 높은 요약표가 있으므로, 다중 패널은 하나의 비교 메시지를 위한 경우로 제한하는 것이 맞다.

## 2. 시각 시스템: 정확한 값

### 2.1 색·서체·외부 의존성

T:14–36의 토큰:

| 역할 | 토큰 | 값 |
|---|---|---|
| 바탕 | `--bg`, `--bg-soft`, `--bg-card` | `#0b0d12`, `#12151d`, `#171b25` |
| 테두리 | `--line` | `#2a3040` |
| 본문·보조·희미한 글 | `--fg`, `--fg-dim`, `--fg-faint` | `#e8ecf4`, `#9aa4b8`, `#5f6980` |
| 개념/Part I에 쓰는 시안 | `--gfx`, `--gfx-soft` | `#35d6e6`, `#0e3a42` |
| 판단/Part II에 쓰는 마젠타 | `--vr`, `--vr-soft` | `#ff5fa2`, `#421229` |
| AI 함정·경고 레드 | `--trap`, `--trap-soft` | `#ff5a4d`, `#431612` |
| 실습·좋은 요청 라임 | `--lab`, `--lab-soft` | `#a8e05f`, `#21330f` |
| 추가 경고 옐로 | `--warn` | `#ffc44d` |

서체 스택은 `--sans: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", "Malgun Gothic", sans-serif`; `--mono: "JetBrains Mono", "D2Coding", Consolas, monospace`.

- Pretendard CSS: `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css`.
- JetBrains Mono CSS: `https://cdn.jsdelivr.net/npm/@fontsource/jetbrains-mono@5.0.20/index.min.css`.
- 모든 주 HTML은 cdnjs의 **Reveal 5.1.0** core CSS/JS, highlight Monokai CSS, notes/highlight 플러그인 JS를 로드한다(W02 §head 및 마지막 script, 다른 주 동일).
- CSS와 Python 머리말의 “컴퓨터그래픽스/지각/HMD”는 잔재다. 데이터리터러시 실제 사용에서 색은 개념·판단·함정·실습을 구분한다. SEED 토큰이 아니라 이 원본의 자체 테마다.

### 2.2 타입 스케일

1280×720 설계 좌표의 `.reveal` 기준 30px, weight 400, tracking `-0.01em`; 제목 공통 weight 700, tracking `-0.03em`, line-height 1.25, margin `0 0 .5em`, 대문자 변환·shadow 없음(T:40–69).

| 요소 | 원본 크기 | 부모 30px일 때 환산 | 그 밖의 값 |
|---|---|---|---|
| h1 / h2 / h3 / h4 | 2.1 / 1.5 / 1.15 / .95em | 63 / 45 / 34.5 / 28.5px | h4 dim, weight 600 |
| 표지 h1 | 2.5em | 75px | line-height 1.15, bottom .35em |
| 구분 표지 h1 | 2.4em | 72px | bottom .25em |
| `.ask` | 1.5em | 45px | weight 700, line-height 1.4, tracking -.035em, max-width 20em |
| `.small / .xs` | .72 / .58em | 21.6 / 17.4px | **카드 안에서는 부모가 작아져 더 작다** |
| `.tag` | .46em | 13.8px | mono, tracking .14em, weight 500 |
| `.divider .kicker / .sub` | .6 / .85em | 18 / 25.5px | kicker tracking .22em; sub max-width 22em |
| `.cover .week / .meta` | .55 / .6em | 16.5 / 18px | tracking .3em / meta line-height 1.9 |
| 표 / th | .66em / .92em | 표 19.8px, th 약 18.22px | 주차별 inline .62~.74em 등으로 덮어씀 |
| `.card / .vs 패널` | .8 / .62em | 24 / 18.6px | vs mono, line-height 1.55 |
| `.eq` | .72em | 21.6px | mono, line-height 1.8, `white-space:pre` |
| `pre / code` | pre .5em, code .85em | pre 15px, code 규칙상 12.75px | highlight 외부 CSS와 실제 computed 크기는 미검증 |
| `.note / .demo-ui` | .42 / .5em | 12.6 / 15px | mono |
| 슬라이드 번호 | 15px | 15px | right 18px, bottom 12px |

본문 p line-height 1.6, bottom .7em; li line-height 1.55, bottom .42em; 중첩 li .88em·dim(T:67–77). `.card .xs`는 24×.58=13.92px이므로 “작은 글도 발표에 충분하다”는 보장은 없다. 숫자는 원본값이며 실제 투사·모바일 가독성 검증 결과가 아니다.

### 2.3 레이아웃·컴포넌트

근거 T §레이아웃 유틸, 각 컴포넌트 주석.

- 모든 슬라이드 왼쪽 정렬, `section` height 100%.
- `.cols`: grid `1fr 1fr`, gap 1.5em, align-items start. `.cols3`: `repeat(3,1fr)`, gap 1.1em. `.wide-left`: `1.5fr 1fr`; `.wide-right`: `1fr 1.5fr`.
- 구분선 `.rule`: 90×5px, radius 3px, bottom 1.4em. 색은 해당 파트와 연동한다. Part III의 `h1 em`은 별도 라임 override가 없어 기본 시안이다.
- `.tag`: pill radius 100px, padding `.32em .8em`, bottom 1.1em. gfx/vr/trap/lab border는 각각 `#1d5a66/#6e2545/#6e2a24/#3c5220`.
- `.card`: bg-card, 1px line, radius 14px, padding `.95em 1.15em`. h4는 카드 내부 1em/700/fg. trap 카드는 배경 `#1a1113`.
- `.key`: 왼쪽 5px 색선, 해당 색 10% alpha→transparent 70%의 90deg gradient, padding `.75em 1.1em`, radius `0 12px 12px 0`, margin `.7em 0`.
- 표: width 100%, collapse, margin `.5em 0`; th 좌측 정렬·600·2px line 하단선; td `#1e2431` 1px 하단선·상단 정렬; 셀 padding `.5em .7em`, 마지막 행 하단선 없음.
- 코드: inline bg-card, 1px line, radius 5px, padding `.1em .38em`, 시안. pre width 100%, shadow 없음, margin `.5em 0`; code 배경 `#090b10`, radius 10px, padding `1em 1.2em`, max-height none, line-height 1.5, 수평 overflow auto.
- `.eq`: 같은 코드 배경·1px line·radius 10px, padding `.8em 1em`, 시안; `.cm`은 faint.
- `img.fig`: block, margin `.15em auto 0`, auto width/height, max-width 100%, **max-height 478px**, radius 12px. 직접 자식 h3가 있는 section에서는 520px. 긴 그림을 너비만으로 맞추지 않고 높이 제한으로 캡션 잘림을 방지한다(T:234–246).
- `.note`: absolute bottom `.2em`, left 0. 본문과 겹칠 가능성을 화면에서 검사해야 한다.
- `.vs`: 2열, gap 1.1em; 패널 radius 12px, padding `.85em 1em`; bad `#1a1113/#6e2a24`, good `#101a10/#3c5220`; 제목 레드/라임, sans·1.15em.
- `.step`: 원형 inline-flex, 1.7×1.7em, mono .8em/700, right .5em. 의미별 inline 색 덮어쓰기 사용.
- `.demo-wrap`: `#06070a`, 1px line, radius 14px, overflow hidden, relative. `.demo` line-height 0, canvas block width 100%.
- `.demo-ui`: flex wrap, gap `.55em 1.1em`, padding `.7em .9em`, border-top 1px line, bg-soft; label gap .5em; range width 110px·시안 accent; 값 min-width 3.4em·우측 정렬.
- 버튼: mono 1em, bg-card, fg, 1px line, radius 7px, padding `.32em .75em`, pointer; hover border/text 시안.
- `.demo-badge`: top 10px/left 12px, .42em mono/faint, tracking .1em. `.demo-alert`: top 12px/right 14px, .5em/700 mono, warn 바탕·`#0b0d12` 글, padding `.34em .8em`, radius 7px, tracking .03em, nowrap, pointer-events none.
- 진행바 3px·시안, 컨트롤 faint(T:104–113).

**인쇄 규칙은 두 가지뿐:** `@media print`에서 bg를 `#0b0d12`로 유지하고 `.demo-ui`를 숨긴다(T:349–352). 흰 종이 전용 테마나 별도 폰트 축소 규칙은 없다. PDF 배치의 나머지는 Reveal 외부 CSS와 빌드 변환에 의존한다.

## 3. Reveal·내비게이션·데모 생명주기

### 3.1 설정과 발표 조작

D:44–65: DOMContentLoaded에서 `Reveal.initialize`, 완료 후 현재 슬라이드 데모 활성화. 설정은 `hash:true`, `slideNumber:"c/t"`, controls/progress/overview 모두 true, `transition:"fade"`, speed fast, backgroundTransition none, width 1280, height 720, margin .055, minScale .2, maxScale 2, `pdfSeparateFragments:false`, plugins `[RevealNotes,RevealHighlight]`.

`dataliteracy/README.md §조작`은 방향키/스페이스, Esc 전체 목록, S 새 창 발표자 노트, 마우스 슬라이더를 안내한다. 커스텀 키 매핑은 없다. hash로 주소에 현재 위치를 남긴다. 기본 키 동작의 실제 브라우저 확인은 하지 않았다.

**Fragments:** PDF에서 fragment마다 페이지를 분리하지 않게 설정돼 있지만, W02~W06에는 `class="fragment"`나 `data-fragment-index`가 없다. 노트의 “그다음 그림 공개”는 자동 단계 공개 구현이 아니다. 앤스컴의 그림과 숫자, 과적합의 좌우 패널은 정적인 이미지 한 장에 함께 들어 있다(W04:277–287, W06:528–538).

### 3.2 데모 계약

D:12–42의 `activate(slide)`는 현재 slide의 **첫 번째** `.demo[data-demo]`만 찾는다. `window.CGDemos[host.dataset.demo]` factory를 최초 진입에 호출하고 `host.__stage`에 보관한다. 재진입에서는 기존 stage와 컨트롤 상태를 재사용한다. 실패는 console.error 후 null; 다음 진입에서 다시 초기화할 수 있다. `slidechanged` 때 현재 슬라이드를 활성화하고 데모 없는 슬라이드에서는 loop를 멈춘다.

factory는 canvas를 생성하고 `host.parentNode`에서 조작부를 찾는다. 따라서 `.demo`와 `.demo-ui`를 같은 `.demo-wrap` 안의 형제로 두는 것이 필수다. 각 factory는 input/click, ResizeObserver에서 `render()`하고 마지막에 `{draw:function(){}}`를 반환한다.

### 3.3 복제하면 안 되는 결함·제약

| 항목 | 코드로 확인한 사실 | 새 덱에서의 대응 |
|---|---|---|
| 불필요한 RAF | D:16–23은 매 프레임 `live.draw()`와 RAF 예약. d03~d06 draw는 모두 빈 함수 | 이벤트 기반 데모에는 상시 RAF를 시작하지 않는다 |
| 비활성 상태 정리 없음 | slidechanged에서 RAF만 취소. observer·input listener를 해제하는 dispose 계약 없음 | 덱을 제거/재장착하는 앱이면 teardown 계약 추가; 정적 덱에서는 최초 1회라 누적 재장착을 단정하지 않음 |
| 개요/탭 숨김 별도 처리 없음 | overviewhidden/visibilitychange 등 핸들러 없음 | 보이는 상태에서만 필요한 animation을 구동 |
| 한 슬라이드 한 데모 | querySelector 하나 | 여러 데모를 둘 경우 별도 수명주기 설계 필요 |
| 접근 가능한 대체 설명 부족 | canvas 내부 fallback/ARIA 설명 없음; 값은 UI에 HTML로 제공 | 그림의 의미·현재 수치를 텍스트로 함께 전달 |

“RAF 때문에 화면이 망가진다”거나 메모리 누수가 재현됐다는 뜻은 아니다. **빈 호출을 반복하는 설계상 낭비**를 정적 코드에서 확인했다.

## 4. 인터랙티브 데모 4종

모두 **2D Canvas**, SVG나 Three.js가 아니다. 공통으로 DPR은 `min(devicePixelRatio||1,2)`, width는 `host.clientWidth||900`, 고정 높이의 canvas를 다시 설정하고 좌표 transform을 적용한다. 난수는 mulberry32+Box–Muller를 사용해 데이터와 점 jitter를 고정한다. 슬라이더 조작에 따라 데이터 생성의 특정 조건만 바뀌므로 변화 원인을 읽기 쉽다.

### 4.1 d03: 평균 대치

근거 `dataliteracy/slides/_shared/demos/d03.js §normals/sd/imputation/render/panel`, W03:131–151.

- 조작: 결측 비율 **0~70%, step 1, 초기 35%**.
- 데이터: 정규형 600개, μ40/σ12, seed 20260910, 2~88 범위만 남김. seed77로 삭제 순서를 고정해 비율이 커지면 결측 집합도 순차 확대.
- 전/후: 왼쪽 전체 원래 분포, 오른쪽 관측치+관측 평균으로 채운 값. 34 bins, 범위 0~90, 높이 320px. 흰 평균선·시안 원본·레드 처리본; 평균·SD와 감소율을 표시.
- 수업 진행: 0→20→50→70%로 바꾸며 평균은 거의 유지되지만 가운데 봉우리와 산포가 바뀌는지 읽음.
- 주의: 원본 평균이 정확히 유지되는 것이 아니라 **남은 관측치 평균**이 대치 후 그대로 유지된다. 좌우 히스토그램은 각각 최대 빈도로 높이를 정규화하므로 빈도 높이를 직접 비교할 수 없다.
- 통계/문구 결함: SD 분모는 n. 5주 데모의 n−1과 정의가 다르다. 감소율 **12%**를 넘으면 “없는 차이가 유의로 나오기 시작하는 구간”이라고 표시하지만 검정을 계산하지도 유의수준을 정하지도 않았다. 이 임계값을 통계적 사실로 복제하지 않는다.

### 4.2 d04: 평균과 중앙값

근거 `dataliteracy/slides/_shared/demos/d04.js §sd/build/render`, W04:137–157.

- 조작: 오른쪽 치우침 **0~100**, 이상치 크기 **0~100**, 모두 초기0, step1.
- 45개 정규형 점, seed20261006, 기본 `38+9z`; 양의 편차만 `1+3.6*s*(d/DMAX)^.7`배 늘림. 이상치는 slider>0이면 **추가 1개**, 값 `168+732*outlier/100`(최대900).
- 화면: 318px, 0~150의 histogram 26bins와 점 strip; 흰 평균선·라임 중앙값선; 두 선 사이 붉은 띠; 오른쪽 96px의 별도 “화면 밖” 구역과 이상치 실제값 라벨. 라벨 높이를 달리해 겹침을 줄임.
- 전/후: 치우침만 키우거나 이상치 한 개만 키워 평균·중앙값·차이·SD를 동시 관찰. 노트는 ①기본→②치우침→③초기화 후 이상치→④띠 폭 읽기 순서.
- 결함/한계: 기본 정규 난수는 d05처럼 ±쌍으로 정확히 대칭화하지 않았다. 0에서 평균=중앙값을 **정확히** 보장하지 않는다. 양의 편차만 바꾸는 시연은 중앙값이 덜 움직이게 만든 특정 사례이며 일반 정리로 읽으면 안 된다. 이상치 추가는 n=45→46으로 바뀌지만 화면에 n을 보고하지 않는다. SD는 n 분모.
- 문구 “평균과 중앙값이 일치→이 경우에만 평균이 적합”, 차이>3을 “왜곡”으로 단정하는 경보는 분석 목적·분포에 따른 판단을 지나치게 단순화한다. 차이는 기술통계이지 자동 오류 판정이 아니다.

### 4.3 d05: 표준화와 기준선

근거 `dataliteracy/slides/_shared/demos/d05.js §sd/quant/cdf/build/render`, W05:156–177.

- 조작: 원점수 **0~140 초기80**, 평균 **30~90 초기60**, SD **3~25 초기10**, 치우침 **0~100 초기0**, step1.
- 60개, seed20261010; z와 −z의 쌍을 만들고 표본 SD로 정규화. 양의 편차만 늘려 오른쪽 꼬리를 형성한다.
- 화면: 312px, 30bins+점 strip, ±1/2/3σ 배경띠, 평균 흰선, z+3 레드선, IQR 상한 라임 점선, 원점수 옐로선. 점은 z 상한 초과 레드, 그 외 IQR 초과 옐로, 일반 시안. z·정규CDF 기반 순위·기준별 개수 표시.
- 전/후: score80 고정→평균60에서85→z 부호 변화; 평균60 복귀→SD10에서25→z 축소; 꼬리 확대→평균/SD와 기준선 이동. **치우침>0일 때 평균·SD slider는 실제 통계값이 아니라 생성 전 기본값**이며 출력은 다시 계산한 실제값이다.
- SD 분모 n−1, 사분위수는 `(n−1)*p` 선형 보간.
- 결함: **상한만** 검사(`v>m+3s`, `v>Q3+1.5IQR`)하면서 출력에는 “±3σ 바깥”, “IQR 바깥”이라고 쓴다. 양측 탐지로 재사용하려면 하한도 검사해야 한다.
- `iHit-zHit`를 z의 “미탐지”로 부르지만 IQR은 참 이상치의 정답이 아니다. `miss<=0`에서 “결과 일치”를 출력하는 것도 일반적으로 동일 개수·동일 집합을 증명하지 않는다.
- percentile은 경험적 순위가 아니라 **정규CDF 가정**. 치우침 .15 이상에서만 “대칭 분포 기준”을 덧붙인다. 정규조건을 모든 상태에 명시해야 한다. W05:139–154 표의 “대칭 분포”만으로 16%·2.3%를 보장하는 표현도 조건이 부족하다.

### 4.4 d06: 차트 조작기

근거 `dataliteracy/slides/_shared/demos/d06.js §chart-trick/peaks/render`, W06:209–230.

- 조작: y축 시작 **0~99 초기0**, bin **3~60 초기24**, 값순 정렬 버튼, 3D on/off 버튼.
- 왼쪽: 매출 `[100,101,102,104]`와 분기 라벨. baseline0→99에서 마지막/첫 막대 길이비 **1.04→5**, 실제 증가율은 항상4%. 정렬하면 내림차순으로 분기 순서를 뒤집고 “시간 순서 소멸” 표시.
- 오른쪽: 별개의 **통학시간 합성 표본 900개**, seed20261103, 평균42/78의 두 정규군집, SD7.2; 범위10~110의 histogram. bin만 변경하며 모양과 국소 봉우리 개수를 표시.
- 높이312px; 3D는 2D canvas에 dx9/dy11의 윗면·측면 polygon을 더하는 모사다. 실제 3D 렌더·카메라 회전은 없다.
- 중요한 구분: **좌우는 같은 데이터가 아니다.** 각각의 화면에서 조작 전후 데이터가 같은 것이다. 파일 머리말의 “오른쪽: 같은 데이터의 분포”를 그대로 복제하지 않는다.
- 봉우리 계수는 주변 bin 비교+최대빈도의32% threshold인 휴리스틱이다. 마지막 bin의 끝점 검사는 없고 통계적 군집 수 추정이 아니다. 라벨은 “화면상 국소 봉우리”로 제한한다.
- 계획의 “차트 유형 변경”은 구현돼 있지 않다(P §1 ‘6주’와 비교).

## 5. 도해 생성 파이프라인

### 5.1 공통 스타일과 출력

S §색 체계/폰트/rcParams/canvas/style_axes/clean/save:

- matplotlib backend **Agg**, NumPy+matplotlib, Python 함수 하나가 도해 한 개를 만든다. `_style`을 import하고 별도 설치된 폰트를 탐지한다.
- BG/BG_SOFT/CARD/LINE/FG/DIM/FAINT는 CSS와 같은 7개 값. GFX/VR/TRAP/LAB/WARN도 같은 5개 강조색. 별도의 `AX_X/Y/Z=#ff5a4d/#a8e05f/#4d9cff`는 Unity 축 잔재이며 이번 도해 표준으로 삼지 않는다.
- SANS 선택 순서 Pretendard→Pretendard Variable→Malgun Gothic→Gulim→sans-serif. MONO는 JetBrains Mono→D2Coding→Consolas→monospace. `CODE=[MONO,SANS]`로 모노의 한글 glyph를 sans에 폴백.
- 기본 font13pt, axes title15pt/700/FG, label DIM, tick FAINT, edge LINE, grid `#1e2431`/0.8, legend frame off·DIM, 선끝 round, `axes.unicode_minus=False`, `svg.fonttype="path"`.
- `canvas` 기본9×5inch. `style_axes`는 위/오른쪽 spine 숨김, 왼/아래 LINE linewidth 1.1pt, grid alpha.55/linewidth .8pt, axisbelow true. `clean`은 축·눈금·grid를 제거해 표·개념도용으로 사용한다.
- `vec`: 기본 lw2.6pt/fs13pt/head.22, annotate 화살표. `note`: fs11pt/DIM. `badge`: fs11.5pt/pad.42, BG_SOFT·해당 색 linewidth 1.3pt 외곽선. matplotlib의 글자 크기·선 두께는 CSS px와 구분한다.
- `save(fig,name,svg=True,png=True,dpi=200,pad=.28)`: `out/name.svg`와 `.png`, `bbox_inches="tight"`, pad_inches 지정, 같은 BG. 저장 후 close, 경로·KB 출력. SVG 글자는 path라 대상 PC 폰트 없이 모양 유지되지만, 생성 시 한글 폰트가 없으면 그 문제까지 고쳐주지는 않는다.
- 각 스크립트의 main은 함수 목록을 순회하고 CLI 인자 문자열이 함수명에 포함된 경우만 만드는 필터를 지원한다. RNG는 스크립트 전역이므로 **전체 실행과 일부 함수만 필터 실행은 난수 소비 순서가 달라 동일 그림을 보장하지 않는다.** 고정 seed만으로 함수별 출력 고정을 보장하지 않는 점에 유의한다.
- seed는 F02=7, F03=11, F04=404, F05=505, F06=606.

### 5.2 생성 도해 전체 목록: 29종

아래 이름에는 각각 `.svg`와 `.png`가 붙는다. 각 행의 근거는 해당 주 파일의 이름이 일치하는 `fig_*` 함수와 그 `save` 호출이다. `out/` 목록에서 29종×2=58개도 확인했다.

| 파일 이름 | 차트/구조 | 전달 메시지 | 재사용할 제작 기법·근거 |
|---|---|---|---|
| d02-table-grammar | 3행4열 표 | 행·열·관측 단위를 먼저 정함 | Rectangle 셀, 행/열 화살표, 단위 강조; F02 §fig_table_grammar |
| d02-scales | 척도 4카드 | 척도마다 가능한 연산 차이 | FancyBboxPatch, 예/특성/통계/주의의 같은 위치, 하단 진행 화살표; §fig_scales |
| d02-tidy | wide/long 표 좌우 | 기계가 읽는 표 구조 | red/lime wrong/right, 같은 셀 폭, 변환 후 구조 장점; §fig_tidy |
| d02-survivorship | 비행기 단순 실루엣 | 관측되지 않은 대상이 중요 | Rectangle+점, 관측된 구멍/비관측 부위 대비, 화살표 질문; §fig_survivorship |
| d02-sampling-bias | 좌우 겹친 histogram | 표본 편향과 표본 수는 별개 | 회색 모집단에 표본 overlay, 가중 빈도로 크기 보정, 평균 실선/점선; §fig_sampling_bias |
| d02-collection-design | 4단 카드 흐름 | 질문부터 출처로 진행 | 정방향 연결과 레드 역방향 오류 화살표, 카드마다 사례; §fig_collection_design |
| d03-dirty-data | 5행 표+우측 callout | 작은 데이터에도 여러 품질 문제 | 문제 행별 annotate·같은 높이의 라벨, 실제 문자열 예; F03 §fig_dirty_data |
| d03-missing-why | 3카드 | 결측 원인별 판단 다름 | 라임/옐로/레드로 안전성 구분, 예시와 조치 대응; §fig_missing_why |
| d03-mean-imputation | 전후 histogram | 평균 대치가 가짜 봉우리·산포 축소 | 동일 bin 경계, 평균선, 실제 통계값 제목, 새 봉우리 화살표; §fig_mean_imputation |
| d03-same-data-diff-conclusion | 좌우 2막대 | 분모 규칙만으로 승자 역전 | 같은 데이터·같은 ylim0~62, 직접 % 라벨, 승자 대형 표시; §fig_same_data_diff_conclusion |
| d03-cleaning-log | 4열 로그 표 | 유지 결정까지 추적 | 무엇/왜/어떻게/영향 행수, 네 번째 사례 회수; §fig_cleaning_log |
| d04-mean-vs-median | 전체 dot strip+확대 strip | 극단 한 명이 평균 이동 | 범위 상자, 전체/직원만 확대, 평균·중앙값 수직선, 17명 span; F04 §fig_mean_vs_median |
| d04-same-mean-diff-spread | 세 histogram 세로 | 평균 동일해도 산포 다름 | sharex, 같은 bins, ±SD 띠/양끝 화살표, 반별 메시지; §fig_same_mean_diff_spread |
| d04-variance-steps | 편차 점선+제곱 면적 | 거리→제곱→평균→제곱근 | 수치와 도형 일치, equal aspect, ①~④ 순서, 단위 복귀 강조; §fig_variance_steps |
| d04-distribution-shapes | 2×2 histogram | 대칭/꼬리/이봉 모양 확인 | 평균 점선·중앙값 실선 공통, 패널별 해석, 이봉 빈자리 callout; §fig_distribution_shapes |
| d04-anscombe | 2×2 scatter | 요약값이 같아도 관계 다름 | 같은 x/y 범위·같은 회귀선, 패널마다 사례명, 통계값 공통 footer; §fig_anscombe |
| d04-mean-trap | 강 단면/만족도막대/응답strip 3패널 | 평균만 보면 판단 실패 | 수심 그림·이봉 막대·한 명 추가 전후를 하나의 원칙으로 묶음; §fig_mean_trap |
| d05-zscore-formula | 정규곡선+칩 공식 | z는 기준점에서 눈금 수 | 편차·SD span, raw/mean/SD 색과 공식 칩 색 대응; F05 §fig_zscore_formula |
| d05-two-subjects | 정규곡선 좌우 | 같은 raw80의 위치 다름 | 평균·raw 선, 누적 영역, z badge와 순위, 두 분포 비교; §fig_two_subjects |
| d05-normal-68-95 | 정규곡선·중첩 영역 | 경험 규칙과 성립 조건 | ±1/2/3 범위·퍼센트·화살표의 대응, 조건 footer; §fig_normal_68_95 |
| d05-outlier-rules | 동일 45점 strip 3행 | 기준마다 후보 수 다름 | 같은 x·같은 jitter 유지, 기준선 이동, 후보 레드·개수 chip; §fig_outlier_rules |
| d05-skew-breaks-z | 대칭/꼬리 histogram+strip | 기준 자체가 극단값에 끌림 | z/IQR 기준선·탐지 chip, 원시 점 병행, 1개 대 6개 비교; §fig_skew_breaks_z |
| d06-chart-decision | 목적→차트 흐름도 | 질문이 차트 선택의 출발 | 분기 화살표, 5행 purpose/chart/caution 구조; F06 §fig_chart_decision |
| d06-chart-strengths | 3×3 미니차트 | 9종 차트의 쓰임/한계 | 각 차트 아래 강점 라임·약점 옐로·금지 레드 동일 위치; §fig_chart_strengths |
| d06-axis-truncation | 매출막대 좌우 | 같은4%가 길이비5배 | 동일 값 라벨, baseline0/99 대조, ratio/실제변화 구분; §fig_axis_truncation |
| d06-dual-axis | twinx 선 좌우 | 축 범위가 교차월 변경 | 동일 두 시계열, 오른쪽축 범위만 변경, 계산된 교차월 점선; §fig_dual_axis |
| d06-bin-width | histogram 3패널 | bin 선택이 봉우리 인상 변화 | 3/24/90 bins와 패널 해석, 공통 원본; §fig_bin_width |
| d06-area-illusion | 원3개+의사3D막대 | 반지름/면적·꼭대기 착시 | r1/r2/r√2를 equal aspect로, 값60/윗면65 위치 연결; §fig_area_illusion |
| d06-ml-overfitting | 학습/검증 scatter+곡선 | 학습점 적합과 새 데이터 성능은 별개 | 11차/3차 모델, 같은 곡선·sharey, 원/다이아로 데이터 분리, 오차 수직점선·실계산 MAE; §fig_ml_overfitting |

### 5.3 대표 PNG 8장 직접 관찰

모든 경로는 `dataliteracy/figures/out/` 아래다.

| 직접 연 PNG | 실제 그림에서 확인한 것 |
|---|---|
| d02-table-grammar.png | 큰 3행 표, 라임 행 화살표·마젠타 열 화살표, 밝은 정의와 회색 보조문이 분리됨 |
| d02-tidy.png | 좌우 red/lime 표 대조가 선명함. 오른쪽에는 2026년 행이 빠져 있어 완전한 reshape가 아니라 부분 예시임 |
| d03-mean-imputation.png | 평균40.4→40.3, SD11.6→9.2가 제목에 직접 나옴. 가운데 새 봉우리에 레드 callout |
| d04-variance-steps.png | ①상단 편차, ②하단 황색 제곱, ③시안 대표면적, ④라임 변 길이의 순서. 225/25/0/25/225→100→10의 위치 대응 |
| d04-anscombe.png | 동일 축의 4관계와 회귀선, 하단 공통 숫자→판단 문장. 숫자와 그림은 처음부터 한 이미지에 공존 |
| d05-skew-breaks-z.png | 왼쪽 z1/IQR1, 오른쪽 z2/IQR6; 오른쪽 큰 x범위에서 중앙 core가 압축되고 원시점과 선이 이를 보충 |
| d06-chart-strengths.png | 큰 3×3 참고표. 모든 칸의 강점/약점/금지 색·위치가 통일. 세로로 길어 슬라이드에 축소되면 글이 작아질 위험 |
| d06-ml-overfitting.png | 학습 원점/검증 다이아, red/lime 곡선과 점선오차, 새 데이터 평균오차10 대4. 좌우 패널은 동시에 보임 |

PNG 자체에서 한글은 읽혔다. 이는 HTML 슬라이드에 넣은 크기·프로젝터 환경의 가독성 검증을 대신하지 않는다.

### 5.4 따라 할 표현 기법과 원본 한계

1. **같은 데이터, 다른 표현:** 축·분모·bin 등 한 조건을 변경하고 전후를 나란히 둔다. 데이터까지 바뀌면 원인을 분리하기 어렵다.
2. **요약+원시값:** histogram 아래 strip, 전체 범위 아래 확대, 요약선 옆 점으로 요약이 숨긴 구조를 보여준다.
3. **그림 안 설명:** callout이 정확한 점/봉우리/기준선을 가리키고 직접 값 라벨·표본 수·단위를 붙인다.
4. **공통 축:** 비교가 목적이면 sharex/sharey·동일 범위를 쓰되, 범위를 달리 써야 하는 비교는 이유를 밝힌다.
5. **공간적 단계:** 분산의 ①~④, 흐름도 arrows는 시간 애니메이션 없이 읽기 순서를 만든다.
6. **강조선 종류도 구분:** 평균/중앙값, z/IQR의 실선/점선을 색과 함께 써서 색만으로 판단하지 않게 한다.

원본의 구체적 함정:

- F02 §fig_tidy: 원본 wide 표는 2024/2025/2026을 포함하지만 tidy 표는 2024/2025만 보여준다. 부분 생략 표기를 붙이지 않으면 변환 과정의 데이터 손실처럼 보인다.
- F03 §fig_mean_imputation: 평균은 원본40.4와 처리40.3으로 약간 다르며 “그대로”는 근사다. “검정하면 없는 차이도 유의”는 항상 성립하는 보장이 아니다.
- F04 §fig_anscombe: 통계값은 반올림 근사, 표본분산 예시다. 다른 장의 n 분산과 혼용하지 않는다. 표기된 “셋째 자리에서야 차이”도 각 통계량의 정밀도 검산 없이는 복제하지 않는다.
- F05 §fig_outlier_rules/fig_skew_breaks_z: 위쪽 울타리만 코드화한 오른쪽 꼬리 사례다. 범용 양측 이상치 코드가 아니다.
- F06 §fig_bin_width: 3bin은 range25~115, 나머지는10~110. footer의 “구간 개수만 변경”과 달리 **bin 경계 범위도 변경**됐다. bin 효과만 실험하려면 범위를 고정해야 한다.
- F06 §fig_chart_strengths의 막대 “시간 추세 금지”와 W06:92–121의 항목 비교 설명은 지나친 절대화다. 차트 유형 금지 목록을 모든 데이터에 적용할 법칙으로 삼지 않는다.
- 합성 데이터라는 사실과 n/출처/기준일은 계획의 필수 요소지만, 실제 도해 모두에 충분히 기입돼 있지는 않다(P §3, W06:266–290).

## 6. 모션과 읽기 순서

| 구현 | 무엇이 바뀌는가 | 데이터 읽기를 돕는 방식 | 실제 사용 상태·근거 |
|---|---|---|---|
| Reveal fade/fast | 슬라이드 전체 | 파트 이동을 짧게 연결 | 사용, D:51–53. 실제 duration은 외부 CSS·런타임 미확인 |
| input/click→Canvas render | histogram·점·평균·기준선·수치 | 조건과 결과를 즉시 연결 | d03~d06 사용. 보간 tween 없이 즉시 다시 그림 |
| 정렬/3D 토글 | 분기 순서·막대 윗면 | 시간축 상실·값 위치 착시를 관찰 | d06 §render 및 click handler |
| `.demo-alert` opacity transition `.18s` | 경고 배지 나타남 | 경고를 갑작스럽지 않게 표시할 수 있음 | T:293–302에 정의만 있음. 지정 덱·데모에서는 생성/사용 안 함 |
| fragments | 항목 단계 공개 | 읽는 순서 제어 가능 | PDF 설정만 존재; 지정 5개 덱에 사용 없음 |
| Python ①~④·화살표 | 정적 공간 순서 | 공식 전개·흐름을 차례로 따라감 | F04 variance, F02 collection. 애니메이션 아님 |

**없던 기능을 있다고 쓰지 않는다:** 지정 범위에 영상, CSS keyframes, GSAP, SVG animation, 점 드래그, 자동 재생 타임라인은 없다. 3D 버튼도 2D 착시다. 빈 RAF는 모션이 아니다. 노트의 “왼쪽 먼저/오른쪽 나중”을 구현하려면 발표자가 가리키거나 별도 fragment 가능한 HTML 요소·단계 슬라이드를 만들어야 한다.

## 7. 빌드·PDF·zip

근거 `dataliteracy/slides/build.mjs` 전체, `tools/print_pdf.py` 전체, `dataliteracy/README.md §다시 만드는 법`.

### 7.1 실행 흐름

README 예:

```sh
py dataliteracy/figures/d04_figures.py
# 아래 서버는 dataliteracy를 문서 루트로 실행
py -m http.server 8766
SLIDE_PORT=8766 node slides/build.mjs 02 03 04
```

이 명령은 원문 기록이다. Windows `py`·PowerShell과 shell-style 환경변수 문법이 혼재한다. macOS에서 그대로 동작한다고 검증하지 않았다.

`build.mjs`는 자신의 부모 `dataliteracy`를 ROOT로 정하고 port 기본8765/환경변수 SLIDE_PORT로 변경한다. 정적 서버를 **시작하지 않으므로 사전에 서버가 있어야 한다.** 인자가 없거나 Windows 고정 두 Chrome 경로가 없으면 즉시 exit1. 주차는 padStart2; HTML이 없으면 건너뛴다.

1. 원본 HTML을 읽고 `<title>`의 `—` 앞 문자열에서 파일명 금지 문자를 제거한다.
2. `figures/out/*.svg` 링크를 PNG로 변경한다. PDF 인쇄의 SVG 누락 문제를 회피하려는 주석이 있다.
3. video를 `*-poster.png` 이미지와 HTML 재생 안내로 바꾼다. 지정 덱에는 video가 없다.
4. `.demo-wrap`부터 `<!--/demo-->`까지 regex로 **안내 카드**로 치환한다. 종료 marker가 꼭 필요하다. 실제 canvas 캡처가 아니다.
5. `slides/wNN/_print.html`을 저장한다.
6. `py ../tools/print_pdf.py http://localhost:PORT/slides/wNN/_print.html?print-pdf out.pdf` 실행.
7. 치환 전 원본 HTML에서 상대 `../` asset 참조를 추출·중복 제거하고 `build_tmp/wNN-slides/slides/wNN/index.html`과 상대 경로 그대로 복사한다. 대상 확장자는 svg/png/jpg/mp4/css/js.
8. 루트 redirect `index.html`, `READ-ME.txt`를 만들고 PowerShell `Compress-Archive`로 zip을 생성한다. staging 내부 경로는 ASCII; 마지막에 build_tmp 삭제.

실제 코드 출력명은 **`dist/wNN-<title에서 추출한 제목>.pdf`, `dist/wNN-interactive-slides.zip`**이다. README 링크는 `dNN-...pdf`, `dNN-interactive-slides.zip`이므로 서로 불일치한다. 별도 이름 변경 단계는 이 스크립트에 없다.

### 7.2 PDF 출력 대기

`tools/print_pdf.py`: sync Playwright→Chrome channel launch, 실패하면 bundled Chromium launch. viewport1280×720, goto networkidle120초, `.pdf-page` attached60초, `document.fonts.ready`, 모든 image.complete60초, **추가 fixed wait1500ms** 후 `page.pdf(print_background=True,prefer_css_page_size=True)`. `.pdf-page` 개수를 출력한다.

“Chrome153 print-to-pdf가 Reveal 레이아웃 전에 인쇄해 빈1쪽”은 코드 주석의 제작 경험으로만 확인했으며 이 환경에서 재현하지 않았다. 현재 도구는 레이아웃 생성·폰트·이미지 완료를 기다리는 점이 핵심이다.

### 7.3 플랫폼·배포 주의

- Node, Python, Playwright+Chrome/Chromium, Windows `py`와 `powershell`이 필요하다. 도해에는 NumPy/matplotlib와 한글 폰트가 필요하다.
- Chrome 존재 검사에서 구한 CHROME 변수는 이후 실행에 쓰지 않는다. macOS/Linux에서 Playwright가 실행 가능해도 이 검사 때문에 빌드가 막힌다.
- zip은 참조한 로컬 파일만 담는다. CDN Reveal·폰트는 내려받지 않고 CSS의 중첩 import도 따라가지 않는다. **완전 오프라인 패키지가 아니다.**
- missing asset은 warn 후 진행하므로 zip 성공 자체가 모든 에셋 완비를 보장하지 않는다.
- `build_tmp` 전체를 반복적으로 삭제한다. 재사용 시 그 경로를 오직 staging 전용으로 예약해야 한다.
- PDF 카드 문구는 “3D 데모”, zip redirect 제목/READ-ME는 “컴퓨터그래픽스 VF3500076”, 드래그 카메라 설명을 그대로 넣는다. 데이터리터러시의 canvas 조작과 맞지 않는다.
- PDF는 demo 조작 결과를 보존하지 않는다. 학생 제출용 정적 자료는 핵심 상태의 스틸·전후 차트를 직접 제공하는 편이 낫다.
- fixed1500ms는 완료 신호가 아니다. 이미지.complete도 깨진 이미지의 성공 로드를 보장하지 않는다. 실전 검증에서는 naturalWidth와 페이지 수·빈 페이지를 별도로 확인한다.

## 8. 계획만 있는 후반 주차: 7~16주

**아래는 구현 완료 목록이 아니다.** 해당 커밋에서 slides 폴더는 w02~w06, demos는 d03~d06, figures script는 d02~d06만 존재한다. 모든 항목은 P §1의 해당 주차 계획에서 읽었다. 8·14~16주의 별도 파일명을 없는 상태에서 만들어 추정하지 않았다.

| 주 | 계획된 데모·조작→확인 | 계획된 도해/운영자료 |
|---|---|---|
| 7 | `d07.js` 상관 조작기: 점1개 드래그·n·선형/U자/두 군집→r 급변·U자 r≈0 | `d07-scatter-reading.svg`, `d07-r-values.svg`, `d07-r-squared.svg`, `d07-nonlinear-zero-r.svg`, `d07-outlier-drives-r.svg`, `d07-range-restriction.svg` |
| 8 | 독립 데모 파일·도해명 **명시 없음** | 실기+서술 공통 시험 데이터, 결과파일·정제로그·답안, 함정#1~#6 진단, 데이터/채점표 동시 제작. 형식·오프라인·부정행위 기준 확인 필요 |
| 9 | `d09.js` 교란 시뮬레이터: 강도·층화 토글·집단비율→층화 후 r 소멸·심슨 반전 | `d09-four-explanations.svg`, `d09-confounder-dag.svg`, `d09-stratification.svg`, `d09-simpson.svg`, `d09-spurious-timeseries.svg` |
| 10 | `d10.js` 배정 비교: 자원/사후/무작위·n·숨은 교란→사전특성 차이·효과 편향 | `d10-hypothesis.svg`, `d10-assignment.svg`, `d10-volunteer-bias.svg`, `d10-sample-size.svg`, `d10-ab-checklist.svg` |
| 11 | `d11.js` 유의성: 실제효과0 포함·n·중간확인 횟수→귀무조건 약5%·peeking시 증가 | `d11-sampling-variation.svg`, `d11-pvalue-definition.svg`, `d11-effect-vs-significance.svg`, `d11-confidence-interval.svg`, `d11-multiple-comparison.svg`, `d11-peeking.svg` |
| 12 | `d12.js` 재식별: 성별/생년/우편번호/직업 공개 조합·모집단 크기→유일 조합 비율 | `d12-goodhart.svg`, `d12-identifiers.svg`, `d12-k-anonymity.svg`, `d12-license-check.svg` |
| 13 | **데모 없음** 명시 | `d13-topic-criteria.svg`, `d13-plan-template.svg`; 질문/단위/출처/변수/정제/방법/검증/한계/일정의 9칸 계획서 |
| 14 | 독립 데모 계획 명시 없음 | `d14-story-structure.svg`, `d14-one-message.svg`, `d14-cherry-picking.svg`; 중간 점검표·발표 초안·데스크 크리틱 |
| 15 | 독립 데모·도해명 명시 없음 | 8분발표+4분질의안(확인 필요), 전달15점을 포함한 루브릭, 보고서·발표자료·데이터·실행기록, 필수질의3문, 동료평가 |
| 16 | 독립 데모·도해명 명시 없음 | 팀 피드백(잘된판단2/보완2/재분석1), AI 함정#1~#12 한 장 요약, 역량점검·포트폴리오 |

### 계획이 규정한 제작 방식

- P §0-2: 도입10분→Part I60→휴식10→Part II30→Part III50→정리20. 실제 구분 표지의 60/30/50은 여기와 대응한다.
- P §0-3: 개념→네 칸 명세→독립 검증. 평가 대상은 코드 작성이 아니라 요구와 오류 판별.
- P §3: 손계산6~20행/함정 재현용 합성 데이터; 생성 규칙 주석·seed·“교육용 합성” 표기, 실제집단 해석 금지.
- P §4: B1=5/6/7, B2=8 시험, B3=9/10/11(데모3종 난도 최상), B4=12+13~16 운영자료.
- 5~12주 체크리스트: 25~30장 HTML, Python→SVG/PNG, JS demo, 네 칸 명세·5단실습, 합성 스크립트/파일, PDF/zip, 배포주소, “개조식 검사 금지 0곳”(원문 표현; 구체 검사 규칙은 이 문서만으로 불명).
- 13~16주: 프로젝트 가이드·루브릭·동료평가·중간점검표·함정 요약 중심. PLATO 과제 등록은 지시가 있을 때만.

**계획/구현 차이:** 계획 첫머리 “완료2~4주”는 현재 커밋의 5~6주 실제 코드보다 오래된 상태다. 6주 계획의 `d06-color-misuse.svg`는 out 목록·F06 함수목록에 없고, 실제로는 `d06-chart-strengths`와 `d06-ml-overfitting`이 추가됐다. 계획의 차트 유형 토글도 실제 데모에는 없다. 미래 주차의 품질·통계적 정확성은 구현 전이므로 검증되지 않았다.

## 9. 재사용 규칙

### 학생 덱이 복사할 22가지

1. 첫 질문은 청중이 판단해야 할 일상 문제 한 문장으로 쓴다. 답은 다음 근거 그림에서 회수한다(§1.1).
2. 장수보다 질문→근거→판단→한계의 순서를 고정한다(P §14주).
3. 표지에 주제·범위·작성자·자료 기준을 넣는다(§1.2).
4. 소주제마다 개념/판단/실습의 역할을 색·태그로 구분한다(§2).
5. 한 장 제목은 학생 분석에서는 결론을 말하게 하고 그림은 그 결론의 근거로 둔다(P §14주).
6. 목록을 길게 쓰기보다 같은 항목 수의 비교 카드·결정표를 쓴다(§1.2).
7. 평균 등 요약값 옆에 분포나 원시 점을 함께 둔다(§5.2).
8. 전후 비교에는 원본을 고정하고 바꾼 조건을 제목에 명시한다(§4, §5.4).
9. 비교 패널의 축 범위·단위·기간을 통일하고 예외는 밝힌다(W06 §정직한 표현의 조건).
10. 강조할 값은 직접 라벨링하고 callout 화살표를 그 위치에 닿게 한다(§5.2).
11. 정상 맥락은 회색, 주목할 데이터는 강조색1개로 제한한다(W06:266–290).
12. 색 외에 실선/점선·원/다이아·패널 위치로도 구분한다(§5.3).
13. 차트에 제목·축 단위·n·출처·기준일을 넣는다(W06:266–290).
14. 공식은 수식만 놓지 말고 기준점·거리·눈금을 그림과 같은 색으로 대응한다(§5.2).
15. 긴 도해는 max-height로 제한하고 작은 글은 여러 장으로 나눈다(§2.3).
16. 네 칸 명세는 복사 가능한 텍스트로 만들고 핵심 제약 한 줄을 강조한다(§1.2).
17. 좋은 요청·나쁜 요청은 같은 데이터의 결과로 비교한다(§1.1 AI 함정).
18. 데모 조작은 한 번에 한 변수씩, 숫자와 그림을 동시에 갱신한다(§4).
19. 난수 데이터와 점 jitter는 재현 가능하게 고정하고 함수별 생성 경로도 고정한다(§5.1).
20. 발표 노트에는 질문·변수 조작 순서·공개 시점·예상 오해를 적는다(W05:170–176).
21. 정적 SVG+PNG를 함께 보관하고 PDF에는 데모의 핵심 상태를 설명 가능한 스틸로 제공한다(§5.1, §7).
22. 요약에는 계산값만이 아니라 판단 규칙·한계·다음 질문을 남긴다(§1.1).

### 복사하지 말아야 할 10가지

1. `gfx/vr/CGDemos` 이름·컴퓨터그래픽스 과목코드·HMD·Unity 축 의미를 학생 분석의 의미 체계로 쓰지 않는다(§2.1, §5.1, §7.3).
2. 2D canvas를 3D라고 설명하거나 드래그 회전을 안내하지 않는다(§4, §7.3).
3. 이벤트 렌더인데도 빈 draw의 상시 RAF를 돌리지 않는다(§3.3).
4. n과 n−1 SD를 정의 없이 섞지 않는다(§4.1~4.3).
5. 상한만 검사하고 “±3σ/양측IQR”이라고 표기하지 않는다(§4.3, §5.4).
6. 정규CDF 순위를 실제 경험적 백분위로, IQR 후보를 참 이상치의 정답으로 쓰지 않는다(§4.3).
7. SD12% 감소·평균/중앙값 차이3 등을 자동 유의/왜곡 판정선으로 쓰지 않는다(§4.1~4.2).
8. “같은 데이터/하나만 변경”이라 쓰고 좌우 데이터·histogram range·변환 후 행을 바꾸지 않는다(§4.4, §5.4).
9. 발표자 노트의 단계 공개를 이미 구현된 fragment라고 간주하지 않는다(§3.1, §6).
10. CDN 의존 zip을 완전 오프라인이라고 부르거나 Windows 전용 빌드를 다른 플랫폼에서 검증 없이 약속하지 않는다(§7).

## 읽기·검증 기록

**지정 원본 텍스트 21개를 전부 읽었다.** 초기 도구 출력에서 생략된 d03 함수 4구간은 해당 줄 범위를 다시 읽어 보완했다. 다른 긴 출력도 요약 객체 대신 전체 본문으로 읽었다.

| 구분 | 완독 수 | 파일 |
|---|---:|---|
| 안내 | 1 | dataliteracy/README.md |
| 주차 HTML | 5 | dataliteracy/slides/w02~w06/index.html 각각 |
| 공유 테마·부트스트랩 | 2 | dataliteracy/slides/_shared/theme.css, deck.js |
| 데모 | 4 | dataliteracy/slides/_shared/demos/d03.js, d04.js, d05.js, d06.js |
| 빌드 | 1 | dataliteracy/slides/build.mjs |
| 도해 스타일·생성기 | 6 | dataliteracy/figures/_style.py, d02_figures.py~d06_figures.py 각각 |
| PDF 도구 | 1 | tools/print_pdf.py |
| 계획 | 1 | plans/데이터리터러시-5-16주-계획.md |
| **합계** | **21** | 지정 파일 누락 없음 |

별도로 **PNG 8개**를 이미지 도구로 직접 열었다(§5.3). 원본 텍스트+대표 이미지의 조사 대상은 **29개 파일**이다. 커밋 확인용 Git 메타데이터와 작업 지침은 이 수에 포함하지 않았다. 실행 테스트·브라우저 조작·PDF/zip 결과물은 미검증이며, 원본 파일은 수정하지 않았다.
