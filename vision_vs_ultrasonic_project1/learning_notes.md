# Sensor lessons (after the system diagram)

Start with [system_diagram.md](system_diagram.md) and write in [system_diagram_notes.md](system_diagram_notes.md). Then follow the [pre-course sessions](experiment_sessions.md) and take notes in [the experiment notebook](experiment_notebook.md). This file supports the first stationary sensor check.

For a closer look at the script's terminal options, use the [argument-parsing lesson and notes](lesson_terminal_arguments.md).

## The first ultrasonic Python call

SunFounder's [PiDog ultrasonic test](https://github.com/sunfounder/pidog/blob/main/test/ultrasonic_test.py) constructs `Ultrasonic(Pin("D1"), Pin("D0"))` and calls `read()` for centimeters. Buck's earlier wiring notes match that setup: D1 is trigger and D0 is echo. Our first script uses the same call without importing or creating `Pidog`, so it does not command the servos.

```python
sensor = Ultrasonic(Pin("D1"), Pin("D0"))
reading_cm = sensor.read()
```

`sensor` is a Python object representing the hardware connection. `read()` asks the library for one measurement and returns a number. We will keep the raw reading and label values at or below zero as invalid. Buck has previously returned `-1` when no echo arrived. An invalid result must never mean "clear path" in the later movement program.

## Lesson 2: measure without movement

1. Keep Buck stationary. Face the ultrasonic transducers toward a broad, flat target. Measure the gap **from the transducer faces** to the target.
2. Put the target at a measured 30 cm and run 20 readings. Repeat at another measured distance, such as 50 cm, without changing the sensor angle. Keep hands, the stand, and loose wires out of the forward path.
3. Compare the printed readings with the physical distances. Look for clustering, large errors, and invalid readings. Do not choose an avoidance threshold until this check makes sense.

From the workspace on the Mac, after Buck is reachable:

```bash
./scripts/deploy.sh
ssh -t buck@buck.local 'sudo python3 ~/pidog-coding/vision_vs_ultrasonic_project1/01_measure_ultrasonic.py --target-cm 30 --output /tmp/pidog-sonar-30cm.csv'
```

If `buck.local` does not resolve, use Buck's current IP address in the SSH command. The saved `192.168.0.151` address may have changed. The CSV is saved **on Buck** at the path after `--output`; the terminal also shows each reading and a summary.

The script introduces `argparse` for command-line values, a `for` loop for repeated measurements, `if` for deciding whether a reading is valid, and `statistics.median` for a typical reading. We can read each part together when we have Buck's output.

## Check your understanding

- Why can `python3` on the Mac open the script but not read Buck's sensor?
- What does a `-1` reading tell us about this measurement? What does it **not** tell us about the space in front of Buck?
- If a target is physically 30 cm away but the median reading is 6 cm, which physical setup details would you inspect before changing the code?

The [next session](experiment_sessions.md#session-2--one-frame-from-the-camera) will inspect a camera image, also without moving Buck.
