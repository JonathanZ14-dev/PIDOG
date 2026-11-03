"""Capture ONE stationary image. Does not import PiDog or command any servo."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import time
from .core import Frame
from .files import save_frame, save_svg


class CameraSource:
    """Own one Picamera2 camera; factory injection permits cleanup tests."""
    def __init__(self, factory=None):
        if factory is None:
            from picamera2 import Picamera2
            factory = Picamera2
        self.camera = factory()

    def capture(self):
        """Configure, warm up, get an RGB PIL image; always close the device."""
        try:
            config = self.camera.create_still_configuration(main={'size': (320, 240)}, queue=False)
            self.camera.configure(config)
            self.camera.start()
            time.sleep(2)
            image = self.camera.capture_image('main').convert('RGB')
            # Explicitly choose a small analysis grid for transparent Python loops.
            image = image.resize((160, 120))
            frame = Frame(image.width, image.height, [list(p) for p in image.getdata()])
            return frame, {'source': 'Picamera2 capture_image; PIL RGB; resized 320x240 to 160x120',
                           'received_utc': datetime.now(timezone.utc).isoformat(),
                           'note': 'Receive time, not exposure time; offline analysis only'}
        finally:
            self.camera.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, help='New output directory, e.g. captures/blue-center-01')
    args = parser.parse_args()
    folder = Path(args.out)
    folder.mkdir(parents=True, exist_ok=False)  # Fail BEFORE opening camera on duplicate run name.
    frame, metadata = CameraSource().capture()
    save_frame(frame, folder/'frame.json', metadata)
    save_svg(frame, folder/'frame.svg')
    print('Saved', folder/'frame.json', 'and frame.svg. No motion commands were sent.')


if __name__ == '__main__':
    main()
