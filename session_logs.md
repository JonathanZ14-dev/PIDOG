# PiDog Session Log

This file records each PiDog work session in chronological order. Each entry
separates completed work, verification results, safety notes, and next steps so
the robot's setup history is easy to follow.

---

## 2026-10-13 — Initial Raspberry Pi and coding setup

### Starting point

- Flashed the microSD card for the Raspberry Pi by following SunFounder's PiDog
website instructions before beginning this coding session.
- Configured the Raspberry Pi with:
  - Username: `buck`
  - Hostname: `buck`
  - Network address used for SSH: `buck.local`
- Opened the local `PIDOG_coding` folder as the workspace for custom code,
notes, and deployment tools.



### Raspberry Pi connection

- Confirmed that the Pi is reachable on the local network as
`buck@buck.local`.
- Created a dedicated Ed25519 SSH key on the Mac and copied only its public key
to the Pi.
- Verified passwordless SSH access. The Pi's `sudo` access still requires the
account password, which keeps privileged system changes protected.



### Verified hardware and operating system

- Model: Raspberry Pi Zero 2 W Rev 1.0
- Architecture: 64-bit ARM (`aarch64`)
- Operating system: Raspberry Pi OS based on Debian 13 (`trixie`)
- Python: 3.13.5
- Memory: approximately 415 MiB available to the operating system, plus swap
- Storage: approximately 29 GB total with about 22 GB free at inspection time
- Confirmed the system is 64-bit, as required by the current PiDog voice
dependencies.



### Local coding workspace created

- Organized custom Python programs under `src/`.
- Added `src/check_pidog.py`, a no-motion health check for the installed Python
modules.
- Added `src/hello_pidog.py`, a guarded first demonstration that can sit, wag
its tail, and bark only after calibration is explicitly confirmed.
- Added reusable scripts under `scripts/`:
  - `setup_pi.sh` — installs and verifies the official PiDog software stack.
  - `setup_audio.sh` — runs the separate interactive I2S audio setup.
  - `deploy.sh` — copies this workspace to `~/pidog-coding` on the Pi.
  - `check_remote.sh` — runs the no-motion health check remotely.
  - `run_hello.sh` — deploys and runs the guarded first-motion demonstration.
- Added VS Code tasks for deploy, no-motion checking, and the guarded demo.
- Expanded `README.md` with connection, installation, calibration, audio, and
everyday development instructions.
- Added `.gitignore` rules for Python, virtual environments, editor files, and
local secrets.
- Validated the shell scripts, Python syntax, VS Code task JSON, and Git diff
formatting locally.



### Software deployed to the Pi

- Deployed this workspace to `/home/buck/pidog-coding`.
- Downloaded SunFounder's official repositories to:
  - `/home/buck/robot-hat`
  - `/home/buck/vilib`
  - `/home/buck/pidog`
- Recorded repository revisions during setup:
  - Robot HAT: `4556bd8` on branch `2.5.x`
  - Vilib: `64c1e9a` on branch `main`
  - PiDog: `cee4bff` on branch `main`



### Official dependency installation

- Started the official installation sequence from
`~/pidog-coding/scripts/setup_pi.sh`.
- Installed the Robot HAT system dependencies, including I2C, SPI, speech,
SDL, PortAudio, SoX, and related development libraries.
- Installed Robot HAT's Python dependencies and SunFounder's voice-assistant
package.
- Completed the Vilib camera/vision installation, including OpenCV, FFmpeg,
OpenBLAS, camera support, and its Python dependencies.
- Verified installed package versions:
  - Robot HAT: 2.5.8
  - Vilib: 0.3.20
- Advanced to the final PiDog Python-package installation. It is currently
paused at a renewed `sudo` password prompt because the previous sudo session
expired during the long Vilib installation.



### Safety decisions

- No servo or body-motion command has been run during setup.
- The no-motion health check imports modules without creating a `Pidog()`
hardware instance.
- The first custom motion example refuses to run unless calibration is
explicitly confirmed.
- Servo calibration must be completed with the physical PiDog and calibration
ruler before the first motion test.
- The I2S audio installer is kept separate because it is interactive and may
reboot the Pi.



### Current status

