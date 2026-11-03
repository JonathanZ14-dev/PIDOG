# Pre-course experiment sessions

Follow these after [the system diagram](system_diagram.md). Record predictions and results in [the experiment notebook](experiment_notebook.md). The loop for every session is **predict → run one small test → inspect raw output → explain → change one thing**. The goal is to understand the interfaces before Buck attempts an obstacle course.

None of sessions 1–4 sends a PiDog motion command. Session 5 is a separate, supervised motion check on the stand. The scripts are starting points for us to read and change together.

## Before using Buck

- Buck must be powered, reachable by SSH, and stationary in a clear space. He is not powered or connected as we prepare these sessions, so all hardware results remain **not run**. Confirm the current network address when he is powered; `buck.local` did not resolve during our last connection attempt.
- Deploy from the Mac with `./scripts/deploy.sh`. If the hostname is unavailable, set `PIDOG_TARGET=buck@CURRENT_IP` for deployment and use the same address in SSH/SCP commands below.
- Keep sensor samples and camera images in `/tmp` on Buck. Copy only the results we decide to keep. Camera images can show the room, so review them before adding any to Git.
- Do not run two camera programs at once. Stop a failed capture program before retrying.

## Session 1 — One number from the ultrasonic sensor

**Question:** Does a measured target produce a plausible, repeatable centimeter reading?

**System path:** Python → Robot HAT D1 trigger → ultrasonic module → D0 echo → `robot_hat.Ultrasonic.read()` → Python number.

**Python ideas:** imports, arguments, a `for` loop, `if` for invalid values, lists, median, CSV.

1. Read [the ultrasonic lesson](learning_notes.md) and [the script](01_measure_ultrasonic.py). Use the [terminal arguments lesson](lesson_terminal_arguments.md) to study `parse_args()` and take notes. Predict what a `-1` reading will be labeled.
2. Measure a broad, flat target at 30 cm from the transducer faces. Keep Buck still. Run 20 readings:

   ```bash
   ssh -t buck@buck.local 'sudo python3 ~/pidog-coding/vision_vs_ultrasonic_project1/01_measure_ultrasonic.py --target-cm 30 --output /tmp/pidog-sonar-30cm.csv'
   ```

3. Repeat at a second measured distance, such as 50 cm, with a different CSV path. Record valid count, median, and any strange values.

**Ready for session 2 when:** we can explain what `read()` returned, what invalid means, and whether the readings track the target's physical distance. If they do not, inspect setup and wiring before trusting sonar in movement code.

## Session 2 — One frame from the camera

**Question:** Can Python receive and save a usable image from Buck's camera?

**System path:** camera → Pi camera interface → Picamera2 → Python → JPEG file. [Raspberry Pi's Picamera2 examples](https://github.com/raspberrypi/picamera2/blob/main/examples/capture_to_buffer.py) use camera configuration, `start()`, and `capture_file()` for still images.

We use Picamera2 directly for this first frame so the camera input is easy to inspect. Vilib is installed on Buck, but its higher-level vision features are a later step.

**Python ideas:** an object, a method call, `try/finally` cleanup, a `Path`, and a timestamp.

1. Predict what a useful frame should show. Place one soft target in view while Buck stays still.
2. Read [the camera script](02_capture_camera.py), then capture:

   ```bash
   ssh -t buck@buck.local 'sudo python3 ~/pidog-coding/vision_vs_ultrasonic_project1/02_capture_camera.py --output /tmp/pidog-camera-test.jpg'
   scp buck@buck.local:/tmp/pidog-camera-test.jpg /tmp/pidog-camera-test.jpg
   ```

3. Inspect the image on the Mac. Record whether the target is visible, its position, lighting, orientation, and anything that could confuse an image detector.

**Ready for session 3 when:** an actual image opens and we can describe what the image contains. An installed camera package alone does not pass this session.

## Session 3 — One paired sensor snapshot

**Question:** Can one Python process use both sensor interfaces and give each observation a timestamp?

**System path:** both sensor branches enter one Python program. The program saves `camera.jpg` plus `sensor_reading.json`; it does not decide or move. These samples are **sequential**, not simultaneous.

**Python ideas:** dictionaries, JSON, timestamps, data validity, and separate sensor responsibilities.

1. Predict what the sonar reading and image should show for one stationary target.
2. Read [the paired snapshot script](03_capture_pair.py), then choose a new output directory:

   ```bash
   ssh -t buck@buck.local 'sudo python3 ~/pidog-coding/vision_vs_ultrasonic_project1/03_capture_pair.py --output-dir /tmp/pidog-pair-001'
   scp -r buck@buck.local:/tmp/pidog-pair-001 /tmp/pidog-pair-001
   ```

3. Open the JPEG and JSON. Label the image **clear**, **blocked**, or **unknown** by eye. Compare that label with the centimeter reading. Note the two timestamps.

**Ready for session 4 when:** we can say which value came from which sensor, how old each value was, and why an invalid sonar value is different from an open path.

## Session 4 — Preview the mode selector and decision

**Question:** Does the same pair of observations lead to different decisions when the allowed sensor changes?

This is a **print-only simulation on the Mac**. We supply a human label for the camera image and a sonar number from a snapshot. The program does not inspect the image or read hardware. Its 25 cm threshold is an example for learning; it is not a calibrated movement threshold.

**Python ideas:** function inputs and return values, Boolean/unknown states, comparisons, mode isolation, and a fail-safe stop.

Read [the decision rule](decision_logic.py) and [the preview program](04_preview_decision.py). Predict each result before running:

```bash
python3 vision_vs_ultrasonic_project1/04_preview_decision.py --mode vision --vision clear --sonar-cm 10
python3 vision_vs_ultrasonic_project1/04_preview_decision.py --mode ultrasonic --vision blocked --sonar-cm 40
python3 vision_vs_ultrasonic_project1/04_preview_decision.py --mode combined --vision clear --sonar-cm 10
python3 vision_vs_ultrasonic_project1/04_preview_decision.py --mode combined --vision clear --sonar-cm -1
```

Then substitute the image label and sonar number from session 3. Explain which evidence each mode was allowed to use. Change one input and predict the effect before rerunning.

**Ready for session 5 when:** we can explain every printed decision, including why missing required data stops the preview. This is still a human-labeled vision demonstration; automatic image detection comes later.

## Session 5 — Check the movement interface separately

**Question:** Can Buck execute one known, bounded action and stop it on the stand?

**System path:** Python → `Pidog` motion API → Robot HAT → servos. This session tests that path alone; it does **not** connect the sensor preview to motion.

**Python ideas:** guarded command-line flags, hardware initialization, `try/finally`, and closing the PiDog object.

Review [the existing guarded motion script](../src/hello_pidog.py) and its [run wrapper](../scripts/run_hello.sh). Only run it with Buck physically supported on the stand, calibration confirmed, and leg/tail space clear. Record what action occurred and whether the program ended cleanly. A person must be present to stop the robot if needed.

**Ready to design the course runner when:** the two sensors work independently, the paired snapshot makes sense, mode selection behaves as predicted, and the motion interface has passed a separate supervised check. We will then add automated image detection and connect decisions to bounded movement one step at a time.
