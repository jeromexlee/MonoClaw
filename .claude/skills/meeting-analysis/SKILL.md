---
name: meeting-analysis
description: |
  Seven-dimension deep analysis framework for executive meetings, product reviews, funding negotiations,
  and roadmap evaluations. Specializes in organizational behavior, power dynamics, and strategic communication analysis.

  Use when user wants to:
  - Analyze a meeting transcript or recording notes (product review, roadmap review, funding discussion)
  - Understand power dynamics, hidden negotiations, or political subtext in a meeting
  - Extract strategic communication patterns from leadership conversations
  - Prepare for or debrief after high-stakes executive meetings
  - Understand what a decision-maker really cares about from their questioning patterns

  Triggers: "meeting analysis", "analyze this meeting", "debrief this meeting", "executive meeting", "funding review", "roadmap review"
---

# Executive Meeting Deep Analysis

A structured framework for analyzing high-stakes meetings — product reviews, funding negotiations, roadmap evaluations, and leadership conversations. Extracts organizational politics, power dynamics, and strategic communication patterns that surface-level summaries miss.

## When to Use

This skill is designed for meetings where **organizational power dynamics matter**:
- Product reviews with senior leadership / executives
- Funding or resource allocation negotiations
- Cross-team roadmap evaluations
- Any meeting where "what was said" differs from "what was meant"

It is NOT for: routine standups, technical design reviews, or meetings where the content is purely operational.

## Workflow

### Step 1: Gather the Input

Ask the user for the meeting transcript or notes. Accept any format:
- Raw transcript (copy-paste, `.txt`, `.md`)
- Meeting notes or summary
- Audio transcription output
- The user's recollection (less ideal, but workable)

If the user provides a file path, read it. If they paste inline, use that directly.

**Clarify scope** before starting:

```
Got it. Before I analyze, let me confirm:
1. What's the meeting context? (product review / funding negotiation / roadmap discussion / other)
2. What's your role in the meeting? (presenter / participant / observer)
3. Any specific dimension you want to deep-dive? (power structure / language artistry / risk watch / all of them)
```

If the user says "all" or doesn't specify, run all 7 dimensions.

### Step 2: Run the Seven-Dimension Analysis

Execute the analysis framework below. For each dimension:
- **Quote the original text** as evidence (use `>` blockquotes)
- **Separate facts from inferences** — label clearly which is which
- Be direct and unsparing in political analysis — the user wants insight, not diplomacy

---

## The Seven Dimensions

### 1. Power Structure & Role Identification

Identify the **decision-maker** (usually the person who asks the most questions, can interrupt others, and sets the framing), **presenters/reporters**, and **stakeholders**.

| Person | Role | Organizational Position | Agenda in This Meeting |
|--------|------|------------------------|----------------------|

Key signals:
- Who sets the discussion framework (framing)?
- Who asks follow-up questions vs. who answers?
- Who stays silent — and is the silence strategic?
- Who can interrupt whom without social cost?

### 2. Decision-Maker's Attention Hierarchy

Analyze the decision-maker's questioning patterns:

- **Strategic clarity**: Testing direction, boundaries, ownership?
- **GTM viability**: Pushing on "for whom, how to measure, which customer segment first?"
- **Irreversibility concerns**: Expressing directional worry vs. execution worry
- **Authenticity testing**: Probing whether the team is telling the truth

For each concern, **quote the original text** and classify whether it's strategic-level or execution-level.

### 3. Presenter's Expectation Management Strategy

| Strategy | Original Quote | True Intent |
|----------|---------------|-------------|

Pay special attention to:
- How the presenter defines the discussion boundary
- Whether they volunteer negative information (trust-building) or wait to be asked
- Resource asks: aggressive vs. deliberately restrained

### 4. Strategic Bottlenecks & Dependency Chain

| Bottleneck | Owner | Chain Impact | Self-Controlled? | Severity |
|-----------|-------|-------------|------------------|----------|

Distinguish self-controlled risks from external dependency risks.

### 5. Hidden Negotiation & Control Rights

Identify invisible power negotiations:
- **Direction-setting rights**: Who defines "what success looks like"?
- **Resource allocation rights**: Who controls headcount, budget, priorities?
- **Execution pace control**: Who determines the timeline?

Analyze: **Who won what?** What was the equilibrium reached?

### 6. Language Artistry & Diplomatic Phrasing

| Original Statement | True Meaning | Technique Used |
|-------------------|-------------|----------------|

Common patterns:
- **Euphemistic substitution**: "sequencing" instead of "deprioritizing"
- **Analogy/metaphor rationalization**: Using stories to justify trade-offs
- **Counter-intuitive trust plays**: Proactively refusing resources to increase credibility
- **Process deflection**: Converting challenges into "let's take that offline"

### 7. Follow-Up Risks & Watch Items

| Item | Type | Risk if Unaddressed |
|------|------|-------------------|

Analyze:
- Which topics were intentionally deferred? Strategic or time-constrained?
- Which commitments carry real consequences if missed?
- Which bets carry more political risk than execution risk?

---

## Output Format

```
# [Meeting Name/Type] Deep Analysis

## Executive Summary
[2-3 sentences: who won, what was decided, what was left unsaid]

## 1. Power Structure & Roles
## 2. Decision-Maker's Attention Hierarchy
## 3. Presenter's Expectation Management
## 4. Strategic Bottlenecks & Dependencies
## 5. Hidden Negotiations & Control Rights
## 6. Language Artistry
## 7. Follow-Up Risks & Watch Items

## Key Takeaways for [User's Role]
[Personalized recommendations based on the user's role in the meeting]
```

## Style Guidelines

- **Language**: Match the user's language. Mixed languages are fine.
- **Tone**: Direct, incisive. Do not shy away from sensitive organizational politics analysis.
- **Evidence**: Every claim must reference the original text.
- **Fact vs. inference**: Always label which is observed fact vs. inference.
- **Formatting**: Use tables, hierarchies, and blockquotes liberally for readability.
