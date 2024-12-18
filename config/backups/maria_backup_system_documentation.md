# Ivanka Backup System

## Overview
Ivanka uses a comprehensive three-layer backup system:

1. **Full System Backups** (`/home/ernsttulle/backups/maria/`)
- Daily snapshots using master_backup.sh 
- Full .tar.gz of entire bot
- Retains last 5 backups
- Part of multi-bot backup system

2. **GitHub Backups** (`/home/ernsttulle/maria/backups/github/`)
- Daily code version control
- Runs at 3:00 UTC
- Pushes to eastern-brown/maria repository
- Tracks all code changes

3. **Claude Session Backups** (`/home/ernsttulle/maria/backups/claude_sessions/`)
- Snapshot system for AI work
- On-demand backups before AI changes
- Quick recovery from unwanted changes
- Project-specific snapshots

## Directory Structure
```
/home/ernsttulle/maria/
└── backups/
    ├── github/
    │   ├── maria_backup.sh      # GitHub backup script
    │   └── github_backup_log.txt # GitHub operation logs
    ├── claude_sessions/
    │   ├── claude_tracker.py    # Core session tracking
    │   ├── claude_session.py    # CLI interface
    │   └── sessions/           # Session snapshots
    └── local/
        └── backup_log.txt      # Local backup logs
```

## System Components

### 1. Full System Backups
Location: `/home/ernsttulle/backups/maria/`
Script: `/home/ernsttulle/master_backup.sh`
```bash
# Format of backup files:
maria_backup_YYYYMMDD_HHMMSS.tar.gz

# Schedule:
- Daily at 15:00 UTC
- Keeps last 5 backups
- Automated via PythonAnywhere tasks
```

### 2. GitHub Backup System
Location: `/home/ernsttulle/maria/backups/github/`
```bash
# Start manual GitHub backup:
cd /home/ernsttulle/maria
./backups/github/maria_backup.sh

# Schedule:
- Daily at 03:00 UTC
- Automated via PythonAnywhere tasks

# Monitoring:
tail -f backups/github/github_backup_log.txt
```

### 3. Claude Session System
Location: `/home/ernsttulle/maria/backups/claude_sessions/`
```bash
# Start new session:
python3 backups/claude_sessions/claude_session.py start "Description"

# List sessions:
python3 backups/claude_sessions/claude_session.py list

# Restore session:
python3 backups/claude_sessions/claude_session.py restore session_ID
```

## Usage Guidelines

### Daily Operations
1. System backup runs automatically at 15:00 UTC
2. GitHub backup runs automatically at 03:00 UTC
3. Create Claude session before AI work:
   ```bash
   cd /home/ernsttulle/maria
   python3 backups/claude_sessions/claude_session.py start "Task description"
   ```

### Recovery Procedures

#### Recover from Bad AI Changes
```bash
# List available sessions
python3 backups/claude_sessions/claude_session.py list

# Restore specific session
python3 backups/claude_sessions/claude_session.py restore session_20241214_050321
```

#### Recover from GitHub
```bash
# View history
git log

# Restore specific commit
git checkout <commit-hash>
```

#### Full System Recovery
```bash
cd /home/ernsttulle
tar -xzf /home/ernsttulle/backups/maria/maria_backup_TIMESTAMP.tar.gz
```

## Maintenance

### Daily Checks
- Check GitHub backup logs:
  ```bash
  tail backups/github/github_backup_log.txt
  ```
- Verify system backup:
  ```bash
  ls -l /home/ernsttulle/backups/maria/
  ```

### Weekly Tasks
1. Clean old Claude sessions
2. Review GitHub backup logs
3. Verify backup integrity

### Monthly Tasks
1. GitHub token review
2. Backup script updates
3. Space usage audit

## Troubleshooting

### GitHub Backup Issues
1. Check token validity
2. Verify remote configuration:
   ```bash
   git remote -v
   ```
3. Review logs:
   ```bash
   cat backups/github/github_backup_log.txt
   ```

### Claude Session Issues
1. Check session directory permissions
2. Verify session metadata:
   ```bash
   cat backups/claude_sessions/sessions/sessions.json
   ```
3. Clean corrupted sessions if needed

### System Backup Issues
1. Check disk space:
   ```bash
   df -h
   ```
2. Verify master_backup.sh permissions
3. Review system logs

## PythonAnywhere Task Configuration

### GitHub Backup Task
```
Command: /home/ernsttulle/maria/backups/github/maria_backup.sh
Time: 03:00 UTC
Frequency: Daily
```

### System Backup Task
```
Command: /home/ernsttulle/master_backup.sh
Time: 15:00 UTC
Frequency: Daily
```