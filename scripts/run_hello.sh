#!/usr/bin/env bash

set -euo pipefail

target="${PIDOG_TARGET:-buck@buck.local}"
remote_dir="${PIDOG_REMOTE_DIR:-pidog-coding}"

cat <<'EOF'
PiDog is about to move. Put it on the floor with clear space around it.
Only continue after completing the official servo calibration.
EOF

read -r -p "Type CALIBRATED to continue: " confirmation
if [[ "$confirmation" != "CALIBRATED" ]]; then
  echo "Cancelled; PiDog did not move."
  exit 1
fi

ssh -t "$target" \
  "sudo python3 ~/$remote_dir/src/hello_pidog.py --i-have-calibrated"
