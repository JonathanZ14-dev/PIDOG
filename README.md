# PIDOG

Custom code and notes for a [SunFounder PiDog](https://docs.sunfounder.com/projects/pidog/en/latest/) — a Raspberry Pi robot dog with 12 servos, camera, ultrasonic sensing, touch, IMU, and RGB lighting.

This repository is for project scripts and experiments. Official kit examples and libraries live in SunFounder's docs and [pidog](https://github.com/sunfounder/pidog) repo.

## Hardware

- Raspberry Pi (3B+/4/5 or Zero 2W; use PiDog V2 for Pi 5)
- SunFounder PiDog kit (Robot HAT, servos, camera, sensors)
- Raspberry Pi is not included with the kit

## Setup

On the Pi, install the official libraries first:

```bash
# Robot HAT
git clone -b 2.5.x https://github.com/sunfounder/robot-hat.git --depth 1
cd robot-hat && sudo python3 install.py

# Vilib (camera / vision)
git clone https://github.com/sunfounder/vilib.git
cd vilib && sudo python3 install.py

# PiDog
git clone https://github.com/sunfounder/pidog.git --depth 1
cd pidog && sudo pip3 install . --break-system-packages
```

Calibrate servos before running motion code. For V2, press the Robot HAT **ZERO** button during assembly, then run `0_calibration.py` from the official examples.

## This repo

Clone onto the Pi (or pull into this workspace on your computer):

```bash
git clone https://github.com/JonathanZ14-dev/PIDOG.git
cd PIDOG
```

Add Python scripts here as you build behaviors (walk, sit, follow, camera, voice, and so on).

## Resources

- [PiDog documentation](https://docs.sunfounder.com/projects/pidog/en/latest/)
- [Official pidog library](https://github.com/sunfounder/pidog)
