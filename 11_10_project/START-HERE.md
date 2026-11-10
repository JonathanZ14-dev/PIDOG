# PiDog Python Vision Lab

**90 minutes · November 10, 2026 · Jonathan's student edition**

Today you will make PiDog locate a blue or green marker, show the pixels used as evidence, and report whether the marker is left, center, or right in its image. You will run complete programs, read their comments, predict results, change one thing, and test again. There are no unfinished code exercises. Your goal is to explain and modify a working system.

The core activity is a small color-based perception module. It is deliberately transparent: you can inspect every decision. Unlike a pretrained object detector, it has no learned weights and cannot name arbitrary objects. This helps us understand the Python pipeline that can later surround a learned detector.

## Open the materials

Open **index.html** on your laptop for the lesson, **code-tour.html** for all the commented source, and **iPad-Notes.pdf** in Apple Files, Goodnotes, or Notability for handwriting. You can also type into the lesson's notes areas in a browser. Export notes before closing or moving the folder; local browser storage is not a backup. The browser guide is an offline document, not an editor that runs Python.

All code is in vision/. Copy this student folder to PiDog. The teacher folder is a separate companion and is not required to run anything. Bring a blue and a green card or object, a ruler, and something with a similar color to use as a distractor. Keep the robot stationary while moving the targets.

## Before the 90-minute lesson: prepare with your teacher

From your laptop, in the directory containing student/:

```sh
scp -r student buck@buck.local:~/pidog-python90
ssh buck@buck.local
cd ~/pidog-python90
python3 -c "import cv2, numpy, picamera2; from PIL import Image; print(cv2.__version__)"
```

Use your existing SSH address if it differs. Stop the earlier camera preview or Vilib program so only one program owns the camera. Run with the Pi's system Python. If imports already work, do not reinstall anything. If they fail, your teacher can install missing packages with:

```sh
sudo apt update
sudo apt install python3-opencv python3-numpy python3-picamera2 python3-pil
```

The commands below belong in a terminal, not at a Python `>>>` prompt. `python3 -m vision.run` means run the module named run inside the package vision. Start in the folder containing vision/. Our programs do not import Pidog or move servos.

First confirm the software without needing the camera:

```sh
python3 -m vision.play
python3 -m vision.run --demo --frames 3 --interval 1 --out runs/demo01
```

Then capture one real observation:

```sh
python3 -m vision.run --camera --out runs/blue01
```

Every run needs a new output folder, such as blue02. The folder contains original.png, mask.png, annotated.png, latest.json, history.jsonl, and index.html. Images contain only the latest frame; history.jsonl keeps all observation records. Preserve a particular picture using a one-frame run before a controlled comparison.

## See results on the laptop or iPad

Open a SECOND SSH terminal on the Pi and run:

```sh
cd ~/pidog-python90
python3 -m http.server 8000 --bind 0.0.0.0 --directory runs
```

On the same trusted Wi-Fi, open **http://buck.local:8000/blue01/** on the laptop or iPad. If the hostname does not resolve, run `hostname -I` on the Pi and use its local IP instead. This simple server has no login and shares the runs folder with devices that can reach the Pi; stop it with Ctrl+C after class. Do not expose or forward this port to the internet.

For repeated observations, in your FIRST SSH terminal:

```sh
python3 -m vision.run --camera --frames 30 --interval 1 --out runs/moving01
```

Open http://buck.local:8000/moving01/ after its first frame. Move the marker slowly. The viewer refreshes every three seconds; processing and saving add time. It is not a high-frame-rate stream. Check timestamps: the last image stays visible after the program stops. JSON and images may briefly show adjacent frames during an update; use a completed one-frame run for exact comparisons.

If local networking blocks the viewer, copy results to your laptop:

```sh
scp -r buck@buck.local:~/pidog-python90/runs/blue01 ./blue01-results
```

Open the PNGs and latest.json directly. No graphical desktop is needed on the Pi. If the camera fails, use --demo or --image with an earlier PiDog picture while you investigate the camera separately.

## Optional laptop replay

On a laptop inside student/, create a separate environment. This does not replace PiDog's installed libraries:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-laptop.txt
python3 -m vision.run --image blue01-results/original.png --out runs/laptop01
```

Windows: use `.venv\Scripts\python.exe` in place of python3, and skip the activation command above. Camera mode is for the Raspberry Pi; it does not remotely open PiDog's camera from a laptop.
