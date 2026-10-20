# PiDog coding workspace

This folder is the safe place for custom PiDog code. The official SunFounder
libraries and examples live on the Raspberry Pi in `~/robot-hat`, `~/vilib`,
and `~/pidog`; this project deploys to `~/pidog-coding` on the Pi.

## Connection

- SSH user: `buck`
- Hostname: `buck.local`
- Default target: `buck@buck.local`

Test the connection from the Mac:

```bash
ssh buck@buck.local
```

The scripts also accept a different target when needed:

```bash
PIDOG_TARGET=buck@192.168.0.151 ./scripts/deploy.sh
```

## First-time setup

Run these commands from this folder on the Mac:

```bash
./scripts/deploy.sh
ssh -t buck@buck.local 'bash ~/pidog-coding/scripts/setup_pi.sh'
./scripts/check_remote.sh
```

`setup_pi.sh` follows SunFounder's current installation sequence for Robot HAT,
Vilib, and PiDog. It requires 64-bit Raspberry Pi OS and does not move servos.

### Calibrate before motion

Do not run custom motion code until calibration is complete. Put PiDog on a flat,
safe platform, have the correct 60-degree or 90-degree calibration ruler ready,
and run:

```bash
ssh -t buck@buck.local
cd ~/pidog/examples
sudo python3 0_calibration.py
```

For PiDog V2, the Robot HAT zero button handles servo zeroing, but the calibration
program is still required. Follow the physical alignment steps in the official
[calibration guide](https://docs.sunfounder.com/projects/pidog/en/latest/python/py_0_calibrate.html).

### Audio

PiDog examples run with `sudo`, which does not use the desktop PipeWire session.
`scripts/setup_audio.sh` makes the Robot HAT speaker the system ALSA default so
`Music()` works as root. Without that, wake-up fails with
`'Pidog' object has no attribute 'music'`.

```bash
ssh -t buck@buck.local 'bash ~/pidog-coding/scripts/setup_audio.sh'
```

If the googlevoicehat card is missing after that, reboot the Pi and run the
script again.

## Everyday workflow

Edit files under `src/`, then use:

```bash
./scripts/deploy.sh          # copy this workspace to the Pi
./scripts/check_remote.sh    # verify modules without moving PiDog
./scripts/run_hello.sh       # guarded sit/wag/bark demo; moves PiDog
```

The same commands are available in VS Code under **Terminal > Run Task**.

## Official resources

- [PiDog documentation](https://docs.sunfounder.com/projects/pidog/en/latest/)
- [Install all modules](https://docs.sunfounder.com/projects/pidog/en/latest/python/python_start/install_all_modules.html)
- [SunFounder PiDog source](https://github.com/sunfounder/pidog)
