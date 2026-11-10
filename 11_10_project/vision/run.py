"""Connect camera -> perception -> reports. Run from the student folder with -m."""
import argparse  # Converts command-line options into Python values.
from contextlib import nullcontext  # Harmless with-block when replay needs no camera.
from dataclasses import asdict  # Settings object -> dictionary for JSON.
from datetime import datetime, timezone
import json  # Portable text format for dictionaries and lists.
from pathlib import Path  # Paths with useful methods instead of manual slashes.
import time
import cv2
from .camera import Camera  # Leading dot means another module in this package.
from .perception import Settings, analyze, demo_image


def save_image(path, pixels):
    """Finish writing before replacing a displayed image."""
    temp = path.with_name("tmp-" + path.name)
    if not cv2.imwrite(str(temp), pixels):  # OpenCV expects a filename string.
        raise OSError(f"Could not save {path}")
    temp.replace(path)  # Rename a complete file in the same directory.


def write_page(folder):
    """HTML/JavaScript display saved results; the browser does not open the camera."""
    # A triple-quoted string holds a multi-line document. No extra web library needed.
    page = '''<!doctype html><html lang="en"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PiDog observations</title><style>body{font:18px system-ui;margin:24px;background:#eef5f2;color:#143f43}img{width:min(100%,640px);display:block;margin-bottom:20px}pre{white-space:pre-wrap}</style>
<h1>PiDog observations</h1><p>Latest saved observation, not live video. Distance is unknown. No motor commands. Check the timestamp: refresh continues after capture ends. Images and JSON can briefly come from adjacent frames while files update.</p>
<h2>Original</h2><img id="original" alt="Original"><h2>Color mask</h2><img id="mask" alt="Mask"><h2>Annotated</h2><img id="annotated" alt="Annotated"><pre id="record"></pre>
<script>async function update(){const q=Date.now();for(const n of ['original','mask','annotated'])document.getElementById(n).src=n+'.png?t='+q;
try{const r=await fetch('latest.json?t='+q);document.getElementById('record').textContent=JSON.stringify(await r.json(),null,2)}catch{document.getElementById('record').textContent='Open latest.json separately if viewing from a file.'}}update();setInterval(update,3000);</script></html>'''
    (folder / "index.html").write_text(page, encoding="utf-8")


def main():
    """Read settings, own the camera once, process a bounded sequence, then close."""
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)  # Choose exactly one.
    source.add_argument("--camera", action="store_true")  # A Boolean flag.
    source.add_argument("--image", type=Path)  # Repeatable saved-image experiment.
    source.add_argument("--demo", action="store_true")  # No camera needed.
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--color", choices=["blue", "green"], default="blue")
    parser.add_argument("--min-pixels", type=int, default=300)
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--frames", type=int, default=1)
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()  # --help is provided automatically.
    if not 1 <= args.frames <= 600 or not 0 <= args.interval <= 10:
        parser.error("Use 1..600 frames and 0..10 seconds between observations")
    if args.image and args.frames != 1:
        parser.error("Saved-image replay uses --frames 1")
    if args.min_pixels < 1:
        parser.error("min-pixels must be positive")
    settings = Settings(args.color, args.min_pixels, args.clean)
    args.out.mkdir(parents=True, exist_ok=False)  # Never erase an earlier trial.
    owner = Camera() if args.camera else nullcontext(None)  # Conditional expression.
    with owner as camera:
        for number in range(args.frames):  # Finite loop: 0 through frames-1.
            if args.camera:
                frame = camera.read()
            elif args.image:
                frame = cv2.imread(str(args.image))  # imread already returns BGR.
                if frame is None:
                    raise ValueError(f"Could not read image: {args.image}")
            else:
                frame = demo_image(["left", "center", "right"][number % 3])
                # Modulo cycles through three positions in synthetic mode.
            start = time.perf_counter()  # Monotonic clock for measuring duration.
            annotated, mask, record = analyze(frame, settings)
            record["processing_ms"] = round(1000 * (time.perf_counter() - start), 2)
            record["frame"] = number
            record["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
            record["source"] = "camera" if args.camera else ("image" if args.image else "synthetic")
            record["settings"] = asdict(settings)
            save_image(args.out / "original.png", frame)
            save_image(args.out / "mask.png", mask)
            save_image(args.out / "annotated.png", annotated)
            # Keep latest images only to limit SD-card writes; retain all text records.
            temporary = args.out / "tmp-latest.json"
            temporary.write_text(json.dumps(record, indent=2), encoding="utf-8")
            temporary.replace(args.out / "latest.json")
            with (args.out / "history.jsonl").open("a", encoding="utf-8") as log:
                log.write(json.dumps(record) + "\n")  # One JSON dictionary per line.
            if number == 0:
                write_page(args.out)  # Viewer appears after its first images exist.
            print(f"{number}: {record['image_region']} | area {record['area_pixels']}")
            if number + 1 < args.frames:
                time.sleep(args.interval)  # Delay PLUS work; not a guaranteed frame rate.


if __name__ == "__main__":
    # Importing this module defines functions. Running it calls main exactly once.
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped; camera context closed. Completed observations are saved.")
