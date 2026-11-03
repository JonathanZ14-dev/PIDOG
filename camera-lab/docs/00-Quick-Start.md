# Quick Start · Camera lab on your PiDog

This is a separate companion package for the two camera sessions. It does not replace your working PiDog installation or the previous obstacle-course kit. Extract the complete ZIP. Open index.html on your laptop for lessons and notes. Run camera commands on the Raspberry Pi through your existing SSH connection. Run fixture analysis and tests on either machine.

## 1 Prepare the physical experiment

Use the assembled, calibrated robot, a charged battery, ruler, matte blue paper or a blue-covered box, red paper, a neutral background, and a way to copy files from the Pi. Keep PiDog stationary on a clear floor. Stop other programs that control the robot or own the camera. The supplied camera code sends no servo commands; a separately running app still could.

Do not reconnect a camera ribbon while powered. If the camera is not detected, shut down and disconnect power before inspecting the cable. Confirm the actual installed camera model rather than assuming every PiDog kit or replacement camera is identical.

## 2 Put the package on the Pi

Use your usual file-transfer tool, or run the following on your LAPTOP. Replace YOUR_USER and YOUR_PI_IP with the values from your working SSH connection. The local camera-lab folder must exist in the current laptop directory.

```sh
scp -r camera-lab YOUR_USER@YOUR_PI_IP:~/camera-lab
ssh YOUR_USER@YOUR_PI_IP
cd ~/camera-lab
pwd
ls
```

If you extracted a folder with a different name, rename it camera-lab or adjust the paths. Python commands below run from this project root, the folder containing camera_lab, docs and tests. A command starting with python3 -m loads a module from that location. Do not type the printed shell prompt or the Python >>> prompt as part of a command.

## 3 Record the existing environment before changing it

```sh
python3 --version
python3 -m camera_lab.doctor
```

The offline lessons require Python 3.9 or later and only its standard library. Live capture needs Raspberry Pi OS with a working modern camera stack, Picamera2 and Pillow. Vilib is optional for the vendor preview. The doctor reports package paths and methods so an unexpected interpreter is visible. Your previous PiDog install may already provide everything needed.

On newer Raspberry Pi OS, check camera enumeration with:

```sh
rpicam-hello --list-cameras
```

If that command does not exist but your older installation provides libcamera-hello, use:

```sh
libcamera-hello --list-cameras
```

These are alternatives, not two required installation steps. Do not use legacy raspistill instructions for this package. Camera enumeration confirms discovery, not image quality.

Only if Picamera2 or Pillow is missing from the system Python, use the Raspberry Pi OS packages:

```sh
sudo apt update
sudo apt install python3-picamera2 python3-pil
```

Prefer the working system interpreter. If you deliberately use a virtual environment, it must see the system camera packages; a tutor can create one with python3 -m venv --system-site-packages .venv. Do not mix random pip upgrades into the working robot image. This lesson does not require installing OpenCV, a neural-network framework, cloud keys or a new OS.

## 4 Prove the offline path first

```sh
python3 -m unittest discover -s tests -v
python3 -m camera_lab.analyze data/blue-center.json --out results/first-fixture
python3 -m camera_lab.learn data/TOY-learning.csv
```

The reference software tests should pass. Read the image-analysis report and the learning results, then explain what each reported value means. Results directories must be new: choose a suffix like -02 for repeats. The synthetic fixture route works without a robot and can keep the lesson moving while a hardware problem is investigated.

## 5 Capture once, then inspect

```sh
python3 -m camera_lab.capture --out captures/first-real
python3 -m camera_lab.analyze captures/first-real/frame.json --out results/first-real
```

Capture starts only the camera. It writes RGB data and a viewable SVG. Analysis writes report.json, image.svg with overlays, and mask.svg. A folder may remain empty after a failed capture; keep the error in your notes and choose a new trial name after fixing the cause.

To inspect through an SSH-only setup, run this on your LAPTOP from a folder where you want the results:

```sh
scp -r YOUR_USER@YOUR_PI_IP:~/camera-lab/captures/first-real ./first-real-capture
scp -r YOUR_USER@YOUR_PI_IP:~/camera-lab/results/first-real ./first-real-analysis
```

Open the copied SVGs in your laptop browser. JSON opens in an editor. Do not assume a preview window can appear inside an SSH terminal. The capture program intentionally requires no graphical desktop.

## 6 Optional vendor preview

Close the capture process first. Run python3 -m camera_lab.vilib_preview --seconds 30, then use http://YOUR_PI_IP:9000/mjpg on the same local network. Add --blue only when doctor reports color_detect is available. A stream opens a local-network web endpoint; do not expose the port to the internet. The program ends after the requested time or Ctrl+C and closes Vilib's camera.

The official ball/face examples can move PiDog. Their commands belong in the later supervised robot activity, not in a stationary camera check. Today's lesson links their pages for video viewing and code reading.

## Troubleshooting by layer

| Symptom | First useful check | Next action |
| --- | --- | --- |
| No module named camera_lab | pwd and ls | Return to the extracted project root; use -m as shown |
| No module named picamera2 or PIL | doctor executable and paths | Use system Python; install only missing OS packages |
| No cameras available | list-cameras | Check hardware with power disconnected; verify sensor support |
| Camera already acquired / resource busy | Another preview, app or process may own it | Stop the known owner cleanly before opening another |
| Permission denied | Compare interpreter/user with working examples | Have tutor inspect group/device permissions; do not blindly run all code as root |
| No desktop preview | You are using SSH | Inspect saved SVGs on laptop or optional web preview |
| Red object appears blue | Confirm explicit PIL RGB conversion | Inspect known red and blue samples before changing thresholds |
| Image upside down or left/right surprising | Capture labeled L/R targets | Record orientation; deliberately transform images before defining navigation axes |
| Empty mask on blue object | Inspect actual HSV, illumination and crop | Tune on calibration images, changing one setting at a time |
| Dark image reports unknown | Mean value below quality threshold | Improve capture conditions; do not convert unknown to clear |
| FileExistsError | Output directory already exists | Use a new trial identifier; preserve previous evidence |

## Notebook use

Each lesson has writable fields and checkboxes. Browser storage is local and can be blocked or cleared. Export an editable JSON backup from each document after class; restore it on that same document to continue elsewhere. Export Markdown for readable notes. Print / PDF includes answers and writing space. Exported notes do not embed your experiment images; preserve the captures and results folders alongside them.

:::note setup_record | Record the exact interpreter, camera enumeration, package versions, completed checks, and any unresolved blocker. | 7
