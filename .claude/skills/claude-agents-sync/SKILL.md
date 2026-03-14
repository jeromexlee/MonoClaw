---
name: claude-agents-sync
description: Ensure every new CLAUDE.md is paired with an AGENTS.md in the same directory, where AGENTS.md references CLAUDE.md.
---

# CLAUDE + AGENTS Pairing

When creating a new `CLAUDE.md`, always create an `AGENTS.md` in the same directory.

Note: This is an OpenCode skill file. Claude Code itself typically does not read `.claude/skills/*`; it reads project instructions from `CLAUDE.md`.

## Required behavior

1. If `{dir}/CLAUDE.md` is created, also create `{dir}/AGENTS.md`.
2. Keep `AGENTS.md` minimal and point to `CLAUDE.md` as the source of truth.
3. If `AGENTS.md` already exists, update it to ensure it references `CLAUDE.md`.

## AGENTS.md template

Use this exact minimal template unless the user asks for additional content:

```md
# Agent Instructions

This directory uses `CLAUDE.md` as the source of truth for agent behavior.

For all instructions, see `./CLAUDE.md`.
```
