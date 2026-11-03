# Deeper reference · Processing, features and learned meaning

This appendix supplies explanations to revisit during either session, plus an optional 15–25 minute extension if the core work finishes early. It does not add required work to the two-hour schedules.

## Processing choices change the evidence

A camera image is already processed before our Python code sees it. Our code then chooses an analysis resolution and color representation. Each transformation solves a problem and can lose or change information.

| Operation | What changes | Useful for | What to watch |
| --- | --- | --- | --- |
| Crop | Keep only a chosen spatial region | Focus on relevant parts of a scene | An obstacle outside the crop disappears from the algorithm |
| Resize | Resample onto a new pixel grid | Smaller computation or model input size | Small features can disappear; interpolated colors change masks |
| Normalize | Map values onto a specified scale | Consistent numerical inputs | 0..255 versus 0..1 must match thresholds/model training |
| Grayscale | Combine RGB channels into one value | Inspect intensity structure | Different colors can become indistinguishable |
| Blur | Mix neighboring values | Reduce small fluctuations | Thin boundaries and small obstacles may disappear |
| Gradient / edge filter | Measure local intensity change | Find structure and boundaries | Shadows and texture also create edges |
| Threshold | Convert a value to a discrete decision | Build a mask or classifier | Boundary and equality behavior matter |

Our capture wrapper explicitly converts to RGB and resizes to 160×120. That makes the examples fast enough for transparent Python loops. It does not preserve every detail of the sensor image. Resizing in a browser can use a different interpolation path than Pillow; use the Python report as the experiment record rather than expecting every uploaded-browser pixel to match exactly.

## Run an inspectable feature experiment

```sh
python3 -m camera_lab.features data/blue-center.json --out results/feature-blue-01
python3 -m camera_lab.features data/red-center.json --out results/feature-red-01
```

Open gray.svg and edges.svg from each folder. A flat region has little internal edge response; its boundary changes intensity and produces a response. The red patch can produce edges even though the blue mask ignores it. Edges therefore provide different information, but they still do not say whether the region is a physical obstacle.

The grayscale function uses a weighted combination of encoded RGB values. It is useful for display and teaching, not a calibrated physical light measurement. The sobel function slides two 3×3 kernels across the grayscale image. It multiplies neighboring values by kernel weights and adds them. One kernel responds to horizontal intensity change, the other to vertical change. We combine absolute responses into a display strength. The outer one-pixel border is left black because a full neighborhood is unavailable there.

```text
Horizontal-change kernel:      Vertical-change kernel:
-1  0  1                      -1 -2 -1
-2  0  2                       0  0  0
-1  0  1                       1  2  1
```

These are numerical arrays, not a diagram of scene geometry. In a constant neighborhood, positive and negative terms cancel. Across a brightness boundary, they may not. Ask the student to calculate a response for a 3×3 patch whose left column is 0 and right column is 100. For the horizontal kernel, the response is 100 + 200 + 100 = 400 when those columns are constant; the middle column is multiplied by zero.

:::note feature_test | Compare original, grayscale, edge map and blue mask. Which structures survive? Which disappear? Explain one false edge, such as a shadow, that is not a physical obstacle boundary. | 6

## From fixed filters to learned representations

Our Sobel weights are chosen by people. In a convolutional neural network, many filter weights can be learned from training data. Each filter combines local input values into a feature map. Nonlinear operations and multiple layers can combine these responses into more complex patterns. Other architectures, such as vision transformers, use patch representations and attention to mix information across the image. Neither architecture comes with a guarantee that a learned pattern represents the physical concept we care about.

A useful conceptual chain is: image → representation → task-specific prediction → evaluation against independent labels. A classifier may output one label for the image. A detector needs spatial outputs too. A depth model needs supervision or assumptions that connect visual cues to geometry. Changing the final label name to “obstacle” does not automatically change the information the model learned to use.

**Embedding:** a numeric vector representing an image, patch or object for a particular model. Similar vectors can reflect useful similarities learned during training, but their meaning depends on that training. A vector is not automatically a complete map of the physical scene.

**Pretraining:** learning from a broad dataset before a particular application. **Fine-tuning:** adjusting an already trained model using task-specific data. **Inference:** using its current parameters without training. A pretrained detector may save collection effort, but it still needs evaluation on your camera, lighting, object sizes and course. We are not installing or training a neural detector in the four-hour core lesson.

## Why labels and counterexamples matter

If every obstacle in training is blue and every empty scene is gray, a model can achieve perfect training accuracy by using color alone. It may never need to represent object height, depth or traversability. The toy learner makes this shortcut visible because it has only one feature. Larger models can also exploit shortcuts, though they may be harder to diagnose.

Design examples that separate correlated properties: blue obstacle versus blue non-obstacle; red obstacle versus red non-obstacle; the same object near and far; a real object versus its photograph. Keep independent scene groups out of development. Ask what would change your belief that the model learned the intended task.

:::note learned_representation | Compare a fixed color rule, a learned scalar threshold, a learned convolutional representation and a pretrained object detector. What is learned in each? What output could we test? Which failure examples must our dataset include? | 7

## Extra callable contracts

- grayscale(Frame) returns a new grayscale Frame; it does not modify the input or access hardware.
- sobel(Frame) returns a new RGB-encoded grayscale edge display; it uses fixed kernels and a black border. It does not identify separate objects.
- features.main reads a saved frame and writes two SVGs into a new directory. Reusing a directory raises FileExistsError to preserve evidence.

A productive next step is to measure whether a proposed extra feature resolves a specific ambiguity in your recorded failures, before connecting it to a motor decision.
