# Skills & Jobs Reference

## Skills

Six pluggable capabilities included out of the box. Each is a `.claude/skills/<name>/SKILL.md` file.

| Skill | What It Does |
|-------|-------------|
| `memory-ops` | Full memory lifecycle: capture insights, extract sessions, ingest meetings/research, weekly distillation, monthly reflection, cross-layer search with provenance |
| `deep-research` | Launches 3-5 parallel sub-agents with intentionally overlapping dimensions. Cross-validates findings, flags contradictions, requires URL citations |
| `meeting-analysis` | Seven-dimension framework: power structure, decision-maker attention, presenter strategy, bottleneck chains, hidden negotiations, diplomatic language, follow-up risks |
| `doc-coauthoring` | Three-stage workflow: context gathering → section-by-section brainstorming/curation/drafting → reader testing with a fresh AI instance |
| `semantic-search` | Embedding-based search across the knowledge base. Pre-filters large document sets before AI reads them. Requires OpenAI API key |

### Add a Skill

Create a new directory under `.claude/skills/` with a `SKILL.md` file:

```
.claude/skills/your-skill/SKILL.md
```

The agent auto-discovers skills from this directory.

---

## Jobs

Lightweight automation via `jobs/runner.py`, scheduled with macOS launchd.

| Job | Schedule | What It Does |
|-----|----------|-------------|
| `hello-world` | Daily 09:00 | Example job to verify runner works |
| `memory-distill` | Sundays 20:00 | Weekly L1→L2 distillation |
| `memory-reflect` | Sundays 20:00 | Monthly L2→L3 reflection proposals |

Two job types:
- **script** — runs a Python file
- **prompt** — sends a prompt to your AI agent CLI (supports opencode, claude, codex backends)

### Add a Job

```yaml
# jobs/your-job/job.yaml
name: your-job
type: script
enabled: true
script: main.py
schedule: "weekdays 09:00"
timeout: 300
```

### Set Up Scheduling

```bash
python -m venv .venv
.venv/bin/pip install pyyaml

# Edit paths in the plist first
vim jobs/launchd/com.user.job-runner.plist
cp jobs/launchd/com.user.job-runner.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.job-runner.plist
```

Linux users: adapt to cron or systemd.

---

## Customization

### Add Memory Categories

Edit `memory/insights/.taxonomy.md`. Three rules:
1. Single primary category per insight
2. Ownership determines categorization
3. Cross-cutting concepts become topics, not categories
