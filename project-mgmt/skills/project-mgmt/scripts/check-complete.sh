#!/bin/bash
# Verify all phases complete before stopping

PROJECT_DIR=".project"
LATEST=$(ls -td "$PROJECT_DIR"/*/ 2>/dev/null | head -1)

if [ -n "$LATEST" ] && [ -f "$LATEST/plan.md" ]; then
  INCOMPLETE=$(grep -c "\- \[ \]" "$LATEST/plan.md")
  if [ "$INCOMPLETE" -gt 0 ]; then
    echo "$INCOMPLETE unchecked items remain"
    echo "Run /project-mgmt sync to save progress before stopping"
  fi
fi

exit 0
