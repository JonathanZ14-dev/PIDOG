"""A complete small playground. Run it, then change ONE value and run again."""
from .perception import Settings, analyze, demo_image


def main():
    # A list holds the three cases. The for-loop applies the same function to each.
    for position in ["left", "center", "right"]:
        frame = demo_image(position)  # NumPy image created without a camera.
        settings = Settings(color="blue", min_pixels=300)
        annotated, mask, observation = analyze(frame, settings)
        # Names receive returned values. Unused images are okay in this text experiment.
        print(position, observation["found"], observation["image_region"])
        print("Array shape:", frame.shape, "one BGR pixel:", frame[100, 25].tolist())
        # Try min_pixels=2000. Predict which output changes before running.
        # Try color="green". Does the scene change, or just the rule?


if __name__ == "__main__":
    main()  # This guard keeps imports from starting our experiment accidentally.
