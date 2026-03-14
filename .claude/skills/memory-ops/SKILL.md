---
name: memory-ops
description: |
  Operational interface for the three-layer memory system. Handles capturing insights,
  extracting session knowledge, ingesting external content, distilling curated knowledge,
  reflecting on long-term insights, and navigating across memory layers.

  Use when user wants to:
  - Save insights from current session or conversation
  - Extract and preserve a session's key learnings
  - Digest meeting transcripts or research reports into memory
  - Review weekly/monthly knowledge accumulation
  - Search or navigate existing memory
  - Review pending Layer 3 reflection proposals

  Triggers: "save this session", "extract memory", "review this week", "ingest this meeting", "ingest this survey", "update memory", "search memory", "reflect", "what do I know about", "remember this", "digest this"
---

# Memory Ops Skill

Operational interface for the three-layer memory system. All capture is user-initiated (pull-based). Automation only applies to distillation of already-captured content.

## Memory Architecture Quick Reference

```
memory/
  index.md          ← Always loaded via CLAUDE.md. Entry point for progressive disclosure.
  raw/              ← Layer 1: Immutable session extractions (user-initiated)
  curated/          ← Layer 2: Distilled reusable knowledge
    topics/         ←   Persistent topic files
    YYYY-WNN.md     ←   Weekly digests
  insights/         ← Layer 3: Long-term stable insights (user-confirmed only)
    .taxonomy.md    ←   Controlled vocabulary + rules
    .pending-reflection.md  ← Monthly reflection proposals
```

## Actions

### 1. `capture` — Real-time refined capture

**Trigger**: "记住这个" / "remember this" / AI identifies high-value insight during session

**Steps**:
1. Identify the insight to capture — must be "painful to rediscover" level
2. Read `memory/curated/topics/` to find the best-fit existing topic file
3. If no good fit, check `memory/insights/.taxonomy.md` for category guidance before creating a new topic file
4. Append entry to the topic file:

```markdown
### YYYY-MM-DD: [One-line summary]
[1-3 sentences explaining the insight and why it matters]
- Source: [current session ID or context]
```

5. Confirm to user what was captured and where

**Rules**:
- Only refined, actionable insights — not raw observations
- Append to existing files over creating new ones
- Never touch `memory/insights/` (Layer 3) without explicit user approval

---

### 2. `extract` — Save current session

**Trigger**: "保存这个session" / "save this session" / "记住这次对话"

**Steps**:
1. Read the current session using `session_read` with `include_todos=true`
2. Apply the extraction prompt to generate structured output:

```
You are a knowledge extraction engine. Given an AI session transcript, extract:

1. DECISIONS: What was decided and why (technical choices, design decisions, trade-offs)
2. LEARNINGS: New knowledge discovered (about codebase, tools, user preferences, domain)
3. PATTERNS: Reusable approaches that worked well (or failed and should be avoided)
4. OPEN QUESTIONS: Unresolved issues flagged for future sessions
5. USER CONTEXT: Any personal context the user shared (preferences, goals, constraints)

For each item, include:
- A one-line summary
- Context: 1-3 sentences quoting or closely paraphrasing the relevant conversation.
  This MUST make the item independently understandable even if the original session is deleted.
- Source: session_id + approximate message range (best-effort)

Only record what would be "painful to rediscover".
Skip: routine file edits, mechanical tool calls, standard greetings.
```

