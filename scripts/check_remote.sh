#!/usr/bin/env bash

set -euo pipefail

target="${PIDOG_TARGET:-buck@buck.local}"
remote_dir="${PIDOG_REMOTE_DIR:-pidog-coding}"

ssh "$target" "python3 ~/$remote_dir/src/check_pidog.py"
