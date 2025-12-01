import os
from PIL import Image
import numpy as np

def make_color_transparent(img, target_color, tolerance_percent=10):
    """
    Makes pixels near target_color transparent in a PIL image.

    Args:
        img (PIL.Image): Input image.
        target_color (tuple): RGB color to make transparent, e.g. (255, 255, 255).
        tolerance_percent (float): Percentage of max color distance to allow.

    Returns:
        PIL.Image: New image with transparency applied.
    """
    img = img.convert("RGBA")
    data = np.array(img)

    rgb = data[:, :, :3].astype(np.int16)
    alpha = data[:, :, 3]

    target = np.array(target_color, dtype=np.int16)
    distance = np.sqrt(np.sum((rgb - target) ** 2, axis=2))

    max_distance = np.sqrt(255**2 * 3)
    tolerance = (tolerance_percent / 100) * max_distance

    mask = distance <= tolerance
    alpha[mask] = 0

    new_data = np.dstack((rgb, alpha))
    return Image.fromarray(new_data.astype(np.uint8), "RGBA")


INPUTS = './inputs'
OUTPUTS = './outputs'

png_files = [f for f in os.listdir(f"{INPUTS}")]

for file in png_files:
    if file.lower().endswith(".png"):
        input_path = os.path.join(INPUTS, file)
        output_path = os.path.join(OUTPUTS, file)

        #target_color = (218, 230, 248)
        target_color = (180, 194, 213)
        tolerance = 1

        img = Image.open(input_path)
        result = make_color_transparent(img, target_color, tolerance)

        result.save(output_path)
        print(f"Saved to {output_path}")
