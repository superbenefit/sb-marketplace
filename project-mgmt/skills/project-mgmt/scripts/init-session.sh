#!/bin/bash
# Display active project context on session start

PROJECT_DIR=".project"

if [ -d "$PROJECT_DIR" ]; then
  # Find most recent issue directory
  LATEST=$(ls -td "$PROJECT_DIR"/*/ 2>/dev/null | head -1)
  if [ -n "$LATEST" ] && [ -f "$LATEST/plan.md" ]; then
    ISSUE=$(basename "$LATEST")
    PHASE=$(grep -m1 "^\*\*Phase\*\*:" "$LATEST/plan.md" | sed 's/.*: //')
    echo "Active: $ISSUE | Phase: $PHASE"
    echo "Files: plan.md, spec.md, findings.md, progress.md"
  fi
fi

exit 0
