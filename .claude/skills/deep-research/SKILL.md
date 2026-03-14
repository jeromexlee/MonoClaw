---
name: deep-research
description: |
  Structured deep research workflow for comprehensive, verifiable third-party investigations.
  Uses parallel sub-agents with intentional overlap to enable cross-validation and discover contradictions.

  Use when user wants to:
  - Research a product, service, course, or company thoroughly
  - Investigate controversial topics with multiple perspectives
  - Conduct due diligence before major decisions
  - Find and cross-validate information from multiple sources

  Triggers: "deep research", "research this", "due diligence", "investigate", "/research"
---

# Deep Research Workflow

> **Requires**: An AI agent with sub-agent capabilities (e.g., OhMyOpenCode `task()`, Claude Code sub-agents)

Systematic research methodology that uses parallel sub-agents with overlapping dimensions to enable cross-validation, discover contradictions, and produce traceable conclusions.

## Core Principles

1. **Cross-Validation**: Multiple sub-agents research overlapping topics to discover contradictions
2. **Traceability**: ALL citations must include URLs - no anonymous "someone said"
3. **Progressive Focus**: Broad scan first, then deep dive into specific dimensions
4. **Single Delivery**: Only the final report is saved - no intermediate files

## Quick Start

When triggered, clarify the research target:

```
"Let's do a deep research. First, let me confirm:
1. What's the research target? (product/course/company/opinion/technology)
2. What's your primary concern? (reviews/pricing/controversy/technical details)
3. Any specific claims you want verified?"
```

## Phase 1: Initial Scan

**Goal**: Quickly understand the landscape, identify key dimensions for deep research.

**Actions**:
1. Use web search for 2-3 searches covering:
   - Basic info: What is it?
   - Market perception: What do people say?
   - Controversy: What criticisms exist?
2. Identify 3-5 dimensions that need deeper investigation

**Output**: Mental notes only - no files saved

**Search tips for balanced results**:
- Always include negative searches: "criticism", "negative review", "scam", "overpriced"
- Search in multiple languages for non-English products/services

## Phase 2: Split & Parallel Research

**Goal**: Deep dive from multiple angles with intentional overlap for cross-validation.

### Dimension Design Principles

**Critical**: Dimensions MUST have ≥50% overlap to enable cross-validation.

| Bad (No Overlap) | Good (With Overlap) |
|------------------|---------------------|
| Price, Features, Reviews | User Experience (touches reviews, value), Price Analysis (touches reviews, value), Success Stories (touches reviews, features) |

### Launching Sub-Agents

Launch 3-5 sub-agents in parallel, one per dimension. Use librarian-type agents for external research.

**Important**:
- Sub-agent results are INTERMEDIATE — do NOT save to files
- Do NOT poll for results — the system notifies on completion
- Collect all results after notification

### Sub-Agent Prompt Template

```
You are a researcher investigating [TARGET]'s [DIMENSION].

Tasks:
1. Search and collect information about [SPECIFIC FOCUS]
2. Also collect related [OVERLAPPING TOPICS]

Requirements:
- Every finding MUST include a URL
- Preserve original quotes, don't just summarize
- If engagement data (likes/comments) exists, preserve it
- Search for both positive AND negative information
- Prioritize independent sources (personal blogs, forums, review articles) over official marketing

Do NOT:
- Write any files
- Summarize — return raw findings

Return format:
## Finding 1
**Source**: [description] (URL)
> Original quote
>
> (engagement data if available)

## Finding 2
...
```

## Phase 3: Integration & Cross-Validation

**Goal**: Identify contradictions, assess credibility, form conclusions.

### Comparison Framework

| Signal | Credibility | Action |
|--------|-------------|--------|
| Multiple agents found same info | HIGH | Use as key finding |
| Only one source | MEDIUM | Note source, flag for verification |
| Contradictory info | REQUIRES ANALYSIS | Highlight contradiction, analyze why |

### Handling Contradictions

When contradictions are found:
1. Note the specific contradiction
2. Analyze possible reasons (different time periods? different user segments? bias?)
3. If critical, launch targeted sub-agent to verify
4. Present both views with analysis in final report

## Phase 4: Write Final Report

**File Location**: `contexts/survey_sessions/<topic>_survey_YYYYMMDD.md`

### Report Structure

```markdown
# [Research Target] Deep Research Report

**Date**: YYYY-MM-DD
**Dimensions**: [list of research dimensions]

## Core Conclusions
[3-5 sentences summarizing key findings with credibility assessment]

## Per-Dimension Analysis

### [Dimension 1]
#### Key Findings
- **Finding 1** ([source description](URL))
  > Original quote

#### Summary
[Dimension conclusion]

## Cross-Validation & Contradictions

### High-Credibility Information (multi-source verified)
- [Info 1]: from [Source A](URL), [Source B](URL), [Source C](URL)

### Single-Source Information (needs verification)
- [Info X]: only from [Source](URL)

### Contradictory Information
| View A | Source | View B | Source | Analysis |
|--------|--------|--------|--------|----------|

## Conclusions & Recommendations

### Overall Assessment
### Recommendations
### Items Needing Further Verification

## Source Summary
[All cited URLs]
```

## Anti-Patterns & Solutions

| Anti-Pattern | Solution |
|--------------|----------|
| Only positive results | Explicitly search negative terms: "criticism", "scam", "problems" |
| Single source | Require sub-agents to find multiple independent sources |
| Over-summarized, lost details | Require original quotes, not just summaries |
| Clean dimension split, no overlap | Design dimensions with intentionally fuzzy boundaries |
| Intermediate files piling up | Only save ONE final report |

## Key Reminders

1. **Never save intermediate files** - only the final report
2. **Always require URLs** - no anonymous citations
3. **Overlap dimensions intentionally** - this enables cross-validation
4. **Search negative terms** - balance the positive bias in search results
5. **Preserve original quotes** - summaries lose nuance
6. **Report contradictions** - they're valuable, not problems to hide