- **Completed:** Robot HAT and Vilib installation.
- **In progress:** Final PiDog Python package; waiting for the visible `sudo`
password prompt in the IDE terminal.
- The Pi remains responsive and the installer is active.
- No hardware movement has occurred.



### Remaining work for today

- [x] Allow the Vilib installer to finish.
- [ ] Install the PiDog Python package if it is not already installed by the
  ```
  final setup stage.
  ```
- [ ] Run the no-motion module verification.
- [ ] Check for failed services and confirm the camera/audio-related packages.
- [ ] Run the separate I2S audio setup and reconnect after any required reboot.
- [ ] Perform physical servo calibration with the correct ruler.
- [ ] Run the guarded sit/wag/bark demonstration only after calibration.

---



## 2026-10-20 — Setup completion audit



### Checks performed

- Reconnected to `buck@buck.local` using the existing SSH key.
- Confirmed that the earlier setup installer is no longer running.
- Repeated all checks without creating a `Pidog()` instance, so no servos or
other moving hardware were activated.
- Confirmed there are no failed system services.
- Confirmed the Pi exposes both required hardware interfaces:
  - I2C: available at `/dev/i2c-1`
  - SPI: available through `/dev/spidev*`
- Verified the installed packages:
  - Robot HAT 2.5.8: installed system-wide and imports correctly.
  - Vilib 0.3.20: installed system-wide and imports correctly.



### Issue found

- The final PiDog package installation did not complete during the October 13
session.
- `import pidog` appeared to work when a check started in `/home/buck`, but it
was loading the downloaded source checkout at `/home/buck/pidog`.
- A clean test from `/tmp` correctly returned `ModuleNotFoundError`, and no
PiDog package metadata exists in the system Python installation.
- Updated `src/check_pidog.py` to verify installed package metadata as well as
imports. This prevents a source checkout from producing a false success.



### Current status

- **Ready:** SSH, Robot HAT, Vilib, I2C, SPI, and system services.
- **Not complete:** PiDog 1.4.0 must still be installed system-wide.
- **Not attempted:** audio configuration, physical servo calibration, and the
first movement demonstration.



### Next command

Run from the Mac's IDE terminal and enter `buck`'s password when prompted:

```bash
ssh -t buck@buck.local \
  'sudo python3 -m pip install ~/pidog --break-system-packages'
```

Then verify from outside the source checkout:

```bash
ssh buck@buck.local \
  'cd /tmp && python3 ~/pidog-coding/src/check_pidog.py'
```



### Remaining work

- [x] Install PiDog 1.4.0 system-wide.
- [x] Pass the corrected no-motion health check from `/tmp`.
- [x] Run and verify the separate I2S audio setup.
- [x] Complete physical servo calibration with the calibration ruler.
- [x] Run the guarded first-motion demonstration after calibration.



### Module completion and calibration preparation

- Confirmed PiDog 1.4.0 is now installed system-wide at
`/usr/local/lib/python3.13/dist-packages/pidog`.
- The corrected no-motion health check passes for all modules:
  - PiDog 1.4.0
  - Robot HAT 2.5.8
  - Vilib 0.3.20
- Reviewed SunFounder's current servo-calibration guide and the installed
`~/pidog/examples/0_calibration.py` controls.
- Confirmed no other PiDog or SunFounder control process is running.
- Confirmed healthy Raspberry Pi power status: `throttled=0x0` (no current or
recorded undervoltage/throttling flags).
- No servo movement was sent during these preparation checks.
- **Next physical step:** place PiDog on the flat calibration stand and identify
whether the included acrylic ruler is the 90-degree or 60-degree version.



### Servo calibration started

- Identified the included acrylic calibration ruler as the **60-degree** model.
- Placed Buck securely on the flat calibration stand.
- Ready to launch SunFounder's interactive `0_calibration.py` program.
- Calibration will proceed through leg servos 1–8 in pairs, with offsets saved
only after the physical alignment has been checked.

---



## 2026-10-20 — Wake-up music attribute error



### Issue

