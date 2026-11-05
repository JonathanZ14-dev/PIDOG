# Official sources and viewing guide

Reviewed November 3, 2026. Package code is an original teaching implementation. Source links establish camera APIs and reference examples, not a claim that this package has been tested on your physical PiDog.

| Source | Why open it | Activity |
| --- | --- | --- |
| [SunFounder camera module](https://docs.sunfounder.com/projects/pidog/en/latest/_shared/component/cpn_camera_module.html) | Hardware connection and listed camera specifications | Locate CSI; compare the listed module with your actual camera |
| [PiDog fun projects](https://docs.sunfounder.com/projects/pidog/en/latest/python/py_fun_project.html) | Official project index | Find visual projects and distinguish them from our stationary experiments |
| [Ball Track, with demonstration video](https://docs.sunfounder.com/projects/pidog/en/latest/python/py_13_ball_track.html) | Color observations connected to robot actions | Watch the embedded demonstration; identify perception, policy and motor calls; do not run it as a stationary diagnostic |
| [Face Track, with demonstration video](https://docs.sunfounder.com/projects/pidog/en/latest/python/py_7_face_track.html) | Another visual task and multimodal behavior | Watch the embedded demonstration; ask what is actually detected versus inferred |
| [Vilib color detection](https://docs.sunfounder.com/projects/vilib-rpi/en/latest/py_color_detection.html) | Named-color API, output fields and preview | Compare documented methods and coordinates with doctor output; this documentation may differ from installed versions |
| [Raspberry Pi camera software](https://www.raspberrypi.com/documentation/accessories/camera-software.html) | Modern camera stack and command-line utilities | Find camera enumeration and distinguish modern from legacy tools |
| [Picamera2 official source](https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py) | Configuration and capture API | Locate create_still_configuration, capture_image and close |
| [Picamera2 official image example](https://github.com/raspberrypi/picamera2/blob/main/examples/capture_image_full_res.py) | Image capture into memory | Compare the example's preview/display assumptions with our headless capture |
| [Picamera2 manual](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf) | Detailed configuration and image-format reference | Use when resolving a version-specific format or configuration question |
| [Python colorsys](https://docs.python.org/3/library/colorsys.html) | RGB/HSV conversion and value ranges | Check why our thresholds use fractions |
| [OpenCV HSV thresholding tutorial](https://docs.opencv.org/4.x/da/d97/tutorial_threshold_inRange.html) | A more optimized implementation of color masks | Compare concepts; do not copy numerical thresholds without checking color-space scale |
| [Google supervised classification](https://developers.google.com/machine-learning/crash-course/classification) | Learning vocabulary and classification | Optional deeper review after our tiny model |
| [Google dataset splitting](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets) | Train, validation and test distinctions | Plan grouped real-scene collection |

The SunFounder video links above point to official pages containing embedded demonstrations; they are not invented standalone video URLs. If the embedded player does not load, the page's code still supports the reading activity. No videos or online models are required for the offline experiments.

:::note source_review | Which source did we inspect? Which API or assumption did we verify against the installed robot? What remains different or unclear? | 5
