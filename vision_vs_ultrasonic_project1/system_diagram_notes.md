# My system diagram notes

Use this file as a working notebook. Short answers are fine. We can edit it together as we inspect Buck and run each sensor check. Keep a guess marked as a guess until we have an observation or source.

**Session date:**

**What I can see on Buck:**

| Component | Where I found it / how it connects | My questions |
| --- | --- | --- |
| Raspberry Pi |  |  |
| Camera and ribbon cable |  |  |
| Ultrasonic module |  |  |
| Robot HAT |  |  |
| Leg servos |  |  |
| Battery, power, and ground connections |  |  |

## Trace the two sensor paths

**Camera path, in my own words:**

> The obstacle's appearance reaches Python by...

**Ultrasonic path, in my own words:**

> Python sends a trigger by... The echo returns by... The library reports...

**Where is our Python program running? What does SSH do?**

> [Write here]

**What is different about a frame and a distance reading?**

> [Write here]

## Trace one decision

Imagine a soft obstacle directly ahead. Describe what each mode may use and what you think it should do. These are predictions; we will test them later.

| Mode | Allowed sensor evidence | My predicted decision and why |
| --- | --- | --- |
| Vision only |  |  |
| Ultrasonic only |  |  |
| Combined |  |  |

## Facts, guesses, and checks

| Statement | Fact, guess, or open question? | Evidence or planned check |
| --- | --- | --- |
| Buck's ultrasonic trigger is D1 / GPIO 4. | Recorded fact | `session_logs.md` and SunFounder documentation |
| Buck's ultrasonic echo is D0 / GPIO 17. | Recorded fact | `session_logs.md` and SunFounder documentation |
| The camera currently delivers usable frames. | Open question | Stationary camera capture lesson |
| The ultrasonic reading matches a target at 30 cm. | Open question | Measured target lesson |
|  |  |  |

## Questions for our next conversation

1. [Question]
2. [Question]
3. [Question]

## What I can explain now

- [ ] I can show where the Mac stops and Buck's Pi begins.
- [ ] I can trace the camera path to a Python frame.
- [ ] I can trace ultrasonic trigger and echo in opposite directions.
- [ ] I can explain how vision only, ultrasonic only, and combined modes differ.
- [ ] I can identify at least one claim in the diagram that still needs testing.

**One thing I learned:**

> [Write here]

**One thing that is still confusing:**

> [Write here]
