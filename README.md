# Codex Harness

한국어 응답, 프로젝트 문맥, 검증 명령과 paperthin 조합을 제공하는 경량 하네스입니다.

## 설정

Python 3.11 이상과 Codex가 필요합니다. 프로젝트 루트에서 실행합니다.

```sh
python3 scripts/activate.py
python3 scripts/verify.py
```

활성화는 `.codex/config.toml`과 `.agents/skills/`를 생성합니다. 기존 파일이 다르면 덮어쓰지 않습니다. 충돌 시 모델 설정은 [프리셋](harness/models.json), 스킬은 `harness/skills/`와 비교해 기존 고유 설정을 보존하며 병합하세요. `--dry-run`으로 생성 대상을 확인할 수 있습니다.

프로젝트를 신뢰하고 새 Codex 작업을 여세요. 이미 선택한 모델이 있으면 앱의 모델 선택기 또는 CLI `/status`에서 실제 적용값을 확인합니다.

## 모델

- 일반 작업 `standard`: GPT-5.6 Sol / medium
- `light`: GPT-5.6 Terra / high

전체 프리셋은 [harness/models.json](harness/models.json)에 있습니다. 최초 활성화 시 `--preset light`처럼 선택합니다. 이후에는 모델 선택기 또는 `.codex/config.toml`에서 변경합니다. 프리셋은 자동 갱신되지 않습니다.

## 스킬 조합

| 호출 | 실행 순서 | 결과 |
| --- | --- | --- |
| `$harness-next` | nba → modelchk | 다음 행동 하나와 모델 역량·추론 강도 제안 |
| `$harness-context-clean` | ssotize → re0 → debloat → reorder | 지정 문서 정리. 기본 대상은 ontology |

[paperthin](https://github.com/LilMGenius/paperthin)의 위 여섯 스킬이 필요합니다. 전역 설치를 재사용하며, 누락되면 조합이 알려줍니다. 각 단계는 실제 스킬 지침을 읽고 결과를 다음 단계로 넘깁니다. 문맥 정리 중 통합 승인이 필요하면 해당 단계에서 멈춥니다. `next`는 읽기 전용이며 모델을 변경하지 않습니다.

앱에서는 스킬을 선택하거나 “harness-context-clean 조합 실행해줘”라고 요청합니다. 선택 목록에 보이지 않으면 새 작업을 여세요. [공식 스킬 안내](https://learn.chatgpt.com/docs/build-skills)

## 프로젝트에 맞추기

외부 리서치는 **Aside MCP**를 우선 사용합니다. 연결된 실제 도구를 확인해 조사하고 중요한 주장은 원문 근거를 검증합니다. Aside가 연결되지 않았다면 연결 필요 상태를 알리며 다른 리서치 서비스로 자동 전환하지 않습니다.

- [AGENTS.md](AGENTS.md): 작업 규칙. 기존 프로젝트 규칙과 병합합니다.
- [docs/ontology.md](docs/ontology.md): 목표·용어·결정과 이유·진행 상태·미해결 질문. 실제 프로젝트 내용으로 채웁니다.
- [harness/checks.json](harness/checks.json): 유한 실행 검사 명령을 인자 배열로 등록합니다. 현재는 하네스 자체 테스트이며, 앱에 적용할 때 lint·타입 검사·테스트로 바꿉니다. 빈 목록은 `SKIPPED`, 실패는 실패 코드로 반환합니다. 자동 종료 훅은 없습니다.

다른 프로젝트에는 `harness/`, `scripts/`, `docs/`와 작업 규칙을 가져가고 기존 문맥과 설정을 보존하세요. 활성화된 스킬을 수정할 때는 `harness/skills/`의 원본과 `.agents/skills/`의 적용본을 함께 맞춥니다.

OMO는 선택 사항입니다. 설치와 운영은 [OMO 안내](docs/omo.md)를 참고하세요.
