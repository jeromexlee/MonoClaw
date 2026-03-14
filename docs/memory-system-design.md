# Three-Layer Memory System Design

## Context

This repo serves as a personal AI runtime — a "digital body" in the cyber cultivation framework. The core problem: every AI session starts from scratch. Learnings, decisions, user preferences, and domain insights vanish when a session ends. CLAUDE.md provides behavioral instructions but no accumulated memory.

This design introduces a three-layer memory system that captures, distills, and crystallizes knowledge from ongoing AI sessions into a progressively refined, persistent knowledge base.

## Design Principles

1. **AI-first, human-readable.** All memory is stored as markdown files in the repo. AI can consume them natively; humans can read and edit them in any text editor.

2. **Append-only raw layer.** Layer 1 raw logs are immutable. Never delete, only archive. This preserves provenance for when distilled knowledge needs to be traced back to its source.

3. **Progressive disclosure for retrieval.** AI loads a compact index at session start (~100 lines). Detailed files are loaded on-demand when a task requires deeper context. This keeps the context window budget tight.

4. **User sovereignty over identity.** Layer 3 (long-term insights) can only be updated with explicit user confirmation. The AI proposes changes; the user approves. This prevents identity drift.

5. **File-based, not database.** No vector stores, no SQLite. Everything is `.md` files tracked by git. Portable, diffable, version-controlled.

---

## Architecture Overview

```
Session (ephemeral)
    │
    ├─── [A] Real-time capture ──────► memory/curated/   (Layer 2, direct)
    │    (user says "remember this",
    │     AI writes refined insight)
    │
    └─── [B] On-demand extraction ──► memory/raw/   (Layer 1)
         (user says "save this session",
          AI extracts from current session)
                                           │
                                           ▼ (weekly distillation, automated)
                                      memory/curated/   (Layer 2)
                                           │
                                           ▼ (monthly reflection, user-confirmed)
                                      memory/insights/   (Layer 3)
                                           │
                                           ▼ (always loaded)
                                      memory/index.md → embedded in CLAUDE.md

External sources (user-initiated only):
  contexts/conversations/*.md  ──► "digest this meeting" ──► memory/curated/
  contexts/survey_sessions/*.md ──► "digest this research" ──► memory/curated/
```

**All capture is user-initiated (pull-based).** The system never automatically scans or extracts from any source. The user decides what's worth remembering.

---

## Layer 1: Raw Session Log

### Purpose
Comprehensive capture of selected AI sessions that the user deems worth preserving. Not every session gets captured — only sessions with thinking, design, strategy, or significant learning get saved here. The user explicitly triggers capture.

### Capture Mechanism B: User-Initiated Session Extraction

When the user says "save this session", the `memory-ops` skill:

1. Reads the current session
2. Extracts knowledge via LLM (decisions, learnings, patterns, open questions, user context)
3. Outputs to `memory/raw/YYYY-MM-DD.md`, appending the extraction

### Provenance Resilience

The provenance chain has three levels:

```
curated entry → raw log → session transcript
  (git tracked)   (git tracked)   (machine-local, NOT git tracked)
```

**Design rule: the raw log must be self-contained.** Each extracted item includes a `Context:` field with the essential quoted excerpt from the original conversation. The session reference is best-effort provenance — useful when available, but not required for the raw log to be independently useful.

### Raw Log Format

```markdown
# YYYY-MM-DD

## Session: [session_id_short] ([session title or topic])
_Extracted: [timestamp] | Messages: [count] | Duration: [duration]_

### Decisions
- [summary]
  - Context: [self-contained context]
  - Source: [session_id]#msg-[range]

### Learnings
- [summary]
  - Context: [self-contained context]
  - Source: [session_id]#msg-[range]

### Patterns
...

### User Context
...
```

---

## Capture Mechanism A: Real-Time Refined Capture

During a session, the AI sometimes identifies high-value insights that are already refined enough to go directly to Layer 2 (curated knowledge). This path skips Layer 1 and writes distilled content in real-time.

