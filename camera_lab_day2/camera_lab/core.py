"""Pure perception: explicit RGB pixels -> mask -> regional evidence."""
from dataclasses import dataclass
import colorsys
import math


@dataclass
class Frame:
    """Row-major RGB image. pixels[y * width + x] is (R,G,B), each 0..255."""
    width: int
    height: int
    pixels: list

    def __post_init__(self):
        if type(self.width) is not int or type(self.height) is not int or self.width < 3 or self.height < 2:
            raise ValueError('Need integer width >= 3 and height >= 2')
        if len(self.pixels) != self.width * self.height:
            raise ValueError('Pixel count must equal width times height')
        if any(len(p) != 3 or any(type(v) is not int or not 0 <= v <= 255 for v in p) for p in self.pixels):
            raise ValueError('Pixels must be RGB integer triples in 0..255')

    def pixel(self, x, y):
        """Return one RGB triple; reject coordinates outside the image."""
        if type(x) is not int or type(y) is not int or not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError('Pixel coordinate outside frame')
        return tuple(self.pixels[y * self.width + x])


@dataclass(frozen=True)
class Settings:
    """HSV uses fractions, NOT OpenCV's 8-bit HSV scale. Defaults need calibration."""
    hue_low: float = 0.52
    hue_high: float = 0.72
    min_saturation: float = 0.40
    min_value: float = 0.20
    min_mean_value: float = 0.12
    area_threshold: float = 0.08

    def __post_init__(self):
        for value in vars(self).values():
            if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError('Settings must be finite fractions in 0..1')
        if self.hue_low > self.hue_high or self.area_threshold <= 0:
            raise ValueError('Use ordered hue bounds and a positive area threshold')


def rgb_to_hsv(rgb):
    """Return hue, saturation, value in 0..1 from a validated RGB triple."""
    return colorsys.rgb_to_hsv(*(v / 255 for v in rgb))


def is_blue(rgb, settings):
    """A Boolean color rule; makes no claim about object identity or distance."""
    h, s, v = rgb_to_hsv(rgb)
    return settings.hue_low <= h <= settings.hue_high and s >= settings.min_saturation and v >= settings.min_value


def blue_mask(frame, settings):
    """Return one Boolean per pixel, retaining row-major image order."""
    return [is_blue(p, settings) for p in frame.pixels]


def region_report(frame, mask, box, settings):
    """Summarize [x0,y0,x1,y1), with exclusive upper bounds, in pixel units."""
    x0, y0, x1, y1 = box
    if len(mask) != len(frame.pixels) or not (0 <= x0 < x1 <= frame.width and 0 <= y0 < y1 <= frame.height):
        raise ValueError('Invalid mask size or ROI')
    selected = []
    value_sum = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            i = y * frame.width + x
            value_sum += max(frame.pixels[i]) / 255
            if mask[i]:
                selected.append((x, y))
    count = len(selected)
    area = (x1-x0) * (y1-y0)
    ratio = count / area
    mean_value = value_sum / area
    status = 'unknown' if mean_value < settings.min_mean_value else ('marker_present' if ratio >= settings.area_threshold else 'marker_absent')
    bbox = None
    centroid = None
    if selected:
        xs, ys = zip(*selected)
        bbox = [min(xs), min(ys), max(xs)+1, max(ys)+1]
        centroid = [sum(xs)/count, sum(ys)/count]
    return dict(roi=list(box), count=count, area=area, blue_ratio=ratio, mean_value=mean_value,
                status=status, bbox=bbox, centroid=centroid)


def analyze(frame, settings):
    """Return full-frame and lower-half left/center/right visual evidence."""
    mask = blue_mask(frame, settings)
    edges = [0, frame.width//3, 2*frame.width//3, frame.width]
    zones = {name: region_report(frame, mask, (edges[i], frame.height//2, edges[i+1], frame.height), settings)
             for i, name in enumerate(('left', 'center', 'right'))}
    return {'width': frame.width, 'height': frame.height,
            'full': region_report(frame, mask, (0, 0, frame.width, frame.height), settings), 'zones': zones}


def suggest(report):
    """A non-actuating message. Absence of our marker never proves free space."""
    status = report['zones']['center']['status']
    if status == 'unknown':
        return 'STOP_AND_RECHECK_IMAGE'
    if status == 'marker_present':
        return 'CENTER_MARKER_DETECTED_REVIEW'
    return 'NO_CENTER_MARKER_NO_CLEARANCE_CLAIM'