3. Read `memory/raw/YYYY-MM-DD.md` (today's date) if it exists
4. Append the extraction as a new `## Session:` section
5. If file doesn't exist, create it with `# YYYY-MM-DD` header
6. Confirm to user what was extracted

**Output format** in `memory/raw/YYYY-MM-DD.md`:

```markdown
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

### 3. `ingest-meeting` — Digest meeting transcript

**Trigger**: "消化这个会议" / "ingest this meeting" / "digest this meeting"

**Steps**:
1. If user specifies a file, read it. Otherwise, list recent files in `contexts/conversations/` and ask which one.
2. Read the meeting transcript (already structured with summary + topic sections)
3. Apply the meeting extraction prompt:

```
Given a meeting transcript, extract reusable knowledge (ignore meeting-specific details and action items):

1. DECISIONS: What was decided and why (technical choices, direction, trade-offs)
2. INSIGHTS: New understanding of a domain (not obvious from common knowledge)
3. PATTERNS: Reusable team/org patterns (collaboration, decision processes, communication strategies)
4. USER CONTEXT: Persistent info about user's role, relationships, project background

Do NOT extract: specific action items, meeting scheduling, temporary status updates.
Include a Context field for each item to make it self-contained.
```

4. For each extracted item, find or create the appropriate topic file in `memory/curated/topics/`
5. Append entries with `Source: contexts/conversations/[filename]`
6. Confirm to user what was ingested

---

### 4. `ingest-survey` — Digest research report

**Trigger**: "消化这个调研" / "ingest this survey" / "digest this research"

**Steps**:
1. If user specifies a file, read it. Otherwise, list recent files in `contexts/survey_sessions/` and ask which one.
2. Read the survey report (structured with conclusions + analysis + cross-validation)
3. Apply the survey extraction prompt:

```
Given a research report, extract long-term reusable knowledge (ignore time-sensitive specific data):

1. CONCLUSIONS: Core conclusions verified by multiple sources
2. FRAMEWORKS: Reusable analysis frameworks or decision models
3. TRADE-OFFS: Key trade-off analyses (long-term valid)
4. GOTCHAS: Traps or counter-intuitive findings

For contradictory info: preserve both views, mark [provisional].
Include original URL provenance for each item.
```

4. For each extracted item, find or create the appropriate topic file in `memory/curated/topics/`
5. Append entries with `Source: contexts/survey_sessions/[filename]`, preserving URL provenance
6. Confirm to user what was ingested

---

### 5. `distill` — Weekly distillation

**Trigger**: "回顾这周" / "review this week" / also triggered by `jobs/memory-distill/`

**Steps**:
1. Collect this week's input: all files in `memory/raw/` from the past 7 days
2. Read existing `memory/curated/topics/` to check for duplicates (from mechanism A or prior ingestion)
3. Apply two-phase processing (mem0 pattern):
   - **Phase 1**: Extract atomic facts/insights from raw logs
   - **Phase 2**: Compare against existing curated knowledge → ADD (new) / UPDATE (more detailed) / SKIP (already known)
4. Write weekly digest to `memory/curated/YYYY-WNN.md`:

```markdown
# Week [N], [YYYY] ([date range])

_Distilled: [timestamp] | Sources: raw/[files] | Items extracted: [N] | Items promoted: [N]_

## Promoted to Topics
- → topics/[file]: [description] (from raw/[source])

## Key Decisions This Week
- [decision summaries]

## Patterns Observed
- [patterns]

## Open Questions Carried Forward
- [questions]
```

5. Append new entries to relevant topic files
6. **Update `memory/index.md`** — regenerate "Recent Working Memory" section from this week's digest + recent topic updates

---

### 6. `reflect` — Monthly reflection

**Trigger**: "反思一下" / "reflect" / also triggered by `jobs/memory-reflect/`

**Steps**:
1. Read past month's weekly digests (`memory/curated/YYYY-WNN.md`)
2. Read all topic files (`memory/curated/topics/`)
3. Read existing Layer 3 insight files (`memory/insights/`)
4. Read taxonomy (`memory/insights/.taxonomy.md`)
5. Identify:
   - Recurring themes that suggest a new stable insight → NEW proposal
   - Existing insights that need updating based on new evidence → UPDATE proposal
   - Insights that may no longer be accurate → REVIEW proposal
6. Write proposals to `memory/insights/.pending-reflection.md`:

```markdown
# Pending Reflection — [YYYY-MM]

_Generated: [date] | Source: curated/[week range]_

## Proposal 1: NEW insight
**Target**: memory/insights/[file]
**Action**: ADD entry
**Content**:
> [proposed insight text]
**Emerged from**: [curated sources with dates]

## Proposal 2: UPDATE existing insight
**Target**: memory/insights/[file] → "[entry title]"
**Action**: UPDATE
**Current**: [current text]
**Proposed**: [proposed new text]
**Emerged from**: [curated sources]
```

7. **STOP. Do not apply changes.** Inform user: "Reflection proposals generated. Please review `memory/insights/.pending-reflection.md`"
8. When user reviews (approve/reject/modify each proposal), apply approved changes to Layer 3 files
9. Clear `.pending-reflection.md` after all proposals are processed

---

### 7. `navigate` — Cross-layer search and traceability

**Trigger**: "what do I know about X" / "搜索记忆" / "我之前关于X说了什么" / "search memory"

**Steps**:
1. Read `memory/index.md` to locate relevant topics/insights
2. Search Layer 3 (`memory/insights/`) for matching entries
3. Search Layer 2 (`memory/curated/topics/`) for matching entries
4. If more detail needed, search Layer 1 (`memory/raw/`) via grep
5. If raw log references a session, can use `session_read` to access original transcript
6. Present findings to user, organized by layer:

```
## From Long-Term Insights (Layer 3)
- [insight entry] (memory/insights/[file])

## From Curated Knowledge (Layer 2)
- [topic entry] (memory/curated/topics/[file])

## From Raw Logs (Layer 1)
- [raw extraction] (memory/raw/[date].md)
```

---

## What This Skill Does NOT Do

- **Does not modify CLAUDE.md** — that's the system rules layer
- **Does not autonomously modify Layer 3** — must go through reflect → user approval
- **Does not do audio transcription** — that's handled by external tools
- **Does not do deep research** — that's the `deep-research` skill
- **Does not manage job scheduling** — that's the `jobs/` framework
- **Does not auto-scan sessions** — all capture is user-initiated
