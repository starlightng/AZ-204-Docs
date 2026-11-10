#!/usr/bin/env bash
set -euo pipefail          # stop on errors, unset variables, and failed pipes

SRC="$HOME/projects"       # what to back up
DEST="$HOME/backups"       # where to put it
KEEP_DAYS=14               # delete backups older than this

STAMP=$(date +%Y-%m-%d_%H%M%S)
ARCHIVE="$DEST/backup_$STAMP.tar.gz"
LOG="$DEST/backup.log"

mkdir -p "$DEST"
log() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }

# Check the source exists before doing anything
[ -d "$SRC" ] || { log "ERROR: $SRC not found"; exit 1; }

log "Starting backup of $SRC"
if tar -czf "$ARCHIVE" -C "$(dirname "$SRC")" "$(basename "$SRC")"; then
    log "OK: created $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"
else
    log "ERROR: tar failed"
    rm -f "$ARCHIVE"       # don't keep a broken archive
    exit 1
fi

# Retention: remove old backups
find "$DEST" -name 'backup_*.tar.gz' -mtime +"$KEEP_DAYS" -delete
log "Cleanup done (kept last $KEEP_DAYS days)"
