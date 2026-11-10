# What we can build next

Choose one extension after the core lesson. The 90-minute plan does not require finishing these. Preserve the current working code and test on saved images first.

## 1. Choose the region nearest the image center

This complete function can be added to perception.py. It changes the selection policy; it does not change the color mask or infer physical distance.

```python
def choose_nearest_center(stats, centers, width, min_pixels):
    """Return a qualifying component index, or None when no region qualifies."""
    # Keep only foreground components with enough matched pixels.
    eligible = [i for i in range(1, len(stats))
                if stats[i, cv2.CC_STAT_AREA] >= min_pixels]
    if not eligible:
        return None  # Explicit absence prevents indexing an imaginary component.
    # abs measures horizontal distance from the image center in pixels.
    return min(eligible, key=lambda i: abs(centers[i][0] - width / 2))
```

To integrate it, replace the `if candidates:` line and the `biggest = max(...)` line in analyze with these two lines (keep the existing area/box block indented underneath):

```python
biggest = choose_nearest_center(stats, centers, width, settings.min_pixels)
if biggest is not None:
```

Keep the later area check; it is redundant but correct. With this alternative, area_pixels remains zero when nothing qualifies, whereas the original implementation retains the largest below-threshold area. Update that output-contract description if you adopt the alternative. Test one large off-center card against a smaller central card, then hide both. A central image region is not automatically the closest real object.

## 2. Add a new color carefully

Add a new entry to RANGES and add the name to argparse's choices in run.py. Use OpenCV's tutorial to inspect HSV values from actual pixels first. Red crosses the hue wraparound, so a red detector generally needs two ranges combined with bitwise OR; simply adding one broad interval can select unwanted colors. Start with a single-interval color and evaluate it under two lighting conditions.

## 3. Add edges as a separate view

OpenCV's Canny tutorial shows how gradients become edge maps. Add a new function returning an edge image and save it separately. Compare a plain card, patterned card, and shadow. An edge is a change in image intensity, not an object identity or proof of collision risk. Keep the marker evidence dictionary separate from edge visualization.

## 4. Replace the rule with a learned detector

Keep the camera.read and reporting responsibilities. Replace the perception internals with preprocessing, pretrained-model inference, and output decoding. A detector can return multiple class labels, scores, and boxes, so define a new contract instead of calling a color area a confidence score. Replay the same saved PiDog pictures before trying repeated camera frames. A small Pi may need laptop inference on copied images.

## 5. Connect observations to sonar later

Combine a timestamped image observation with a timestamped range reading only after considering camera direction, sonar coverage, and time alignment. The sonar may see a different surface from the colored component. Begin by logging both, not by assigning the sonar distance to every detected object. This prepares the vision-only / sonar-only / combined obstacle-course comparison.

## Official tutorials and videos

Links checked November 10, 2026. These are references for extending this original teaching code; their interfaces may differ from our wrapper.

- [OpenCV: Changing Colorspaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html): read cvtColor and inRange; compare its BGR input with our explicit camera conversion. Its webcam example is not a drop-in Pi CSI driver.
- [OpenCV: Morphological Transformations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html): inspect opening before trying --clean.
- [OpenCV: Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html): optional edge-view project.
- [Raspberry Pi Picamera2 manual](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf): camera configuration and capture reference.
- [SunFounder PiDog Face Track](https://docs.sunfounder.com/projects/pidog/en/latest/python/py_7_face_track.html): official embedded demonstration and Vilib code. Watch the demonstration and identify sensing versus action. The complete example moves the head/body and activates other hardware; it is not part of today's stationary code.
- [3Blue1Brown: But what is a neural network?](https://www.3blue1brown.com/lessons/neural-networks/): video follow-up connecting pixels to learned features. Use a short selected segment, not the whole video inside the 90 minutes.
- [OpenCV Python course repository and chapter links](https://github.com/jasmcaus/opencv-course): optional guided Python video practice on reading images, color spaces, and drawing. Compare tutorial code to our modules rather than replacing the working Pi environment.
