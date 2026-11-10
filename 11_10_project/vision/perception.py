"""Image -> evidence. No camera ownership, file writing, or motor commands."""
from dataclasses import dataclass  # Generates an initializer for a data container.
import cv2
import numpy as np

# Dict maps color names to lower/upper HSV tuples. OpenCV uint8 H:0..179, S/V:0..255.
# These are starting ranges to investigate, not universal color definitions.
RANGES = {"blue": ((100, 80, 50), (135, 255, 255)),
          "green": ((40, 80, 50), (85, 255, 255))}


@dataclass
class Settings:
    """Experiment parameters are chosen by us; they are not learned weights."""
    color: str = "blue"  # Annotation describes intent; value supplies a default.
    min_pixels: int = 300  # Minimum area of the largest connected colored region.
    clean: bool = False  # Optional removal of speckles using morphology.

    def __post_init__(self):
        # dataclass calls this after assigning fields. Reject invalid settings early.
        if self.color not in RANGES:
            raise ValueError("Choose blue or green")
        if type(self.min_pixels) is not int or self.min_pixels < 1:
            raise ValueError("min_pixels must be a positive integer")


def region_name(center_x, width):
    """Describe an IMAGE position, not a safe walking direction."""
    if center_x < width / 3:
        return "left"
    elif center_x < 2 * width / 3:
        return "center"
    else:
        return "right"


def analyze(bgr, settings):
    """Return (annotated_image, mask, evidence_dict) from a uint8 BGR array.

    This is a hand-written color rule, not semantic object recognition.
    """
    if bgr is None or bgr.dtype != np.uint8 or bgr.ndim != 3 or bgr.shape[2] != 3:
        raise ValueError("Expected a uint8 BGR image with three channels")
    height, width = bgr.shape[:2]  # Slice the first two dimensions; unpack the pair.
    if height == 0 or width == 0:
        raise ValueError("Image must not be empty")
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)  # Represent color differently.
    lower, upper = RANGES[settings.color]  # Dictionary lookup, then tuple unpacking.
    mask = cv2.inRange(hsv, np.array(lower, dtype=np.uint8),
                       np.array(upper, dtype=np.uint8))
    # Mask pixels: 255 matched all bounds; 0 did not. This is not confidence.
    if settings.clean:
        kernel = np.ones((3, 3), dtype=np.uint8)  # Neighborhood for the operation.
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # Opening removes speckles but may also remove thin real features.
    count, labels, stats, centers = cv2.connectedComponentsWithStats(mask, connectivity=8)
    # Connected components group touching foreground pixels. Label 0 is background.
    candidates = list(range(1, count))  # [] if no foreground regions exist.
    evidence = {"color": settings.color, "found": False, "image_region": "unknown",
                "area_pixels": 0, "box": None, "center": None,
                "width": width, "height": height, "distance_cm": None}
    # None means unknown; it is not zero distance or proof that a path is clear.
    annotated = bgr.copy()  # Preserve the original pixels for comparison.
    if candidates:  # Empty lists are false; nonempty lists are true.
        # lambda defines a short ranking function; max selects the largest region.
        biggest = max(candidates, key=lambda i: stats[i, cv2.CC_STAT_AREA])
        area = int(stats[biggest, cv2.CC_STAT_AREA])  # NumPy int -> JSON-friendly int.
        evidence["area_pixels"] = area  # Keep measurement even below the threshold.
        if area >= settings.min_pixels:  # Equality is included.
            x, y, box_w, box_h, _ = [int(v) for v in stats[biggest]]
            cx, cy = [float(v) for v in centers[biggest]]  # Foreground-pixel centroid.
            evidence.update({"found": True, "image_region": region_name(cx, width),
                             "box": [x, y, x + box_w, y + box_h], "center": [cx, cy]})
            # Stored upper box coordinates are exclusive; drawing endpoints aren't.
            cv2.rectangle(annotated, (x, y), (x + box_w - 1, y + box_h - 1),
                          (0, 255, 255), 2)
            cv2.circle(annotated, (round(cx), round(cy)), 4, (0, 0, 255), -1)
    message = f"{settings.color}: {evidence['image_region']} | area={evidence['area_pixels']}"
    cv2.putText(annotated, message, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                .6, (0, 255, 255), 2)
    return annotated, mask, evidence  # A tuple lets the caller unpack three results.


def demo_image(position="center"):
    """Known synthetic scene for a repeatable test, not a PiDog photograph."""
    frame = np.full((240, 320, 3), 190, dtype=np.uint8)  # Gray BGR canvas.
    x = {"left": 20, "center": 140, "right": 260}[position]
    frame[90:150, x:x + 30] = (255, 0, 0)  # Rows then columns; blue in BGR.
    return frame
