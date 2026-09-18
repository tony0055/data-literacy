@AGENTS.md

## Claude Code notes

Skills live in `~/.agents/skills/` and are symlinked into `~/.claude/skills/`. The `~/.agents/skills/` copies are canonical; `harness/skills/` in this repo is an older Codex-activation source and is not what runs here. Edit the canonical copy.

`scripts/activate.py` writes `.codex/config.toml` and `.agents/skills/` for Codex. It does not configure Claude Code, and the model presets in `harness/models.json` are Codex model IDs — they do not apply to the model running here.
