#!/bin/bash
# Create Pull Request for SAAT Repository

cd "$(dirname "$0")"

echo "Creating Pull Request for SAAT..."
echo "Branch: claude/fix-three-m-files-011CUf9vnrJ6Acp3wuQWYELY"
echo "Target: main"
echo ""

gh pr create \
  --base main \
  --head claude/fix-three-m-files-011CUf9vnrJ6Acp3wuQWYELY \
  --title "Add Structurizr JSON integration and complete documentation" \
  --body-file PR_DESCRIPTION.md

echo ""
echo "PR created successfully!"
