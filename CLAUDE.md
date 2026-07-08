# fullsend-skill

Standalone packaging of the `/fullsend` agent skill for Claude Code.

## Project structure

- `skills/fullsend/` — the fullsend skill, installable via `npx skills add`
  - `SKILL.md` — skill definition (routing, essential principles, troubleshooting)
  - `references/` — per-command reference docs (validate, inspect, trigger, watch, etc.)
  - `scripts/` — command metadata and helper scripts

## Conventions

- Skill content is the source of truth — consuming repos install from here
- Changes to the skill go here first, then propagate via reinstall
- Reference docs follow the pattern: Usage, Prerequisites, Procedure, Report
