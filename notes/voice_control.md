# Buck voice-control notebook

## Goal

Build voice control in small, understandable layers. Each layer must work by
itself before it is connected to Buck's movement system.

## The complete pipeline

```text
your voice
    |
    v
Robot HAT microphone -> ALSA/PortAudio -> speech-to-text (Vosk)
                                              |
                                              v
                                      recognized text
                                              |
                       +----------------------+
                       |
                       v
              safe command parser
                       |
                       v
               allowlisted action
                       |
                       v
                 PiDog action API

Optional response path:

recognized text -> language model -> response + allowed action
                                      |
                         +------------+------------+
                         |                         |
                         v                         v
                 text-to-speech (Piper)       PiDog action API
                         |
                         v
                 Robot HAT speaker
```

The language model is optional. Basic commands such as "sit," "stand," and
"stop" can remain fully offline and deterministic.

## Components and responsibilities

| Component | Purpose | Runs where | Network needed? |
| --- | --- | --- | --- |
| Robot HAT microphone | Converts sound into an electrical/digital signal | Buck | No |
| ALSA | Linux audio device and routing layer | Buck | No |
| PortAudio / `sounddevice` | Gives Python access to the microphone | Buck | No |
| Vosk | Converts recorded speech into text | Buck | Only for the first model download |
| Command parser | Maps recognized phrases to a small allowlist | Our code | No |
| PiDog action API | Executes the chosen physical action | Buck | No |
| Piper | Converts response text into speech | Buck | Only for the first voice download |
| Wake phrase | Keeps Buck idle until a phrase such as "Hey Buck" is recognized | Vosk + our code | No |
| LLM (optional) | Handles open-ended conversation and proposes actions | Cloud or another computer | Usually |

## Why we are building the non-AI version first

A fixed command parser is easy to inspect and test. The recognized text must
match an action we explicitly allowed; unknown text does nothing. This lets us
separate recognition errors from robot-control errors and prevents arbitrary
model output from directly controlling servos.

## Safety rules

1. Audio and speech-recognition tests do not import or initialize `Pidog`.
2. Parser tests print the selected action but do not execute it.
3. Motion is added only after audio and parsing pass independently.
4. The first physical-action test is performed with Buck on the stand.
5. `stop` is always a local command and never depends on an LLM or internet
   service.
6. LLM-proposed actions must pass through the same fixed allowlist.
7. API keys belong in `.env` or an ignored `secret.py`; they are never committed.

## What is installed on Buck

Checked on 2026-10-22:

- Robot HAT playback device: `sndrpigooglevoi`, card 1, device 0.
- Robot HAT capture device: `sndrpigooglevoi`, card 1, device 0.
- Python/PortAudio default device: index 7, named `default`.
- `sounddevice` 0.5.6.
- `vosk` 0.3.45.
- `piper-tts` 1.8.0.
- `sunfounder-voice-assistant` 1.1.9.
- `pidog.stt.Vosk`, `pidog.tts.Piper`, and
  `pidog.voice_assistant.VoiceAssistant` import successfully.
- SunFounder's installed examples include `20_voice_active_dog_gpt.py` and its
  supporting `voice_active_dog.py`.

## Learning plan

- [x] Map the voice-control architecture.
- [x] Confirm that Linux and Python can see the Robot HAT microphone.
- [x] Lesson 1: record a short WAV file and measure the microphone signal.
- [x] Lesson 2: transcribe one sentence locally with Vosk.
- [x] Lesson 3: build and unit-test a fixed command parser without movement.
- [x] Lesson 4: connect Vosk to the parser for a no-motion voice preview.
- [ ] Lesson 5: connect one safe command to one PiDog action on the stand.
- [ ] Lesson 6: add a continuous offline listening loop.
- [ ] Lesson 7: test Piper and give Buck a spoken response.
- [ ] Lesson 8: combine listening, command selection, action, and response.
- [ ] Optional: add an LLM for conversation while retaining the action allowlist.

## Lesson 1 — microphone signal

The microphone produces many samples per second. For speech recognition we use
16,000 samples per second, one channel, and signed 16-bit samples. This common
format is written as **16 kHz, mono, S16_LE**.

`src/voice_control/01_record_and_measure.py` records a short sample and reports:

- **Peak**: the loudest individual sample.
- **RMS**: the average signal energy, which is more useful for judging normal
  speech loudness.
- **dBFS**: level relative to the loudest value a digital sample can represent.
  Zero dBFS is maximum; normal speech should be negative. Values near zero may
  clip, while extremely low values suggest a muted or disconnected microphone.

