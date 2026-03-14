# Agent Instructions

This directory is the three-layer memory system. For design details, see `docs/memory-system-design.md`.

## Structure
- `raw/` — Layer 1: Immutable session extractions (user-initiated, append-only, never delete)
- `curated/` — Layer 2: Distilled reusable knowledge (weekly digests + persistent topic files)
- `insights/` — Layer 3: Long-term stable insights (**user-confirmed only** — never modify without explicit user approval)
- `index.md` — Progressive disclosure entry point, loaded every session via CLAUDE.md

## Rules
- All capture is **pull-based** (user-initiated). Never auto-scan or auto-extract.
- Layer 1 (`raw/`) is immutable and append-only. Archive quarterly, never delete.
- Layer 3 (`insights/`) requires user approval for any modification. Use `.pending-reflection.md` for proposals.
- Use the `memory-ops` skill for all memory operations.
