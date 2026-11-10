"""Camera wrapper: owns one Pi CSI camera and returns OpenCV BGR images."""
import time  # Standard-library module for the warm-up delay.


class Camera:
    """A class is a blueprint; each instance stores its own device in self."""

    def __init__(self):
        # Delayed import lets saved-image replay work without Pi camera libraries.
        from picamera2 import Picamera2
        self.device = Picamera2()  # Create the hardware-facing library object.

    def __enter__(self):
        # Python calls this when entering `with Camera() as camera:`.
        try:
            config = self.device.create_still_configuration(
                main={"size": (640, 480)}, queue=False  # Dict containing a tuple.
            )
            self.device.configure(config)
            self.device.start()
            time.sleep(2)  # Allow exposure and white balance to begin settling.
            return self  # The variable after `as` refers to this instance.
        except BaseException:
            # __exit__ is not called if __enter__ fails; close here as well.
            self.device.close()
            raise  # Keep the original error, including an interrupted startup.

    def read(self):
        """Return uint8 pixels with shape (height, width, 3), in BGR order."""
        import cv2  # OpenCV handles image conversions.
        import numpy as np  # NumPy stores arrays of numbers.
        rgb = self.device.capture_image("main").convert("RGB")
        # Explicit Pillow RGB conversion avoids guessing camera buffer order.
        return cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2BGR)

    def __exit__(self, error_type, error_value, traceback):
        # These arguments describe an exception, if any. None does not suppress it.
        self.device.close()  # Also runs when the with-block raises an exception.
