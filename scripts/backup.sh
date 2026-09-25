#!/usr/bin/env bash
set -euo pipefail
stamp=$(date +%Y%m%d-%H%M%S)
mkdir -p "backups/$stamp"
# Preserve tracked source without runtime databases or virtual environments.
git archive --format=tar HEAD | tar -x -C "backups/$stamp"
echo "Created backups/$stamp"