Run it only when prompted during the lesson:

```bash
python3 ~/pidog-coding/src/voice_control/01_record_and_measure.py
```

The recording is saved under `/tmp` on Buck and is not committed to Git.

### Lesson 1 result

The first recording passed:

| Measurement | Result | Meaning |
| --- | ---: | --- |
| Format | 16 kHz, mono, signed 16-bit PCM | Correct for our speech pipeline |
| Duration | 4.000 seconds | Correct |
| Peak | -9.2 dBFS | Healthy headroom below clipping |
| RMS | -38.4 dBFS | Somewhat quiet, but usable |
| Clipped samples | 0.000% | No distortion from overload |

This proves the hardware microphone, ALSA route, PortAudio, and Python capture
layer work together. It does not yet prove that speech recognition can
understand the words.

## Lesson 2 — offline speech-to-text

Vosk is the **speech-to-text (STT)** engine. A language model contains patterns
that let the recognizer turn audio samples into likely words. The small English
model is downloaded to `~/.vosk_models` on the first run; recognition then runs
locally without sending microphone audio to a cloud service.

Vosk can produce two kinds of output: a changing **partial transcript** while
you speak and a stable **final transcript** after an utterance ends. Our lesson
script uses a fixed six-second recording first, then asks Vosk for the final
result. Separating capture from recognition ensures that the exact audio can be
replayed while troubleshooting.

Run:

```bash
python3 ~/pidog-coding/src/voice_control/02_transcribe_once.py
```

Wait one second, say one sentence, and then remain quiet. The exact input is
saved as `/tmp/buck-vosk-last.wav`. Replay it on Buck with:

```bash
aplay -D default /tmp/buck-vosk-last.wav
```

This script imports only audio and speech-recognition code and cannot move Buck.

### Lesson 2 result

After raising the Robot HAT microphone control from 51% to 75%, the saved test
had a peak of -6.0 dBFS, RMS of -29.3 dBFS, and no clipping. Vosk successfully
transcribed the spoken command. Compared with lesson 1, the average speech
signal improved by about 9 dB while retaining safe headroom.

## Lesson 3 — the command safety boundary

Speech recognition returns ordinary text; it should not call servo functions
directly. `command_parser.py` acts as a gate:

```text
recognized text
      |
      v
normalize case, punctuation, and spaces
      |
      v
check the emergency stop token
      |
      v
remove optional "Hey Buck" and "please"
      |
      v
exact allowlist match ---- no match ----> NO ACTION
      |
      v
approved internal action name
```

Important design choices:

- Aliases such as `sit` and `sit down` map to the same internal action.
- Unknown or multi-command phrases produce no action.
- Matching whole normalized phrases avoids mistakes such as finding `sit`
  inside an unrelated word.
- The standalone word `stop` overrides other words because a false stop is
  safer than unintended continued movement.
- The parser has no PiDog imports, so it is easy to test on any computer.

Run its demonstration:

```bash
python3 ~/pidog-coding/src/voice_control/03_try_command_parser.py --demo
```

Then try your own phrases interactively:

```bash
python3 ~/pidog-coding/src/voice_control/03_try_command_parser.py
```

Every result states `Motion: disabled in this lesson`.

## Lesson 4 — integrated voice-command preview

The microphone/Vosk component and parser now share a narrow interface: one
plain-text transcript. This is **composition**—small components are connected
without either component needing to know the other's internal details.

`speech_input.py` owns recording, WAV storage, signal measurements, and Vosk.
`command_parser.py` accepts text and returns a decision. The preview program
connects them:

```text
SpeechResult.transcript -> parse_command() -> ParseResult.action
```

Run one integrated preview:

```bash
python3 ~/pidog-coding/src/voice_control/04_voice_command_preview.py
```

Say one allowed phrase such as "Hello Buck, please sit down," then pause. The
program prints the exact transcript, normalization, action decision, and reason.
It still has no PiDog import and ends with `Motion: disabled in this lesson`.

## Lesson 5 — one guarded physical action

`05_voice_move_once.py` performs exactly one listen-decide-act cycle. The order
is intentional:

```text
record -> transcribe -> parse -> validate -> safety flags -> countdown
                                                        |
                                                        v
                                               initialize PiDog
                                                        |
                                                        v
                                            one bounded action -> close
```

The physical `Pidog` object does not exist while speech is being recognized.
It is created only after all of these checks pass:

1. Vosk returned text.
2. The parser returned one allowlisted action.
3. The motion layer independently approves that action.
4. `--execute` was supplied.
5. Calibration and stand placement were explicitly confirmed.

