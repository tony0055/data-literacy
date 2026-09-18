# OMO Light

Codex CLI용 선택적 플러그인입니다. Node/npm과 Codex CLI가 필요합니다. 아래 고정 버전은 베타입니다.

```sh
npx lazycodex-ai@5.0.0-beta.50 install --no-tui --no-codex-autonomous
npx lazycodex-ai@5.0.0-beta.50 doctor
```

설치기는 전역 `~/.codex`와 `~/.local/bin`을 변경합니다. `--no-codex-autonomous`는 기존 권한 설정을 유지합니다. 설치 후 새 세션에서 플러그인·MCP가 보이는지 확인하고 작은 `ultrawork` 작업으로 수정 결과와 검사를 확인하세요. 앱에서의 도구 노출은 별도로 확인합니다.

작업 분배·실행 루프·에이전트 모델은 OMO가 관리합니다. 프로젝트 기본 모델이 OMO 작업자의 모델까지 바꾸지는 않습니다. OMO의 Context7·grep MCP와 실행 루프를 프로젝트에 중복 등록하지 마세요.

업데이트와 상세 설정은 [OMO 설치 안내](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/installation.md)를 확인하세요.
