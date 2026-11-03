"""Optional bounded SunFounder camera preview. No Pidog object, no locomotion."""
import argparse
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=int, default=30)
    parser.add_argument('--blue', action='store_true', help='Requires Vilib.color_detect API')
    args = parser.parse_args()
    if not 1 <= args.seconds <= 120:
        parser.error('Choose 1..120 seconds')
    from vilib import Vilib
    if args.blue and not callable(getattr(Vilib, 'color_detect', None)):
        parser.error('Installed Vilib lacks color_detect. Use plain preview and the saved-image labs.')
    try:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=False, web=True)
        if args.blue:
            Vilib.color_detect('blue')
        print('On the same network open http://YOUR_PI_IP:9000/mjpg . Ctrl+C stops.')
        end = time.monotonic()+args.seconds
        while time.monotonic() < end:
            if args.blue:
                p = Vilib.detect_obj_parameter
                print({k: p.get(k) for k in ('color_n','color_x','color_y','color_w','color_h')})
            time.sleep(.5)
    except KeyboardInterrupt:
        pass
    finally:
        Vilib.camera_close()


if __name__ == '__main__':
    main()
