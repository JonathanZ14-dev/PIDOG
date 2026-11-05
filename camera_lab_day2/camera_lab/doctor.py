"""Report interpreter and installed camera APIs WITHOUT opening any devices."""
import importlib
import importlib.metadata
import platform
import sys


def main():
    print('Python:', sys.version.split()[0], 'Executable:', sys.executable, 'System:', platform.platform())
    for name in ('picamera2', 'PIL', 'vilib', 'pidog'):
        try:
            m = importlib.import_module(name)
            try:
                version = importlib.metadata.version('Pillow' if name == 'PIL' else name)
            except importlib.metadata.PackageNotFoundError:
                version = getattr(m, '__version__', 'version unavailable')
            print(name, version, getattr(m, '__file__', '?'))
            if name == 'picamera2':
                for method in ('create_still_configuration','capture_image','close'):
                    print(' ', method, hasattr(m.Picamera2, method))
            if name == 'vilib':
                for method in ('camera_start','camera_close','display','color_detect','color_detect_switch'):
                    print(' ', method, hasattr(m.Vilib, method))
        except Exception as error:
            print(name, 'NOT READY:', type(error).__name__, str(error))
    print('No camera or PiDog object constructed. Import success does not prove capture works.')


if __name__ == '__main__':
    main()
