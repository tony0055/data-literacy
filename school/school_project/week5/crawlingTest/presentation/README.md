# 스마트글래스 리뷰 발표

국내 리뷰 15건의 EDA를 9장, 약 4분 10초의 HTML 발표로 재구성했다. 입력은 `../eda_snapshot.json`, 평점 분모는 6건이며 주제 코딩은 다중 분류다. 시장 대표성·브랜드 순위·현재 AI 지원 상태를 추론하지 않는다.

## 계획과 완료 기준

1. 원자료 집계에서 발표 흐름과 그래프 생성.
2. GPT 이미지 표지와 Anime.js 그래프·문장 모션 구현.
3. ego-lite에서 9장 렌더·영역 넘침·이동·재생·동작 줄이기·전체화면·발표 노트 확인. 실패는 수정 후 관련 검사만 재실행.
4. 별도 `gh-pages` 체크아웃에 공개 산출물만 배포하고 실제 Pages URL 검증.

## 실행과 산출물

```sh
python3 school/school_project/week5/crawlingTest/presentation/build_slides.py
```

- `index.html`: 이미지·Anime.js를 내장한 단일 HTML. 글꼴은 네트워크 실패 시 시스템 글꼴로 표시한다.
- `deck-template.html`, `build_slides.py`: 재생성 소스.
- `script.md`: 슬라이드별 발표 대본.
- `assets/smart-glasses-hero-v1.png`: GPT 생성 콘셉트 이미지. 특정 실제 제품의 사진이 아니다.
- `assets/anime-4.5.0.umd.min.js`, `ANIME-LICENSE.md`: [Anime.js v4.5.0 공식 소스](https://github.com/juliangarnier/anime/tree/v4.5.0), MIT.

시각화 10개(사이트·유형·분류·연도·평점·주제·3개 주제별 구성·결측 행렬). Anime.js의 막대 reveal, 세로 막대 성장, 문장·행렬 stagger를 사용하며 그래프 값은 원자료의 최종값을 고정한다. OS 모션 감소 설정과 수동 토글을 지원한다. Manim 영상은 사용하지 않았다.

조작: 방향키/Space 이동, F 전체화면, S 발표 노트, R 모션 재생. 인쇄는 전체 9장을 출력한다.

## 검증 기록

2026-10-02: ego-lite 1280×720에서 9장 모두 검사한 요소의 슬라이드 영역 넘침 0, 생성 이미지 로딩, Anime.js 실행, 이동·전체화면·모션 감소·노트 팝업 확인. 오류 수집 결과 0. 표지·주제 차트 화면을 직접 확인했다. 노트의 다음 제목 빈 문자열 문제를 수정했다. 저장소 기본 검증 19개 통과.

수정 후 노트의 다음 제목 정상 표시를 재확인했다. 844×390 모바일 가로 화면을 직접 확인했고, OS 모션 감소에서 실행 모션 0개, 인쇄 매체에서 9장 표시·제어부 숨김을 확인했다. PDF 출력 파일 자체는 생성하지 않았다.

## 배포

GitHub CLI 인증을 사용해 별도 체크아웃의 `gh-pages` 브랜치를 푸시하고 Pages 소스를 설정했다. `main`과 기존 작업 트리는 배포 커밋에 포함하지 않았다.

- URL: https://tony0055.github.io/data-literacy/presentation/
- 배포 커밋: `a0bf6ffd58233f5b4a1e296865651b8fb4153179`
- 공개 파일 7개: 루트 진입 HTML, `.nojekyll`, 발표 HTML, Anime.js 라이선스, EDA HTML, 리뷰 CSV, 주제 코딩 CSV.
- 키·API 실행 로그·사용자 작업 파일은 포함하지 않았다.

Pages 배포 실행 `36956505179` 성공. 공개 주소를 ego-lite로 열어 9장, 이미지 로딩, Anime.js 실행·다음 이동·재생·차트 화면을 확인했다. EDA HTML·리뷰 CSV·코딩 CSV 링크 모두 HTTP 200, 수집된 런타임 오류 0. JS 구문 검사와 CSV SHA-256 일치 검사도 통과했다. GitHub 자동 생성 워크플로의 Node 20 사용 중단·러너 이미지 변경 안내는 있었으며 빌드/배포 실패는 없었다.
