---
name: semantic-search
description: |
  Semantic similarity search across the knowledge base. Goes beyond keyword matching
  to understand conceptual relationships. Covers the memory three-layer structure
  and contexts/ external resources.

  Acts as a capability enhancer for memory-ops navigate: when the knowledge base
  grows too large for the LLM to read in full, semantic search provides pre-filtering
  to find the most relevant fragments before navigate synthesizes them.

  Use when user wants to:
  - Search meeting transcripts for a topic's history (even without exact keywords)
  - Find semantically related historical thinking, retrospectives, or design discussions
  - Do cross-layer semantic association in the memory three-layer structure
  - Pre-filter for navigate when there are too many files to read
  - Disambiguate: find the most relevant historical definition or context

  Triggers: "semantic search", "search by meaning", "find related", "what's related to", "search knowledge base"
---

# Semantic Search Skill

Semantic search infrastructure. Source of truth remains markdown files + git; the embedding cache is a rebuildable acceleration index.

## Positioning

**Not** a replacement for navigate, **is** an accelerator for navigate.

| Scenario | Use navigate | Use semantic-search |
|----------|-------------|-------------------|
| Few memory files (<20) | LLM reads directly | Not needed |
| Known exact keyword | grep is sufficient | Not needed |
| 50+ conversation transcripts | Can't read all | Pre-filter |
| Cross-topic semantic association | Keywords don't match | Understands semantics |
| "Have we discussed X before?" | Try navigate first | Use if navigate falls short |

## Knowledge Asset Map

Scope presets correspond to actual project structure:

| Scope | Covered Paths | Use Case |
|-------|--------------|----------|
| `full` | memory three layers + all contexts | Default, breadth-first |
| `memory` | insights/ + curated/ + raw/ | Search personal memory |
| `conversations` | contexts/conversations/*.md | Search meeting transcripts |
| `contexts` | conversations/ + survey_sessions/ | Search all external inputs |

## Usage

### Prerequisites

- `.env` with an embedding API key (e.g., `OPENAI_API_KEY`)
- Python 3.10+ and `openai` package

### Core Command

```bash
python .claude/skills/semantic-search/scripts/main.py \
    --query "<natural language query>" \
    --scope full \
    --top-k 10
```

### Auto-scope (Recommended)

When `--scope` is omitted, defaults to `full`. The agent should choose based on query intent:
- User asks about "meeting discussions" → `--scope conversations`
- User asks about "my previous thoughts" → `--scope memory`
- Uncertain → omit, defaults to full

## Output Format

JSON output to stdout, status info to stderr:

```json
{
  "query": "discussions about oncall improvements",
  "scope": "full",
  "files_searched": 22,
  "total_chunks": 187,
  "results": [
    {
      "score": 0.8723,
      "source_file": "contexts/conversations/20260310_AI_Oncall_Sync.md",
      "layer": "contexts",
      "heading": "## Topic 2: Oncall Process Optimization",
      "text": "..."
    }
  ]
}
```

- `score`: cosine similarity (0-1), > 0.8 highly relevant, 0.7-0.8 related, < 0.7 weak
- `layer`: `L3-insights` / `L2-curated` / `L1-raw` / `contexts`
- `text`: first 500 chars preview. Read source_file for full content.

## Integration with memory-ops

When `navigate` is triggered and search scope is large, recommended flow:

```
1. Run navigate standard flow (read index.md → grep Layer 3/2/1)
2. If standard flow results insufficient:
   → Call semantic-search for top-k relevant fragments
   → Use those fragments to guide navigate's deep reading
3. Synthesize results, organize by layer, annotate provenance
```

## Cache Management

- Cache location: `.semantic_cache/` (gitignored)
- Indexed by file content hash — auto-invalidated when files change
- Rebuild cache: `--rebuild-cache`
- Delete cache: `rm -rf .semantic_cache/` (always rebuildable)

## Notes

- Embedding computation requires API calls with associated costs
- First search computes all embeddings; subsequent searches only process new/changed files
- Read-only — never modifies source files, only writes to cache
- Excludes AGENTS.md, CLAUDE.md, .gitignore, .py, .sh and other non-knowledge files
