# launchd Operations

## Installation

```bash
# ⚠️ Edit the paths in the plist first, replacing with your actual project path!
cp com.user.job-runner.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.job-runner.plist
```

## Operations

```bash
launchctl start com.user.job-runner              # Trigger immediately
launchctl stop  com.user.job-runner              # Stop current run
launchctl unload ~/Library/LaunchAgents/com.user.job-runner.plist  # Unload (must unload before editing)
launchctl load   ~/Library/LaunchAgents/com.user.job-runner.plist  # Reload
launchctl list | grep job-runner                   # Check if loaded
```

## Debugging

```bash
tail -f /YOUR/PROJECT/PATH/jobs/logs/runner.log
tail -f /YOUR/PROJECT/PATH/jobs/logs/runner-error.log
```

## Important Notes

You must `unload` before editing the plist, then `load` after making changes. Editing the file directly without unloading will not take effect.