- `sudo python3 ~/pidog/examples/1_wake_up.py` failed after
`sound_effect init ... fail` with `'Pidog' object has no attribute 'music'`.
- Root cause: pygame/ALSA as root opened HDMI (`vc4hdmi`) instead of the Robot
HAT speaker (`sndrpigooglevoi`). That init exception was swallowed, so
`self.music` was never created and `pant()`/`speak()` crashed.



### Fix applied on the Pi

- Added `dtoverlay=googlevoicehat-soundcard` to `/boot/firmware/config.txt`.
- Wrote `/etc/asound.conf` so ALSA default is the Robot HAT speaker/mic.
- Confirmed `Music()` now initializes as root.
- Guarded installed `pidog.py` so a future sound init failure sets
`self.music = None` instead of crashing.



### Remaining work

- [x] Re-run `sudo python3 ~/pidog/examples/1_wake_up.py` on a safe stand.
- [x] Complete physical servo calibration with the calibration ruler.
- [x] Run the guarded first-motion demonstration after calibration.



### Servo calibration completed

- Calibrated all eight leg servos using the 60-degree ruler.
- Saved the offsets through SunFounder's calibration interface and exited the
program normally with `Ctrl+C`.
- Verified that `0_calibration.py` is no longer running.
- Verified the saved file at `/home/buck/.config/pidog/pidog.conf`.
- Saved leg offsets:
  ```text
  [11.8681, 8.7912, -1.3187, -2.1978,
   -0.8791, -1.3187, -7.4725, -1.3187]
  ```
- All eight offsets are within the calibration program's allowed ±20-degree
range.
- Added a backup to `calibration/pidog.conf.2026-10-20` in this workspace.
- Prepared a gentle first-motion test: move slowly into `sit`, wag the tail four
times, and stop. Walking, twisting, and audio are excluded from this first
test.



### Initial example testing and sensor diagnostics

- Ran SunFounder's Wake Up example after calibration.
- Motion completed, but the speaker produced no sound; audio remains a separate
troubleshooting item.
- Ran SunFounder's Patrol example and observed that obstacle detection did not
appear to respond.
- Stopped Patrol before diagnosis and confirmed no example process remained
active.
- Tested the ultrasonic sensor directly through Robot HAT pins without creating
a `Pidog()` instance, so no servos moved:
  - Trigger pin: `D1`
  - Echo pin: `D0`
  - Samples: 20
  - Result: all readings were `-1` (no echo before the driver timeout)
- Next diagnostic: repeat the sensor-only sample with a flat target held
15–20 cm directly in front of the ultrasonic transducers.



#### Ultrasonic near-target result

- Repeated 20 sensor-only readings with a flat target held 15–20 cm directly
in front of the transducers.
- All 20 readings again returned `-1`.
- Compared the diagnostic with SunFounder's installed official test at
`~/pidog/test/ultrasonic_test.py`; it uses the same Robot HAT configuration:
`Ultrasonic(Pin("D1"), Pin("D0"))`.
- Confirmed the GPIO mapping reported by the installed Robot HAT library:
  - `D0` / echo = GPIO 17, white wire
  - `D1` / trigger = GPIO 4, yellow wire
- Conclusion: Patrol logic is not the cause. The sensor has no echo response;
wiring, connector seating/orientation, power to the module, or the ultrasonic
module itself must be checked next.



#### Ultrasonic connection reseat and successful retest

- Powered/check-cycled Buck and reseated the ultrasonic sensor connection.
- Repeated the direct sensor-only test with 20 samples; no servo or body-motion
commands were sent.
- All 20 readings were valid, with no `-1` timeout results:
  ```text
  5.61, 5.39, 5.60, 5.14, 4.37, 4.82, 4.83, 5.05, 6.06, 5.60,
  5.83, 5.80, 5.82, 6.31, 5.90, 5.91, 6.03, 5.09, 6.33, 5.35 cm
  ```
- The median reading was approximately 5.6 cm. This confirms that the trigger,
  echo, and sensor module are now responding after the connection was reseated.
- The detected distance was shorter than the estimated 15–20 cm target
  placement. Before running Patrol again, the next check is to place a flat
  target at a measured 30 cm from the faces of the two ultrasonic transducers
  and verify that nothing else (the stand, a hand, wiring, or part of the robot)
  is blocking their forward field of view.
