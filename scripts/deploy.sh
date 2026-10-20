#!/usr/bin/env bash

set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${PIDOG_TARGET:-buck@buck.local}"
remote_dir="${PIDOG_REMOTE_DIR:-pidog-coding}"

echo "Deploying $project_dir to $target:~/$remote_dir"
rsync -az \
  --exclude .git/ \
  --exclude .venv/ \
  --exclude __pycache__/ \
  "$project_dir/" "$target:$remote_dir/"

echo "Deployment complete."
