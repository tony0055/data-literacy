# Week 5 — Firecrawl 크롤링 테스트: WAN 3.0과 Seedance 2.5

수집일: 2026-10-02 (Asia/Seoul)

## 결론

- 루트 `.env`의 `FIRECRAWL_API_KEY`는 실제 Firecrawl v2 요청에서 인증에 성공했다. 키 값은 출력하거나 이 폴더에 복사하지 않았다.
- 나무위키 「영상 인공지능」 문서는 정상 수집됐지만, 정확한 버전명 `Wan 3.0`은 본문에 없었다. 이 문서가 명시한 알리바바 계열은 Wan 2.1, Wan 2.7, HappyHorse 1.0이다.
- WAN 3.0의 존재와 사양은 알리바바 공식 문서에서 확인했다. 따라서 아래 비교에서 나무위키는 동향 참고 자료, 공식 제품 문서는 현재 사양의 근거로 사용했다.
- 두 모델 모두 30초급 멀티모달 영상과 오디오를 지향한다. WAN 3.0은 API·스토리보드·문서/URL 입력처럼 구조화된 제작 제어가 강하고, Seedance 2.5는 최대 50개 레퍼런스·4K·영역 편집처럼 크리에이터용 참조 워크플로가 강하다.

## 나무위키 수집 결과

