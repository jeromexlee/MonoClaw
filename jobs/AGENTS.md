# Jobs System

This directory is a general-purpose job automation framework. launchd periodically triggers `runner.py`, which scans all job directories and executes due tasks.

## Installation (From Scratch)

Prerequisites: Python 3.11+ (recommended to manage via asdf, see `.tool-versions` in project root).

```bash
# 1. Create venv and install dependencies
python -m venv .venv
.venv/bin/pip install pyyaml

# 2. Install launchd plist (triggers runner.py --all-due at the top of every hour)
# ⚠️ Edit the paths in the plist first!
cp jobs/launchd/com.user.job-runner.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.job-runner.plist

# 3. Verify
launchctl list | grep job-runner
.venv/bin/python jobs/runner.py --list
```

The plist contains hardcoded absolute paths to `.venv/bin/python`. If you move the project directory or rebuild the venv, you must update the plist accordingly (run `launchctl unload` before editing, then `load` after).

## Starting and Stopping

```bash
# Manually trigger all due jobs once
.venv/bin/python jobs/runner.py --all-due

# Manually run a specific job (regardless of schedule)
.venv/bin/python jobs/runner.py hello-world

# Pause a job: edit job.yaml and set enabled: false
# Resume: change back to true

# Stop the entire launchd scheduler
launchctl unload ~/Library/LaunchAgents/com.user.job-runner.plist

# Re-enable
launchctl load ~/Library/LaunchAgents/com.user.job-runner.plist

# Trigger immediately (don't wait for the next hour)
launchctl start com.user.job-runner
```

For debugging, check logs: `tail -f jobs/logs/runner.log` and `jobs/logs/runner-error.log`.

## Adding a New Job

Create a directory under `jobs/` and add a `job.yaml` file:

```yaml
name: my-job
type: script          # script or prompt
enabled: true
script: main.py       # required when type=script
schedule: "weekdays 14:00"   # see format below
description: "What this job does"
timeout: 300          # seconds, default 300
config:               # arbitrary key-value pairs, passed to script via JOB_CONFIG environment variable
  foo: bar
```

Schedule format: `daily 09:00`, `weekdays 14:00`, `sundays 20:00`, `hourly`. The runner executes hourly and checks which jobs are due.

For type=script, scripts receive configuration via the `JOB_CONFIG` environment variable (JSON string), and stdout is saved as output in `runs/{run_id}/output.json`. For type=prompt, the runner invokes the corresponding CLI (opencode / claude / codex) based on the `prompt_backend` setting in `jobs/config.yaml`.

`jobs/config.yaml` is a per-machine configuration (gitignored), allowing different machines to use different backends. When the file doesn't exist, opencode is used by default. Individual jobs can override the global setting using `prompt_backend: claude` in their job.yaml.

Each run creates a `runs/{run_id}/` directory containing `meta.json` (status, duration, errors) and `output.json`, and updates the `runs/latest` symlink.