CLAUDE.md includes instructions for this behavior. A and B never conflict because they write to different locations. When L1→L2 distillation runs, it deduplicates against what A already captured.

---

## Layer 2: Curated Knowledge

### Purpose
The 10% signal extracted from the 90% noise of daily operations. Organized by topic, with provenance links back to Layer 1.

### Structure

```
memory/curated/
  YYYY-WNN.md              ← Weekly digest (auto-generated from raw/)
  topics/                  ← Persistent topic files
    ai-workflow-patterns.md
    system-design-knowledge.md
    codebase-conventions.md
    ...
```

### Topic File Format

```markdown
# [Topic Name]

_Primary category: [category]_
_Facets: [facet1], [facet2]_

## Entries

### YYYY-MM-DD: [One-line summary]
[1-3 sentences]
- Source: raw/YYYY-MM-DD.md#session-[id]
```

### Provenance Pattern

Every Layer 2 entry includes a `Source:` field pointing to the Layer 1 raw log. Three levels of depth: curated summary → raw extraction → original transcript. Progressive disclosure at the data layer.

---

## Layer 3: Long-Term Insights

### Purpose
Stable, slow-changing knowledge about the user's thinking patterns, values, preferences, and domain expertise. This is the "personality" layer. Updated rarely and only with user confirmation.

### Taxonomy Rules

**Rule A**: Single primary category, multiple facets. Each insight document has exactly one primary category.

**Rule B**: "Who is responsible?" determines primary category. When an insight spans multiple domains, the owning domain gets the primary category.

**Rule C**: Cross-cutting concepts become topics, not categories. If a concept appears across many primary categories, it becomes a topic collection in curated/topics/.

### Insight File Format

```markdown
# [Category Name]

_Primary category: [name]_
_Facets: [dimensions]_
_Last updated: YYYY-MM-DD (user-confirmed)_
_Update history: Created YYYY-MM-DD_

## Core Insights

### [Insight title]
[Description of the insight and how it manifests]
- Emerged from: [curated sources]
- Stability: stable (observed across N+ months)
```

---

## Retrieval: Progressive Disclosure

`memory/index.md` is a compact (~100-120 lines) file that gets loaded every session. It gives the AI:

1. **User Profile** — 5-line summary
2. **Domain Insight Directory** — one line per Layer 3 file
3. **Recent Working Memory** — last 7-10 days of curated highlights

---

## Trigger Summary

| Process | Frequency | Trigger | Output | Human Approval |
|---------|-----------|---------|--------|----------------|
| A: Real-time capture | Per session | AI identifies insight | curated/topics/ | No |
| B: Session extraction | On-demand | User says "save session" | raw/YYYY-MM-DD.md | No |
| Ingest meeting | On-demand | User says "digest meeting" | curated/topics/ | No |
| Ingest survey | On-demand | User says "digest research" | curated/topics/ | No |
| L1→L2 distillation | Weekly | `jobs/memory-distill/` | curated/YYYY-WNN.md + topics/ | No |
| L2→L3 reflection | Monthly | `jobs/memory-reflect/` | insights/.pending-reflection.md | **Yes** |
| Index update | Weekly | Part of distillation | index.md | No |

---

## Implementation References

### A. Two-Phase Memory Management (mem0 pattern)

**Phase 1 — Fact extraction**: LLM extracts atomic facts from conversation.
**Phase 2 — Memory decision**: For each fact, compare against existing memory and decide: ADD (new), UPDATE (more detailed), DELETE (contradicted), or NONE (already known).

This pattern applies directly to L1→L2 distillation.

### B. Selective Recording Heuristic

> Record only what would be "painful to rediscover":
> - YES: Non-obvious gotchas, architectural decisions with rationale, security requirements
> - NO: Incremental steps, obvious implementations, routine config changes

### C. Observation Taxonomy

Type dimension: `bugfix | feature | refactor | change | discovery | decision`
Concept dimension: `how-it-works | why-it-exists | what-changed | problem-solution | gotcha | pattern | trade-off`

Useful for structuring extraction prompts.
