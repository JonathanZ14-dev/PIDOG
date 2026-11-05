"""Analyze a saved image; no camera and no motors are opened."""
import argparse
import json
from pathlib import Path
from time import perf_counter
from .core import Settings, analyze, blue_mask, suggest
from .files import load_frame, save_svg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image')
    parser.add_argument('--out', required=True, help='New output directory')
    parser.add_argument('--threshold', type=float, default=.08)
    parser.add_argument('--hue-low', type=float, default=.52)
    parser.add_argument('--hue-high', type=float, default=.72)
    args = parser.parse_args()
    settings = Settings(area_threshold=args.threshold, hue_low=args.hue_low, hue_high=args.hue_high)
    frame, metadata = load_frame(args.image)
    start = perf_counter()
    report = analyze(frame, settings)
    report['analysis_seconds'] = perf_counter()-start
    report['message'] = suggest(report)
    report['settings'] = vars(settings)
    report['input_metadata'] = metadata
    folder = Path(args.out)
    folder.mkdir(parents=True, exist_ok=False)
    (folder/'report.json').write_text(json.dumps(report, indent=2))
    save_svg(frame, folder/'image.svg', report=report)
    save_svg(frame, folder/'mask.svg', mask=blue_mask(frame, settings))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
