# Project harness

Reply to the user in Korean. Keep maintained instructions concise.

## Working agreement

- Establish the requested outcome and acceptance criteria from the request and repository. Make routine implementation decisions autonomously; ask when a missing product decision changes the outcome.
- Use Plan → Explore → Build → Review as phases of one task, not four mandatory agents. Skip unnecessary phases for small changes.
- Use Aside MCP as the primary tool for external research. Discover its available tools instead of assuming method names. Verify consequential API/version claims against original official sources and cite them. If Aside is unavailable, report the missing connection; do not silently substitute Exa or another research provider. Continue independent local inspection and label anything unverified.
- Complete authorized work through relevant verification. Report actual checks and their outcomes; skipped checks are not passes. Use `python3 scripts/verify.py` for the configured project checks.
- For repeated failures, change the hypothesis before retrying. If progress requires external access or a user decision, preserve evidence and state the blocker.
- Preserve unrelated changes and credentials. Do not force-push or switch branches arbitrarily.

## Context and ownership

- On re-entry or long tasks, read `docs/ontology.md`; verify its state against live files. Preserve separate goal, vocabulary, decision/reversal reasons, state (Done / In progress / Next gate), and open questions. Update after meaningful milestones.
- OMO, when installed and explicitly invoked, owns orchestration, worker roles, loop state, and its MCPs. Do not add a second loop, parallel-agent roster, or duplicate Context7/grep servers. Ordinary tasks use the native Codex workflow.
- `$harness-next` composes paperthin nba → modelchk; `$harness-context-clean` composes ssotize → re0 → debloat → reorder. Load their installed instructions when requested. Sources live under `harness/skills/`; activation and dependencies are in `README.md`.
- Model IDs and effort presets live in `harness/models.json`. Do not claim prose changed the running model. Honor the user's selected model; model changes require a supported client control or an explicit launch option.
- Read `docs/omo.md` only for OMO installation or interoperability work.

## Keep it light

Do not require paperthin, recurring reviews, new rules, or multi-agent work for every edit. Add instructions only for a repeated, project-specific need. Review for duplication near seven instruction files or sixty lines in one rule.
