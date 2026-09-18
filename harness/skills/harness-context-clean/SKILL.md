---
name: harness-context-clean
description: Run the paperthin ssotize, re0, debloat, and reorder sequence on project ontology or a user-selected document when the user requests this cleanup combo.
---

Required installed skills: `ssotize`, `re0`, `debloat`, `reorder`. Resolve them from the current skill catalog and read each actual `SKILL.md` before its step. User-level skills may be under `~/.agents/skills` or `~/.codex/skills`; use the discovered path. If a dependency is missing, report it and stop rather than simulate it.

Use the user's target, or default to `docs/ontology.md` relative to the project root. Explicitly requesting this combo requests its named sequence, including the user-invoked `debloat` and `reorder` steps. Do not automatically start the full combo just because a milestone or 150-line threshold was reached; suggest it instead. Do not infer permission for unrelated files or external changes.

1. Apply `ssotize`: audit the target and relevant sources, report duplicates and a concrete consolidation plan. Honor its approval requirement. If session authorization already covers the specific changes, use it; otherwise pause before mutation and retain the pending plan. Do not run later mutating steps while this gate is pending. If there is no consolidation to do, record a no-op and continue.
2. Apply `re0` to the resulting target: reconcile stale information against evidence and produce a clean current document.
3. Apply `debloat` to that result: remove padding while retaining all load-bearing meaning.
4. Apply `reorder` last: name one ordering principle, move items only, and verify no content was added, removed, or reworded during this step.

Pass each step's actual artifact and findings to the next. Report completed, no-op, or pending status per step in Korean; do not call a partial chain complete. The sequence is executed by the agent in this task, not by shell slash commands or a background loop.

For ontology, preserve Goal, Core vocabulary, Decision log, Current state, and Open / needs human judgment as separate sections. Keep Done / In progress / Next gate distinct. Preserve decision and reversal reasons, unique constraints, unresolved disagreements, and evidence links even when compressing. Fill template sections only from established project facts. OMO loop state and evidence remain owned by OMO; reference rather than rewrite them. Do not silently decide product direction or delete implementation during document cleanup.
