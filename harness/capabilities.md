# Capabilities · 도구를 고르는 자리

아래는 후보다. 설치·연결·로그인·크레딧을 보증하지 않는다 — 쓰기 전에 지금 세션에서 실제로 되는지 확인하고, 다른 에이전트의 연결 상태를 승계했다고 가정하지 않는다. 도구가 없으면 알리고 임의로 제공자를 바꾸지 않는다.

| 필요한 능력 | 후보 | 쓰기 전에 확인할 것 |
| --- | --- | --- |
| 웹 조사·페이지 읽기·로그인 사이트·스크린샷 | ego-lite — `ego-browser` 스킬을 읽고 `ego-browser nodejs`. 작업자도 같다 | 원출처에 닿는지. 다 쓰면 작업 공간을 닫는다 |
| 정해진 사이트의 반복·대량 수집 | Firecrawl | 키는 저장소 루트 `.env`의 `FIRECRAWL_API_KEY`로만 둔다 — 출력·커밋·문서 복사 금지. 크레딧 |
| PDF·HWP·관공서 표를 텍스트로 | `kordoc` 스킬(MCP가 없으면 `npx -y kordoc@^4`). 통계 원표는 `pdftotext -layout`으로 전사해 대조 | `NEEDS_OCR`·`SKIPPED_IMAGE` 경고면 `--ocr` |
| 메모리 검색·Notion·Gmail·Slack 어댑터 | Aside | 사용자가 "aside로"라고 할 때나 대체재가 없을 때만, 쓰는 이유를 밝힌다 |
| 분석·차트 | Python 스크립트·노트북 | 프로젝트 README의 실행법. 실제로 돌린 출력으로 보고한다 |
| 덱 렌더·넘침·모션 검사 | 덱 폴더의 `scripts/render.ts` 등(Bun + Chrome) | 그 덱 README의 명령 |
| 발표 링크 공개 | `gh` + GitHub Pages — [배포 절](../docs/data-to-slides-workflow.md#7-github-pages-배포-요청승인-있을-때만) | 사용자 요청·승인. 공개 저장소에 비밀 키·내부 로그를 넣지 않는다 |

캡차·봇 챌린지는 풀지 않는다. 만나면 사용자에게 알리고 다른 경로를 찾는다.
