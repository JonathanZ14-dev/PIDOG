# PiDog obstacle course: vision, ultrasonic, and both

## Purpose

Build and test a small obstacle course for Buck (PiDog) using three sensing modes:

1. **Vision only:** the camera supplies obstacle information.
2. **Ultrasonic only:** the forward ultrasonic sensor supplies obstacle information.
3. **Combined:** the camera and ultrasonic sensor both supply obstacle information.

We will build this together in short lessons. The goal is to understand the Python code and the Pi's hardware/software path well enough to explain each sensor reading, movement decision, and test result. A successful project is a repeatable comparison, not just one run in which Buck reaches the finish.

## Main question

How does Buck's ability to finish the same course change when it uses the camera, the ultrasonic sensor, or both?

We will record what happened in each run, including stops, contacts, missed obstacles, and sensor failures. We will discuss why a mode succeeded or failed rather than treating the fastest time as the only result.

## Scope and working assumptions

- Start with a short, indoor, flat course made from stable, soft obstacles. A person will supervise every moving trial.
- Use the same start position, obstacle layout, movement commands, and finish condition for all three modes. Change only which sensor information the decision code may use.
- For the first vision version, use obstacles with a distinct, consistent color or appearance so we can learn camera frames and a simple image-processing method. This is a **structured-course** test, not a claim that the camera can recognize every object.
- The ultrasonic sensor measures forward clearance. A single forward reading does not describe the whole scene. Camera-based decisions will use image position and apparent size; we will establish useful thresholds by observation on the actual course.
- The combined mode will have an explicit rule for conflicting or missing readings. The initial rule is to stop when either sensor reports an immediate hazard or when the readings needed for a safe decision are unavailable. We can revise the rule after inspecting logged data.
- Do not add remote AI or autonomous exploration to the first version. Sensor processing and movement decisions should run locally on Buck.

These are design choices for the first experiment. We can revise them after the stationary sensor lessons, and record any changes before comparing trial results.

## Learning path

Each step should leave us with a small program or observation that works on its own.

Working documents: [system diagram](system_diagram.md), [diagram notes worksheet](system_diagram_notes.md), [pre-course experiment sessions](experiment_sessions.md), and [experiment notebook](experiment_notebook.md). The [ultrasonic lesson](learning_notes.md) supports the first sensor session.

| Step | What we will learn | Evidence before moving on |
| --- | --- | --- |
| 1. Map the system | Raspberry Pi, camera, ultrasonic sensor, Robot HAT, PiDog motion library; where Python runs and how data reaches it | Draw the data flow for both sensors and the movement commands |
| 2. Read ultrasonic data | Python imports, variables, functions, loops, units, invalid readings, and timeouts | Log repeated readings at measured target distances without moving Buck |
| 3. Read camera frames | Camera device, frames, pixels, image coordinates, and frame timing | Save or display frames and confirm the course obstacles are visible |
| 4. Detect obstacles | Python functions and simple image processing; thresholds and false detections | Mark detected obstacle regions in recorded frames, with no movement |
| 5. Decide without moving | Conditions, a small state machine, and separation of sensing from decisions | Replay sample readings through each mode and print `forward`, `turn`, or `stop` |
| 6. Connect motion | PiDog movement calls, timing, safe shutdown, and the operator stop control | Check short commands on the stand, then supervised low-speed floor movement |
| 7. Run the course | Logging, repeatable trials, and fair comparisons | Complete and record trials in all three modes |
| 8. Analyze results | Basic Python data analysis and measurement limits | Summarize each mode's outcomes and explain observed differences |

At each step, we will inspect the raw output before trusting a higher-level decision. The code should keep sensor reading, decision making, and movement in separate functions so each can be understood and tested independently.

## Experiment design

Before trials, mark the start and finish, record the obstacle positions and sizes, and photograph the layout. Choose a floor surface and lighting that can remain reasonably consistent. Set the camera angle, walking speed, decision interval, stop threshold, and turn behavior from stationary checks and short supervised trials; write the chosen values down.

Run the same course several times per mode. Rotate the order of modes between rounds so changes in lighting, battery state, or course setup do not always favor the same mode. Reset Buck and the obstacles to their marked positions before each trial. Keep a person close enough to stop Buck immediately.

For each trial, record:

- Mode, trial number, start time, and course configuration.
- Whether Buck reached the finish, stopped safely, needed operator intervention, or touched an obstacle.
- Elapsed time and number of stops or turns.
- Timestamped sensor readings, chosen decisions, invalid readings, and any software errors.
- Notes on lighting, battery condition, obstacle movement, and anything unusual.

We will compare completion rate, contacts, interventions, and time among **completed** trials. A run that stops safely because it cannot see enough should be recorded separately from a run that hits an obstacle. We will also review a few logs frame by frame to understand specific failures.

## Safety and prerequisites

- Buck's servo calibration is recorded as completed in `session_logs.md`. Recheck physical condition and use the existing calibration guidance before motion work.
- The earlier ultrasonic test returned valid readings after the connector was reseated, but they were shorter than the estimated target distance. Verify readings against a measured target at several distances and check for `-1` timeouts before relying on them.
- Confirm the camera provides usable frames on Buck before choosing the vision algorithm.
- Complete sensing and decision tests without body motion first. Test initial motion with Buck supported on the stand, then use a clear, supervised floor area.
- Start slowly with soft obstacles. Keep a direct operator stop method available and stop the program on missing sensor data, stale frames, or unexpected errors. Never interpret an invalid ultrasonic reading as an open path.

## First deliverables

1. A simple diagram of the camera and ultrasonic data paths.
2. Small, no-motion sensor scripts and saved sample outputs.
3. A decision module that can run on recorded readings without Buck.
4. One course runner with a mode setting: `vision`, `ultrasonic`, or `combined`.
5. A trial log and a short comparison of the three modes.

## Decisions to make together after the sensor checks

- Exact course layout, obstacle materials, and what counts as crossing the finish.
- Which camera-visible features to detect in version one.
- Walking speed, obstacle thresholds, turn behavior, and the number of trials per mode.
- Whether the first course is a straight path with stopping/turning or a route that requires navigating around obstacles.

**Next step:** map the hardware and software data flow, then validate the ultrasonic readings with a measured target while Buck remains still.
