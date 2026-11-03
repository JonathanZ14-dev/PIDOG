# Definitions, contracts and code map

Use this as a reference, then write your own explanations. A definition is learned when you can use it to predict or explain an observation.

| Term | Meaning here | Concrete example |
| --- | --- | --- |
| Sensor | Device converting a physical signal into measurable values | Camera detects light; ultrasonic system detects echoes |
| CSI | Camera Serial Interface connecting camera and Pi | Ribbon connection carrying image data |
| ISP | Image signal processing that turns sensor measurements into useful images | Demosaicing and color processing |
| Pixel / channel | Sample location / one component of its stored value | Pixel (20,30) has R,G,B channels |
| RGB | Red, green and blue image representation | (20,60,220) in our fixture |
| HSV | Hue, saturation and value representation | colorsys uses 0..1 for all three |
| Resolution | Image width and height in pixels | 160×120 analysis frame |
| Exposure / gain | Light collection duration / signal amplification | Brighter frame with possible blur or noise tradeoffs |
| White balance | Adjustment of relative color response | A white sheet may look different under warm light |
| Mask | Per-pixel selection map | White pixels pass our blue rule |
| ROI | Chosen image region | Bottom center third |
| Threshold | Boundary used in a decision | Fraction >= .08 means marker_present when quality passes |
| Bounding box | Axis-aligned rectangle around selected pixels | [x0,y0,x1,y1), with exclusive upper bounds |
| Centroid | Mean location of selected pixels | Can fall between two disconnected patches |
| Feature | Numeric property used for inference | Blue fraction |
| Semantics | Meaning assigned to image content | Calling a region a box rather than a blue patch |
| Label / ground truth | Target annotation / independent reference for evaluation | Human records whether an obstacle was placed |
| Model / parameter | Mapping used for prediction / adjustable value | A threshold classifier / its threshold |
| Training / inference | Fitting parameters / using fitted parameters | Learn .11, then classify a new fraction |
| Loss | Measure of prediction error used during fitting | Number of mistakes in the training rows |
| Generalization | Performance on new examples | Testing on a different layout or appearance |
| Distribution shift | New data differs from development data | Blue training boxes, red test obstacle |
| Leakage | Evaluation information contaminates development | Splitting adjacent frames of one scene across train and test |
| Confidence / calibration | Model certainty score / agreement of such scores with outcomes | Our area ratio is NOT a confidence score |
| Frame rate / latency | Frames per second / delay until evidence is used | A 30 fps stream can still be delayed |
| Pure function / side effect | Output depends on input values / effect beyond return value | analyze versus capture or file writing |
| Class / instance | Definition of data and behavior / one object of that type | Frame versus a particular captured Frame |
| Method / self | Function bound to an object / that instance | frame.pixel(4,5) |
| Wrapper | A simpler boundary around another API | CameraSource around Picamera2 |
| Module / package | Importable code unit / organized collection of modules | core.py / camera_lab |
| Exception / finally | Failure signal / cleanup block run as control exits | Camera close after capture failure |
| Contract | Explicit promise about inputs, outputs and effects | RGB triples 0..255 in row-major order |

:::note glossary_own | Pick six terms that were unfamiliar. Define them in your words and attach one image, code line or experiment that illustrates each. | 10

## Suggested reading order

Read exercises/student.py, then core.py, capture.py, files.py, analyze.py, and learn.py. The doctor and optional Vilib preview are support tools. You do not need to rewrite boilerplate before you can reason about perception. Keep acquisition, interpretation and future action in separate modules.

## Every custom callable explained

