#!/usr/bin/env bash

set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This script must run on the Raspberry Pi." >&2
  exit 1
fi

CONFIG="/boot/firmware/config.txt"
if [[ ! -f "$CONFIG" ]]; then
  CONFIG="/boot/config.txt"
fi

OVERLAY="googlevoicehat-soundcard"
ASOUND_CONF="/etc/asound.conf"

echo "Configuring Robot HAT I2S audio (googlevoicehat) as the ALSA default."

if ! grep -q "^dtoverlay=${OVERLAY}" "$CONFIG"; then
  echo "Adding dtoverlay=${OVERLAY} to ${CONFIG}"
  echo "dtoverlay=${OVERLAY}" | sudo tee -a "$CONFIG" >/dev/null
fi

sudo dtoverlay "$OVERLAY" 2>/dev/null || true

sudo tee "$ASOUND_CONF" >/dev/null <<'EOF'
pcm.robothat {
    type asym
    playback.pcm {
        type plug
        slave.pcm "speaker"
    }
    capture.pcm {
        type plug
        slave.pcm "mic"
    }
}

pcm.speaker_hw {
    type hw
    card sndrpigooglevoi
    device 0
}

pcm.dmixer {
    type dmix
    ipc_key 1024
    ipc_perm 0666
    slave {
        pcm "speaker_hw"
        period_time 0
        period_size 1024
        buffer_size 8192
        rate 44100
        channels 2
    }
}

ctl.dmixer {
    type hw
    card sndrpigooglevoi
}

pcm.speaker {
    type softvol
    slave {
        pcm "dmixer"
    }
    control {
        name "robot-hat speaker Playback Volume"
        card sndrpigooglevoi
    }
    min_dB -51.0
    max_dB 0.0
}

pcm.mic_hw {
    type hw
    card sndrpigooglevoi
    device 0
}

pcm.mic {
    type softvol
    slave {
        pcm "mic_hw"
    }
    control {
        name "robot-hat mic Capture Volume"
        card sndrpigooglevoi
    }
    min_dB -26.0
    max_dB 25.0
}

ctl.robothat {
    type hw
    card sndrpigooglevoi
}

pcm.!default robothat
ctl.!default robothat
EOF

echo "Wrote $ASOUND_CONF"

if ! aplay -l | grep -q sndrpigooglevoi; then
  echo "The googlevoicehat sound card is not visible yet." >&2
  echo "Reboot the Pi, then run this script again." >&2
  exit 1
fi

sudo python3 - <<'PY'
from robot_hat import Music

Music()
print("Music() works as root.")
PY

echo "Audio default is now the Robot HAT speaker."
echo "Re-run examples with: sudo python3 ~/pidog/examples/1_wake_up.py"