The movement layer currently supports only `sit`, `stand`, `lie`, and four tail
wags. Forward walking and turns are intentionally excluded from this first
voice-motion test. Postures use reduced speeds, and `dog.close()` runs even if
an error or interruption occurs.

The program defaults to a dry run. Physical movement requires:

```bash
python3 ~/pidog-coding/src/voice_control/05_voice_move_once.py \
  --execute --i-have-calibrated --on-stand
```

Always physically check the stand and clear space around every leg immediately
before running that command.

## Lesson 6 — continuous active listening

`06_active_voice_control.py` keeps the Vosk model and PiDog connection loaded
and repeats this bounded cycle:

```text
record 6 seconds -> transcribe -> exact allowlist check -> one short action
                                                              |
                                                              v
                                                        listen again
```

The loop does not require a wake phrase. It accepts bare commands such as "sit
down" whenever they are captured in a listening window. The command still must
match the small action allowlist exactly; ordinary conversation and unknown
phrases cause no movement. The word `stop` exits the program. Ctrl+C also
exits, and `dog.close()` always runs during shutdown.

The loop overwrites `/tmp/buck-active-command-last.wav` each round. This keeps
the most recent input available for replay without filling the SD card with
recordings.

Test the loop without motion for a limited number of rounds:

```bash
python3 ~/pidog-coding/src/voice_control/06_active_voice_control.py \
  --max-rounds 3
```

After physically checking Buck's stand and clearing every leg and the tail,
start physical mode with:

```bash
python3 ~/pidog-coding/src/voice_control/06_active_voice_control.py \
  --execute --i-have-calibrated --on-stand
```

Current limitation: listening and movement are sequential. Buck cannot hear
`stop` while a short action is executing; it listens again only after that
action finishes. For that reason this lesson permits only bounded posture and
tail actions—not walking. Ctrl+C also cannot interrupt the underlying movement
call until that call returns.

## Planned command boundary

The first parser will recognize only a small set:

| Spoken intent | Internal action |
| --- | --- |
| "sit" / "sit down" | `sit` |
| "stand" / "stand up" | `stand` |
| "lie down" | `lie` |
| "wag your tail" | `wag_tail` |
| "stop" | `stop` |

Everything else maps to `unknown` and causes no movement.

## Official references

- [SunFounder: STT with Vosk (offline)](https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_stt_vosk.html)
- [SunFounder: TTS with Piper and OpenAI](https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_tts_piper_openai.html)
- [SunFounder: AI Voice Assistant Dog](https://docs.sunfounder.com/projects/pidog/en/latest/ai_interaction/python_ai_robot.html)
- [SunFounder PiDog source](https://github.com/sunfounder/pidog)

## Session observations

### 2026-10-22

- Started after the Zero 2 W Wi-Fi stability fix passed a five-minute
  continuous connection test.
- Confirmed the microphone and offline speech libraries before recording.
- No servos or PiDog motion objects were initialized during inventory.
- Recorded and analyzed a four-second microphone sample. The format was correct,
  the signal was usable, and no samples clipped.
- Added a one-sentence Vosk transcription lesson. The first run will download
  the small English model to Buck; subsequent runs operate offline.
- Initial live recognitions returned only `huh` and `ah`. Inspection showed the
  Robot HAT microphone capture control at 51% (0 dB), so it was raised to 75%
  (+12.2 dB) for a controlled retest.
- Changed the Vosk lesson to save the exact six-second input before
  transcribing it. This allows every failed recognition to be replayed and
  separates microphone diagnosis from recognizer diagnosis.
- With the microphone at 75%, the next sample measured -6.0 dBFS peak and
  -29.3 dBFS RMS with no clipping, and Vosk transcribed it successfully.
- Added the lesson 3 allowlist parser, interactive simulator, and automated
  tests. No motion API is connected yet.
- Refactored microphone/Vosk work into the reusable `speech_input.py` component.
- Added lesson 4's integrated voice-command preview. It passes the Vosk text to
  the allowlist parser but deliberately has no motion connection.
- Added lesson 5's one-shot guarded movement controller and a separate motion
  allowlist. Physical execution requires explicit execute, calibration, and
  stand confirmations and uses bounded speeds/repetitions.
- Added lesson 6's continuous listener. It accepts bare allowlisted commands,
  accepts `stop` to exit, reuses and resets one offline Vosk recognizer, and
  safely closes PiDog on exit.
- Kept the active loop limited to short posture and tail actions because its
  sequential design cannot listen while an action is running.
