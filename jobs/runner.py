#!/usr/bin/env python3
"""
Generic job runner for personal-assistant.

Usage:
    python runner.py jobs/linkedin-search    # Run a specific job
    python runner.py --all-due               # Run all due jobs
    python runner.py --list                  # List all jobs and their status
"""

import json
import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime, time as dtime
import yaml

JOBS_DIR = Path(__file__).parent
LOG_DIR = JOBS_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "runner.log"),
    ],
)
log = logging.getLogger("job-runner")


def _load_runner_config() -> dict:
    config_path = JOBS_DIR / "config.yaml"
    if not config_path.exists():
        return {}
    try:
        return yaml.safe_load(config_path.read_text()) or {}
    except yaml.YAMLError as e:
        log.warning(f"Failed to parse {config_path}: {e}")
        return {}


RUNNER_CONFIG = _load_runner_config()


def load_job_config(job_dir: Path) -> dict | None:
    """Load and validate job.yaml from a job directory."""
    job_yaml = job_dir / "job.yaml"
    if not job_yaml.exists():
        return None
    try:
        return yaml.safe_load(job_yaml.read_text())
    except yaml.YAMLError as e:
        log.error(f"Failed to parse {job_yaml}: {e}")
        return None


def run_job(job_dir: Path) -> bool:
    """Execute a single job. Returns True on success."""
    job_dir = job_dir.resolve()
    config = load_job_config(job_dir)
    if config is None:
        log.error(f"No valid job.yaml in {job_dir}")
        return False

    if not config.get("enabled", True):
        log.info(f"Skipping disabled job: {config['name']}")
        return True

    run_id = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    run_dir = job_dir / "runs" / run_id
    run_dir.mkdir(parents=True)

    meta = {
        "job": config["name"],
        "run_id": run_id,
        "started_at": datetime.now().isoformat(),
        "config_snapshot": config,
        "status": "running",
    }

    log.info(f"=== Starting job: {config['name']} (run_id: {run_id}) ===")

    try:
        if config["type"] == "script":
            output = _run_script_job(config, job_dir, run_dir)
        elif config["type"] == "prompt":
            output, session_id = _run_prompt_job(config, run_dir)
            meta["session_id"] = session_id
        else:
            raise ValueError(f"Unknown job type: {config['type']}")

        (run_dir / "output.json").write_text(output)
        meta["status"] = "success"
        log.info(f"Job {config['name']} completed successfully")

    except subprocess.TimeoutExpired:
        meta["status"] = "timeout"
        meta["error"] = f"Job exceeded timeout"
        log.error(f"Job {config['name']} timed out")

    except Exception as e:
        meta["status"] = "failed"
        meta["error"] = str(e)
        log.error(f"Job {config['name']} failed: {e}")

    meta["finished_at"] = datetime.now().isoformat()
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    latest = job_dir / "runs" / "latest"
    if latest.is_symlink() or latest.exists():
        latest.unlink()
    latest.symlink_to(run_id)

    return meta["status"] == "success"


