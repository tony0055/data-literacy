---
name: harness-next
description: Run the paperthin nba then modelchk sequence to recommend one next action and size its model effort, without executing the action.
---

Required installed skills: `nba`, `modelchk`. Resolve them from the current skill catalog and read each actual `SKILL.md` before its step. User-level skills may be under `~/.agents/skills` or `~/.codex/skills`; use the discovered path rather than assuming a fixed machine path. If a dependency is missing, identify it and stop instead of imitating its behavior or claiming completion.

1. Read `docs/ontology.md` relative to the project root and verify relevant live state. Apply `nba` to produce exactly one next action, its evidence, and its done-when condition.
2. Pass that action, its scope, and its verification condition to `modelchk`. Apply its risk-and-complexity assessment and preserve both recommended tier and effort intent, rationale, adjustment triggers, and proof surface.
3. As a separate harness recommendation, consult `harness/models.json`. Honor the user's selected preset; report a mismatch if the advisory sizing differs. Do not change the running model, write configuration, or launch agents.

Reply in Korean with the one next action and the sizing result. This combo is read-only: it does not execute the recommended action. If the user separately authorized implementation, finish this advisory sequence before continuing that work outside the combo. Do not turn a template's placeholder text into assumed project facts.
