#!/usr/bin/env bash

set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This script must run on the Raspberry Pi." >&2
  exit 1
fi

if [[ "$(getconf LONG_BIT)" != "64" ]]; then
  cat >&2 <<'EOF'
PiDog's current voice dependencies require 64-bit Raspberry Pi OS.
Install Raspberry Pi OS 64-bit, then run this script again.
EOF
  exit 1
fi

clone_or_update() {
  local url="$1"
  local destination="$2"
  shift 2

  if [[ -d "$destination/.git" ]]; then
    echo "Updating $destination"
    git -C "$destination" pull --ff-only
  elif [[ -e "$destination" ]]; then
    echo "$destination exists but is not a Git checkout; leaving it untouched." >&2
    exit 1
  else
    git clone "$@" "$url" "$destination"
  fi
}

echo "Installing Raspberry Pi system prerequisites"
sudo apt-get update
sudo apt-get install -y git python3-pip python3-setuptools python3-smbus

clone_or_update \
  https://github.com/sunfounder/robot-hat.git \
  "$HOME/robot-hat" \
  --branch 2.5.x --depth 1

clone_or_update \
  https://github.com/sunfounder/vilib.git \
  "$HOME/vilib" \
  --depth 1

clone_or_update \
  https://github.com/sunfounder/pidog.git \
  "$HOME/pidog" \
  --depth 1

echo "Installing Robot HAT"
(
  cd "$HOME/robot-hat"
  sudo python3 install.py
)

echo "Installing Vilib"
(
  cd "$HOME/vilib"
  sudo python3 install.py
)

echo "Installing PiDog"
sudo python3 -m pip install "$HOME/pidog" --break-system-packages

echo "Verifying Python modules"
python3 - <<'PY'
import pidog
import robot_hat

print(f"pidog:     {pidog.__file__}")
print(f"robot_hat: {robot_hat.__file__}")
print("Core PiDog installation is ready.")
PY

cat <<'EOF'

Core setup completed without moving any servos.

Next:
  1. Calibrate before running motion code:
       cd ~/pidog/examples && sudo python3 0_calibration.py
  2. Install I2S audio separately (it is interactive and may reboot the Pi):
       bash ~/pidog-coding/scripts/setup_audio.sh
EOF
