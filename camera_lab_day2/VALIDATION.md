# Validation record — November 3, 2026

## Completed

- 19 Python reference unit tests passed on Python 3.9.6 without Picamera2, Pillow, NumPy, OpenCV or PiDog installed on the authoring computer.
- Tests cover pixel validation, coordinates, HSV, color masks, threshold equality, darkness handling, ROI partitioning, bounding boxes, file round-trip, overwrite prevention, camera cleanup on success/failure, supervised-model errors, scene leakage and edge features.
- The grayscale/edge command generated SVGs successfully.
- Both browser JavaScript files passed syntax checking. Eight independent assertions checked the browser HSV/color/status calculations.

- All nine HTML documents passed duplicate-ID and local-link checks. All included SVGs parsed as XML.

## Limits

No PiDog was connected. Live camera initialization, image quality, camera-model compatibility, Vilib streaming and installed-library behavior remain unverified on your robot. Camera ownership and cleanup were tested with fakes, which do not prove hardware behavior. The provided doctor and Quick Start are the on-device acceptance procedure.

An isolated headless browser could not launch in the authoring environment. Notes persistence, import/export, image upload, visual layout and print rendering have therefore not been exercised in a real browser. JavaScript syntax and pure-function checks do not establish full browser behavior. Before class, type a sample note, export/restore JSON, inspect a fixture and test Print/PDF. Keep exported backups even if local autosave appears to work.

No program in the capture/perception pipeline sends motor commands. The optional official examples linked for reading can move PiDog; they are explicitly separated from this stationary lab.

Student edition: instructor materials, exercise implementations and precomputed example reports have been excluded. The exercise checker loads only exercises/student.py.