| Callable | Input → output | Effects, assumptions and failure |
| --- | --- | --- |
| Frame generated constructor | width, height, pixels → Frame instance | Dataclass stores image values, then validation runs |
| Frame.__post_init__ | Stored fields → None | Rejects undersized/noninteger dimensions, count mismatch and invalid RGB triples |
| Frame.pixel | Integer x,y → RGB tuple | Pure lookup; rejects out-of-bounds coordinates |
| Settings generated constructor / __post_init__ | Fraction parameters → immutable Settings | Rejects invalid fractions, reversed hue bounds and nonpositive area threshold |
| rgb_to_hsv | Validated RGB triple → H,S,V tuple | Pure; uses standard-library colorsys; all output channels 0..1 |
| is_blue | RGB and Settings → Boolean | Pure; inclusive hue, saturation and value comparisons |
| blue_mask | Frame and Settings → Boolean list | Pure; same pixel order as Frame |
| region_report | Frame, mask, integer ROI, Settings → dictionary | Pure; count, mean value, ratio, status, union box and centroid; rejects mask-size/ROI errors |
| analyze | Frame and Settings → evidence dictionary | Pure; full image and three lower-half regions; no device access |
| suggest | Analysis report → message string | Pure; does not output a motor command or claim free space |
| save_frame | Frame, new path, metadata → None | Creates parent directory and writes JSON; refuses an existing file |
| load_frame | JSON path → (Frame, metadata) | Reads disk and validates image; bad JSON or fields raise |
| save_svg | Frame, path, optional mask/report → None | Writes SVG image; helper color_at obtains the current row's color, adjacent equal colors merge into one rectangle |
| CameraSource.__init__ | Optional camera factory → owned camera instance | Imports Picamera2 only when needed; constructs camera; constructor errors propagate |
| CameraSource.capture | Owned camera → (Frame, metadata) | Configure/start/warm-up/capture/convert/resize; always closes camera in finally after construction |
| capture.main | CLI --out → files and printed path | Requires new folder before opening camera; capture errors propagate |
| analyze.main | Input path and thresholds → report and two SVGs | Validates settings, measures analysis duration, creates new results folder; never opens camera |
| doctor.main | No arguments → printed diagnostic | Imports installed modules but does not construct camera or robot objects; reports import failures |
| vilib_preview.main | Duration and optional --blue → bounded stream and printed readings | Opens Vilib camera/network preview; closes in finally; Ctrl+C supported |
| load_rows | CSV path → validated example list | Reads disk, converts numeric fields, rejects scene leakage and missing splits |
| evaluate | Examples and threshold → TP,TN,FP,FN,n,accuracy | Pure; positive target is obstacle presence; empty accuracy is None |
| fit_threshold | Nonempty two-class training examples → threshold | Pure; builds candidates, nested score counts errors and implements tie-break; no validation/test access |
| learn.main | CSV CLI argument → printed model/evaluation | Loads rows, fits only train split, reports three split results |
| check_exercises.main | --student → pass/fail output and exit status | Imports your exercise module; tests values and errors; unfinished TODOs fail intentionally |
| flat_index | Valid x,y,width → flat list index | Student pure function; preconditions specified in docstring |
| marker_fraction | Count, area → fraction | Student pure function; invalid counts/zero area raise ValueError |
| marker_status | Ratio, mean value, threshold → marker status | Student pure function; quality check takes priority |
| fuse_evidence | Two already mapped statuses → fused status | Student pure function; valid inputs are clear, blocked and unknown |

The test-only helper solid creates a 6×4 single-color Frame. Test methods assert the contract named by their test name. Mock camera methods imitate the external API; they verify ownership and call behavior, not sensor operation. The test suite does not require camera packages.

## Library methods we call

Picamera2 creates the camera owner; create_still_configuration describes the requested output; configure applies it; start begins acquisition; capture_image returns a Pillow image; convert('RGB') makes channel meaning explicit; resize chooses our small analysis grid; getdata returns pixels in image order; close releases the camera. These operations are called by our wrapper, not reimplemented.

Vilib.camera_start starts its camera service; display enables viewing; color_detect chooses a named color when supported; detect_obj_parameter exposes measurements; camera_close releases its camera. Check installed method availability. A package name or version alone does not prove all methods behave like today's online documentation.

The standard-library modules also have jobs: argparse handles command-line options; pathlib represents paths; json and csv serialize data; colorsys converts color representations; dataclasses generates data-class boilerplate; time measures intervals or waits; unittest checks behavior. None provides object semantics automatically.

## Write a new function's contract before coding

:::note new_contract | Function name and purpose; inputs/types/units; returned type/meaning; side effects; invalid-input behavior; one example; one boundary test; one failure test. | 10

A good next wrapper should isolate a real responsibility, not just rename every line. Prefer a small pure helper for a calculation and a resource-owning class when state/lifetime actually needs to be managed. No decorator or inheritance is required in this project.
