# 2026-09-11 2D 마인크래프트 (웹)

## 실행

```sh
python3 -m http.server 8000
# http://localhost:8000/web/index.html
```

외부 의존성 없음. 정적 파일만으로 동작.

## 조작

- 이동: A/D, ←/→
- 점프: Space, W, ↑
- 캐기: 마우스 왼쪽 (6타일 반경)
- 설치: 마우스 오른쪽
- 선택: 1–8, 휠, 핫바 클릭
- 제작: 통나무 1 → 판자 4
- 저장: 10초 자동 + 종료 전 + 저장 버튼
- 도움말: H

## 구조

- `web/index.html`: 캔버스, 상단바(FPS/좌표/시간/시드), 핫바, 도움말, 터치 버튼.
- `web/styles.css`: 전체화면 캔버스, 상단바, 핫바 슬롯 UI.
- `web/main.js`: 160×72 월드, 12종 타일, 시드 생성, 동굴·나무·광석, AABB 물리, 낮주기, localStorage 저장.
- `tests/test_web_game.py`: 파일 존재, HTML 구조, 무의존, `node --check`, 핵심 심볼, 월드 상수, 생성·캐기 스모크.

## 검증

- `python3 scripts/verify.py`: 15 tests OK.
- `node --check web/main.js`: OK.