def _run_script_job(config: dict, job_dir: Path, run_dir: Path) -> str:
    """Execute a script-type job. Returns stdout as output."""
    script_path = job_dir / config["script"]
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    timeout = config.get("timeout", 300)

    env = {
        **__import__("os").environ,
        "JOB_CONFIG": json.dumps(config.get("config", {})),
        "JOB_RUN_DIR": str(run_dir),
    }

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(job_dir),
        env=env,
    )

    (run_dir / "stdout.log").write_text(result.stdout)
    (run_dir / "stderr.log").write_text(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(
            f"Script exited with code {result.returncode}.\n"
            f"stderr: {result.stderr[:500]}"
        )

    return result.stdout


def _run_prompt_job(config: dict, run_dir: Path) -> tuple[str, str]:
    """Execute a prompt-type job via configured backend. Returns (output, session_id)."""
    prompt = config["prompt"]

    for f in config.get("context_files", []):
        path = JOBS_DIR.parent / f
        if path.exists():
            prompt += f"\n\n--- {f} ---\n{path.read_text()}"
        else:
            log.warning(f"Context file not found: {path}")

    timeout = config.get("timeout", 600)
    backend = config.get("prompt_backend") or RUNNER_CONFIG.get("prompt_backend", "opencode")

    backends = {
        "opencode": _invoke_opencode,
        "claude": _invoke_claude,
        "codex": _invoke_codex,
    }
    invoke = backends.get(backend)
    if invoke is None:
        raise ValueError(f"Unknown prompt_backend: {backend!r} (options: {', '.join(backends)})")

    log.info(f"  prompt backend: {backend}")
    return invoke(prompt, timeout, run_dir)


def _save_run_logs(result: subprocess.CompletedProcess, run_dir: Path):
    (run_dir / "stdout.log").write_text(result.stdout)
    (run_dir / "stderr.log").write_text(result.stderr)


def _invoke_opencode(prompt: str, timeout: int, run_dir: Path) -> tuple[str, str]:
    result = subprocess.run(
        ["opencode", "run", "--format", "json", prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(JOBS_DIR.parent),
    )
    _save_run_logs(result, run_dir)

    output = ""
    session_id = ""
    for line in result.stdout.splitlines():
        try:
            event = json.loads(line)
            if not session_id:
                session_id = event.get("sessionID", "")
            if event.get("type") == "text":
                output += event.get("part", {}).get("text", "")
        except json.JSONDecodeError:
            continue

    return output or result.stdout, session_id


def _invoke_claude(prompt: str, timeout: int, run_dir: Path) -> tuple[str, str]:
    result = subprocess.run(
        ["claude", "-p", "--output-format", "json", prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(JOBS_DIR.parent),
    )
    _save_run_logs(result, run_dir)

    try:
        data = json.loads(result.stdout)
        return data.get("result", result.stdout), data.get("session_id", "")
    except (json.JSONDecodeError, KeyError):
        return result.stdout, ""


def _invoke_codex(prompt: str, timeout: int, run_dir: Path) -> tuple[str, str]:
    result = subprocess.run(
        ["codex", "exec", "--full-auto", "--json", prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(JOBS_DIR.parent),
    )
    _save_run_logs(result, run_dir)

    output = ""
    session_id = ""
    for line in result.stdout.splitlines():
        try:
            event = json.loads(line)
            if event.get("type") == "thread.started":
                session_id = event.get("thread_id", "")
            elif event.get("type") == "item.completed":
                item = event.get("item", {})
                if item.get("type") == "agent_message":
                    output = item.get("text", "")
        except json.JSONDecodeError:
            continue

    return output or result.stdout, session_id


def _get_last_run_time(job_dir: Path) -> datetime | None:
    """Get the timestamp of the last run from the latest symlink."""
    latest = job_dir / "runs" / "latest"
    if not latest.is_symlink():
        return None
    try:
        run_id = latest.resolve().name
        return datetime.fromisoformat(run_id)
    except (ValueError, OSError):
        return None


def _parse_schedule(schedule: str) -> dict:
    """
    Parse schedule string into components.
    Formats: "weekdays 14:00", "sundays 20:00", "daily 09:00", "hourly"
    """
    parts = schedule.lower().split()
    result = {"days": None, "time": None}

    if "hourly" in parts:
        result["days"] = "daily"
        return result

    day_map = {
        "weekdays": [0, 1, 2, 3, 4],
        "daily": [0, 1, 2, 3, 4, 5, 6],
        "mondays": [0], "tuesdays": [1], "wednesdays": [2],
        "thursdays": [3], "fridays": [4], "saturdays": [5], "sundays": [6],
    }

    for part in parts:
        if part in day_map:
            result["days"] = day_map[part]
        elif ":" in part:
            h, m = part.split(":")
            result["time"] = dtime(int(h), int(m))

    return result


def is_due(config: dict, job_dir: Path) -> bool:
    """Check if a job is due to run based on its schedule."""
    schedule_str = config.get("schedule")
    if not schedule_str:
        return False

    schedule = _parse_schedule(schedule_str)
    now = datetime.now()

    if schedule["days"] is not None and isinstance(schedule["days"], list):
        if now.weekday() not in schedule["days"]:
            return False

    last_run = _get_last_run_time(job_dir)
    if last_run:
        if schedule["days"] == "daily" and schedule.get("time") is None:
            if last_run.hour == now.hour and last_run.date() == now.date():
                return False
        else:
            if last_run.date() == now.date():
                return False

    if schedule["time"]:
        scheduled_minutes = schedule["time"].hour * 60 + schedule["time"].minute
        current_minutes = now.hour * 60 + now.minute
        if current_minutes < scheduled_minutes or current_minutes > scheduled_minutes + 59:
            return False

    return True


def run_all_due():
    """Scan all job directories and run jobs that are due."""
    log.info("=== Checking all jobs ===")
    job_dirs = sorted([
        d for d in JOBS_DIR.iterdir()
        if d.is_dir() and (d / "job.yaml").exists()
    ])

    if not job_dirs:
        log.info("No jobs found")
        return

    for job_dir in job_dirs:
        config = load_job_config(job_dir)
        if config is None:
            continue

        if not config.get("enabled", True):
            log.info(f"  {config['name']}: disabled, skipping")
            continue

        if is_due(config, job_dir):
            log.info(f"  {config['name']}: due, running...")
            run_job(job_dir)
        else:
            log.info(f"  {config['name']}: not due, skipping")


def list_jobs():
    """List all jobs and their status."""
    job_dirs = sorted([
        d for d in JOBS_DIR.iterdir()
        if d.is_dir() and (d / "job.yaml").exists()
    ])

    if not job_dirs:
        print("No jobs found.")
        return

    print(f"{'Name':<25} {'Type':<10} {'Enabled':<10} {'Schedule':<20} {'Last Run':<25} {'Status'}")
    print("-" * 110)

    for job_dir in job_dirs:
        config = load_job_config(job_dir)
        if config is None:
            continue

        last_run = _get_last_run_time(job_dir)
        last_run_str = last_run.strftime("%Y-%m-%d %H:%M") if last_run else "never"

        latest = job_dir / "runs" / "latest"
        status = "-"
        if latest.is_symlink():
            meta_path = latest.resolve() / "meta.json"
            if meta_path.exists():
                meta = json.loads(meta_path.read_text())
                status = meta.get("status", "-")

        print(
            f"{config['name']:<25} "
            f"{config['type']:<10} "
            f"{'yes' if config.get('enabled', True) else 'NO':<10} "
            f"{config.get('schedule', '-'):<20} "
            f"{last_run_str:<25} "
            f"{status}"
        )


if __name__ == "__main__":
    if "--all-due" in sys.argv:
        run_all_due()
    elif "--list" in sys.argv:
        list_jobs()
    elif len(sys.argv) > 1 and sys.argv[1] != "--help":
        job_path = Path(sys.argv[1])
        if not job_path.is_absolute():
            job_path = JOBS_DIR / job_path.name if not job_path.exists() else job_path
        success = run_job(job_path)
        sys.exit(0 if success else 1)
    else:
        print(__doc__)
