"""File boundaries and inspectable SVG images; standard library only."""
import json
from pathlib import Path
from .core import Frame


def save_frame(frame, path, metadata=None):
    """Write RGB JSON with optional capture metadata; refuses overwrite."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        json.dump(dict(width=frame.width, height=frame.height, pixels=frame.pixels, metadata=metadata or {}), f)


def load_frame(path):
    """Read validated JSON into a Frame, returning (frame, metadata)."""
    data = json.loads(Path(path).read_text())
    return Frame(data['width'], data['height'], data['pixels']), data.get('metadata', {})


def save_svg(frame, path, mask=None, report=None):
    """Write a pixel-faithful view (or binary mask) plus optional region boxes."""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {frame.width} {frame.height}" width="800" role="img"><title>RGB view or binary mask; pixel coordinates</title>']
    for y in range(frame.height):
        # Merge adjacent same-color pixels to keep the file compact.
        x = 0
        while x < frame.width:
            def color_at(xx):
                i = y*frame.width+xx
                return ('white' if mask[i] else 'black') if mask is not None else 'rgb(%s,%s,%s)' % tuple(frame.pixels[i])
            color = color_at(x)
            end = x+1
            while end < frame.width and color_at(end) == color:
                end += 1
            parts.append(f'<rect x="{x}" y="{y}" width="{end-x}" height="1" fill="{color}"/>')
            x = end
    if report:
        for zone in report['zones'].values():
            x0,y0,x1,y1 = zone['roi']
            parts.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="#ffff00" stroke-width="0.7"/>')
            if zone['bbox']:
                a,b,c,d = zone['bbox']
                parts.append(f'<rect x="{a}" y="{b}" width="{c-a}" height="{d-b}" fill="none" stroke="#ff00ff" stroke-width="0.7"/>')
    parts.append('</svg>')
    Path(path).write_text(''.join(parts))
