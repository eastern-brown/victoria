#!/bin/bash
# /home/ernsttulle/peggy/config/backups/github/peggy_backup.sh

# Configuration
BOT_DIR="/home/ernsttulle/peggy"
LOG_FILE="$BOT_DIR/config/backups/github/github_backup_log.txt"
DATE=$(date '+%Y-%m-%d_%H-%M-%S')

# Ensure we're in the right directory
cd "$BOT_DIR" || {
    echo "ERROR: Could not change to bot directory" >> "$LOG_FILE"
    exit 1
}

# Log start of backup
echo "=== GitHub backup started at $(date) ===" >> "$LOG_FILE"

# Git backup
echo "Checking for changes to commit..." >> "$LOG_FILE"

# Check if there are changes to commit
if git status --porcelain | grep -q '^'; then
    git add . >> "$LOG_FILE" 2>&1
    git commit -m "Daily GitHub backup: $DATE" >> "$LOG_FILE" 2>&1
    echo "Pushing changes to GitHub..." >> "$LOG_FILE"
    git push origin master >> "$LOG_FILE" 2>&1
    echo "Changes committed and pushed successfully" >> "$LOG_FILE"
else
    echo "No changes to commit" >> "$LOG_FILE"
fi

echo "=== GitHub backup completed at $(date) ===" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"