대상: [영상 인공지능](https://namu.wiki/w/%EC%98%81%EC%83%81%20%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5)

Firecrawl v2가 HTTP 200으로 본문 67,744자를 수집했다. 본문 및 Firecrawl의 대상 질의 결과에서 확인된 내용은 다음과 같다.

- 2025-02-26: Wan 2.1 오픈소스 공개
- 2026-04-03: Wan 2.7 출시
- 2026-04-27: HappyHorse 1.0 출시
- `Wan 3.0`: 명시되지 않음
- Seedance 쪽은 2026년 2월 Seedance 2/2.0과 액션 장면 역량을 언급하지만, 이 문서만으로 Seedance 2.5의 현재 사양을 확정할 수 없음

따라서 “나무위키에서 WAN 3.0 정보를 얻었다”고 쓰는 것은 부정확하다. 이번 테스트에서 확인한 사실은 “현재 해당 문서가 WAN 3.0을 아직 다루지 않는다”는 것이다.

## 공식 문서 기반 비교

| 항목 | Alibaba WAN 3.0 | ByteDance Seedance 2.5 |
| --- | --- | --- |
| 제공 형태 | Alibaba Cloud Model Studio API, 정식 제공 | Dreamina 구독자 대상 지역별 순차 제공 |
| 기본 생성 길이 | 2~30초 | 최대 30초 |
| 추가 길이 주장 | 입력 영상과 출력의 합이 30초 이내 | 공식 제품 페이지는 표준 30초, 확장 모드 최대 180초를 안내. 단일 패스 모델 출력과 플랫폼 연장 기능은 구분 필요 |
| 해상도 | 480P, 720P, 1080P | 공식 제품 페이지 기준 4K |
| 입력·참조 | 텍스트, 첫/마지막 프레임, 이미지, 영상, 오디오, 문서 1개 또는 공개 웹페이지 1개 | 텍스트·스크립트·이미지·영상·음악·스타일 가이드 등 최대 50개 멀티모달 참조 |
| 세부 한도 | 참조 이미지 최대 10개, 참조 영상 최대 5개·합계 15초, 참조 오디오 최대 5개·합계 15초 | 공식 제품 페이지는 총 50개 참조를 안내하지만 유형별 한도는 미기재 |
| 오디오 | 대화, BGM, 효과음의 네이티브 생성 | 비디오·오디오 생성, 오디오 참조와 립싱크 지원 |
| 장면 구성 | 타임스탬프가 붙은 4~6초 단위 스토리보드와 최대 30초 다중 샷 내러티브 | 공식 출시 페이지에는 다중 샷 규격 미기재 |
| 편집·제어 | 요소 추가·제거·수정, 스타일·조명·대화 편집, 정·역·양방향 확장 | 타임스탬프·캐릭터·요소 단위 편집과 특정 영역만 재생성하는 부분 편집 |
| 접근 제약 | 모델·엔드포인트·API 키의 리전이 같아야 하며, 참조 모드와 첫/마지막 프레임 모드는 동시 사용 불가 | 유럽·아시아·중동·남미의 16세 이상 구독자 계정부터 순차 제공 |

## 무엇이 다른가

1. **제어 방식**  
   WAN 3.0은 API 파라미터, 참조 유형별 제한, 스토리보드 타임스탬프가 구체적이다. 자동화된 제작 파이프라인과 샷 단위 제어에 적합한 형태다. Seedance 2.5는 많은 레퍼런스를 한 번에 넣고 특정 영역을 다시 만드는 방향이 강조된다.

2. **출력 지향점**  
   WAN 3.0 공식 API의 최고 명시 해상도는 1080P다. Seedance 2.5 제품 페이지는 4K 출력을 내세운다. 다만 이 비교는 API 출력 규격과 서비스 프런트엔드의 마케팅 사양을 비교한 것이므로 동일 조건 벤치마크는 아니다.

3. **입력 범위**  
   WAN 3.0은 이미지·영상·오디오뿐 아니라 문서와 공개 웹페이지를 직접 입력으로 받는다. Seedance 2.5는 최대 50개의 창작 레퍼런스를 결합하는 쪽이 강점이다.

4. **편집 방향**  
   WAN 3.0은 장면 요소, 조명, 대화와 영상 길이 확장을 폭넓게 제어한다. Seedance 2.5는 전체 영상을 다시 만들지 않고 특정 구역·캐릭터·시점만 고치는 반복 제작에 초점을 둔다.

5. **근거 수준**  
   WAN 3.0의 현재 사양은 알리바바 공식 문서에서 확인됐다. 나무위키는 WAN 3.0을 명시하지 않으므로 보조 자료로만 사용했다. Seedance 2.5는 Dreamina 공식 출시·제품 페이지를 우선 근거로 삼고, 나무위키의 사용자 평가는 검증된 성능 수치가 아니므로 비교표에서 제외했다.

## 출처

- [나무위키 — 영상 인공지능](https://namu.wiki/w/%EC%98%81%EC%83%81%20%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5)
- [Alibaba Cloud — WAN 3.0 Video Generation Guide](https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-guide)
- [Alibaba Cloud — WAN 3.0 Release](https://modelstudio.console.alibabacloud.com/model-releases/wan3.0-video)
- [Dreamina — Seedance 2.5 Launch](https://dreamina.capcut.com/resource/seedance-2-5-launch)
- [Dreamina — Seedance 2.5 Product](https://dreamina.capcut.com/seedance/seedance-2-5)
- [나무위키 — Seedance](https://namu.wiki/w/Seedance)

## 재실행

저장소 루트 `.env`에 `FIRECRAWL_API_KEY`가 설정된 상태에서 실행한다.

```sh
python3 school/school_project/week5/crawlingTest/check_firecrawl.py
```

스크립트는 키 자체를 출력하지 않고 인증 성공, 페이지 상태, 수집 문자 수, `Wan 3.0` 정확 일치 여부만 표시한다.
실행할 때마다 Firecrawl 페이지 수집 크레딧이 사용될 수 있다.

---

# 스마트글래스 상품 리뷰 CSV

수집일: 2026-10-02 (Asia/Seoul)

## 산출물

- `smart_glasses_reviews.csv`: 국내 사이트의 한국어 리뷰 15건. 다나와 6건, 클리앙 5건, 네이버 블로그 1건, 티스토리 3건이다.
- `smart_glasses_reviews_ko.json`: 직접 확인한 리뷰 메타데이터, 짧은 원문 발췌 및 수집자가 작성한 요약의 정본이다.
- `collect_smart_glasses_reviews.py`: 저장한 스냅샷을 CSV로 변환하며, 선택적으로 Firecrawl v2 API에서 사용기 발췌를 재확인한다.
- `smart_glasses_review_evidence.json`: 수집 방법·URL·API 수집 ID·발췌 재확인 결과·제약을 기록한다.
- `archive/overseas_2026-10-02/`: 국내 리뷰 요청으로 대체된 이전 해외 리뷰 산출물을 보존했다.

다나와 쇼핑몰 구매후기 6건과 개인 사용기 9건을 `review_type`으로 구분한다. 상품은 Ray-Ban Meta·Stories, XREAL Air·Air 2 Pro, Rokid AI Glasses, Razer Anzu를 포함한다. 카메라형·AR 디스플레이형·오디오형을 `product_category`로 나눈다. CSV는 엑셀에서 한글을 읽기 쉬운 UTF-8 BOM 형식이다.

CSV에는 상품명, 사이트와 원 쇼핑몰(확인한 경우), 원문 평점·척도, 날짜, 작성자, 구매 진술, 제휴 고지, 짧은 발췌, 한국어 요약, URL 및 수집 방법을 담았다. 리뷰 전문은 저장하지 않았다.

## 수집 방법

`skillTest/.agents/skills/`의 쿠팡·네이버 쇼핑·다나와 검색 스킬을 참고해 후보 상품을 찾았다. 검색 API는 상품 정보만 제공하며 리뷰 본문은 제공하지 않았다. 사용기 9건은 루트 `.env`의 키로 Firecrawl v2 API에서 수집했다. 다나와 3개 상품 페이지는 API 결과에서 리뷰 본문이 노출되지 않아 ego-lite의 실제 `쇼핑몰 상품리뷰` 탭에서 6건을 보완했다. 다나와 표시는 원 쇼핑몰 리뷰의 집계이며 원 쇼핑몰 상세 페이지까지 직접 확인한 것은 아니다.

## 재실행

저장된 스냅샷으로 CSV를 다시 만드는 기본 실행은 API 키나 외부 패키지가 필요 없다.

```sh
python3 school/school_project/week5/crawlingTest/collect_smart_glasses_reviews.py
```

사용기 9건의 발췌를 출처에서 재확인하려면 루트 `.env`의 `FIRECRAWL_API_KEY`를 설정하고 아래를 실행한다. 크레딧이 사용되며 24시간 캐시를 허용한다.

```sh
python3 school/school_project/week5/crawlingTest/collect_smart_glasses_reviews.py --verify-sources
```

이 명령은 새 리뷰를 자동 추가하는 수집기가 아니라 기존 발췌 확인기다. 다나와 동적 리뷰와 새 글은 ego-lite/API로 재확인한 뒤 스냅샷을 갱신해야 한다. 네트워크 결과의 전체 본문이나 키는 저장·출력하지 않는다.

## 해석 시 주의

- 국내 사이트의 한국어 글이라는 뜻이며, 작성자의 국적·거주지나 국내 구매 여부를 확인한 것은 아니다. 해외구매 상품도 포함한다.
- 15건은 편의표본이다. 다나와 Rokid 3건은 기본 유용한 리뷰순 상단에서 가져왔으며 전체 구매자를 대표하지 않는다.
- 구매후기 평점은 화면의 80·100점과 척도 100을 그대로 저장했다. 사용기는 별점이 없어 결측으로 남겼다.
- 내돈내산·구매 진술은 작성자의 주장이다. 구매 인증 배지는 확인하지 않았다. 제휴 고지를 확인한 글은 따로 표시했다.
- 클리앙의 오라질 글 2건은 같은 작성자의 다른 사용기이며 독립 구매자 2명으로 집계하면 안 된다.
- 요약은 작성자의 경험을 정리한 것이며 제품 사양이나 현재 기능 지원을 검증한 정보가 아니다. 배송·포장 평가를 성능 평가와 혼합하지 않는다.
- 검증: CSV 재생성, 15행·중복·날짜·평점 범위·한국어·BOM 확인, API 사용기 발췌 9건 재확인, 저장소 기본 검사를 실행했다. 동적 후기 6건은 수집 시 실제 브라우저 화면을 확인했다.

## HTML 발표와 공개 배포

[GitHub Pages 발표](https://tony0055.github.io/data-literacy/presentation/) · [제작·검증·배포 기록](presentation/README.md)

`presentation/index.html`: 국내 리뷰 분석을 9장, 약 4분 10초로 정리했다. 10개 시각화와 Anime.js 그래프 모션, GPT 생성 콘셉트 표지, 발표 노트·전체화면·모션 줄이기를 포함한다. 원자료와 EDA 보고서 링크도 공개 배포했다. 별도 `gh-pages` 브랜치로 배포하며 기존 작업 파일과 키는 포함하지 않는다.

## EDA·시각화 HTML 보고서

- `smart_glasses_eda_report.html`: 데이터와 런타임을 포함한 단일 HTML 보고서. 인터넷 없이 열 수 있으며 차트 6개와 표 3개, 한국어 분석·한계·수집 설계를 포함한다.
- `build_review_eda.py`: CSV를 입력으로 결측·중복·평점 통계·사이트/유형/연도 분포와 수동 주제 코딩을 집계한다.
- `eda_summary.json`, `eda_snapshot.json`: 집계값, 원본 해시, 차트 데이터 및 분석 근거.
- `review_theme_coding.csv`: 리뷰 ID별 주제·서술 방향·판정 근거. 여러 주제를 허용하며 자동 감성 분석이 아니다.
- `eda-report/`: 편집 가능한 보고서 소스와 빌드 산출물. 공유 런타임을 사용하며 외부 CDN이나 추가 패키지 설치는 필요 없다.

평점이 있는 구매후기 6건의 평균은 93.3/100점이다. 사용기 9건은 별점 결측이며 평균에서 제외했다. 미디어 활용 언급 7건, 착용·디자인 및 AI·음성 각 6건은 수집 발췌·요약에 근거한 수동 분류 결과다. 이 표본에서 시장 만족도나 제품 순위를 추정하지 않았다.

CSV가 바뀌면 주제 코딩 사전도 재검토해야 한다. 보고서의 문장은 집계에 맞춰 함께 수정한다. 숫자만 갱신하면 고정 서술과 불일치할 수 있다.

```sh
python3 school/school_project/week5/crawlingTest/build_review_eda.py --sync-report
```

현재 설치된 Data 플러그인의 `scripts/data-app.mjs build --project-dir <eda-report 절대경로> --separate-data`로 빌드한다. `export-offline --project-dir <동일 경로> --output <동일 경로>/.data-app-offline/exports/smart_glasses_eda_report.html`로 내보낸 뒤 상위 crawlingTest 폴더에 복사한다. 보고서 ID는 재실행 시 보존한다.

검증: 집계값과 CSV 대조, 파이썬 컴파일, 보고서 빌드·오프라인 HTML 내보내기, 실제 ego-lite에서 차트 표시·검색과 전체 복원·390px 폭의 넘침을 확인했다. LSP 서버는 설치되어 있지 않아 사용하지 않았고 빌드와 실행으로 점검했다.
