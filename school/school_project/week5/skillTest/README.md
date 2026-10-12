# Week 5 — 로컬 스킬 테스트

이 폴더의 `.agents/skills/`에만 k-skill을 설치했다. 글로벌 및 저장소 루트 스킬 경로에는 설치하지 않았다. 이 폴더를 작업 디렉터리로 지정한 Codex 작업에서 사용한다. 현재 대화의 스킬 목록 반영 여부는 별도로 확인해야 하며, 목록에 없으면 이 폴더에서 새 작업을 연다.

## 설치 목록

원본 README의 **쇼핑·중고거래** 분류 전체 12개:

- `coupang-product-search`: 쿠팡 상품 검색
- `naver-shopping-search`: 네이버 쇼핑 가격비교
- `danawa-price-search`: 다나와 최저가 비교
- `market-kurly-search`: 마켓컬리 상품 조회
- `daiso-product-search`: 다이소 상품 조회
- `olive-young-search`: 올리브영 검색
- `ohou-today-deal`: 오늘의집 오늘의딜 조회
- `bunjang-search`: 번개장터 검색
- `daangn-used-goods-search`: 당근 중고거래 검색
- `daangn-cars-search`: 당근중고차 검색
- `consumer-price-safety-search`: 소비자 가격·리콜정보 조회
- `delivery-tracking`: 택배 배송조회

한국어·글쓰기 분류에서는 `korean-slang-writing`(한국어 유행어 글쓰기)만 설치했다.

## 원본과 범위

- 저장소: [NomaDamas/k-skill](https://github.com/NomaDamas/k-skill)
- 고정 커밋: `9fade13b1066bc58fd820fe659145a9a21974138`
- 설치일: 2026-10-02
- 라이선스: MIT, [LICENSE.k-skill](LICENSE.k-skill)
- 각 스킬 폴더의 `SKILL.md`, `instruction.md`, `skill.json`, 제공되는 보조 파일을 그대로 보존했다.
- `SKILL.md`는 원본 CLI 안내용 진입점이다. 고정 버전의 실제 지침은 각 폴더의 `instruction.md`에서 읽을 수 있다. 원본의 `npx ... instruct` 명령은 최신 배포판을 조회하므로 이 스냅샷과 다를 수 있다.
- 설치·업데이트는 이 폴더의 경로를 명시해서 수행한다. 전역 일괄 업데이트 명령은 이 로컬 테스트의 설치 절차에 포함하지 않는다.

파일 저장과 원본 일치만 검증했다. 실제 상품 조회·글쓰기 실행, 외부 서비스 연결 및 인증 설정은 이번 설치에 포함하지 않았다.
