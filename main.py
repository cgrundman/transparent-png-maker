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


def linear_color_gradient(low_color, high_color, steps=10):
    """
    Generate a linear list of RGB colors from low_color to high_color.

    Args:
        low_color (tuple): (R, G, B) starting color (dark).
        high_color (tuple): (R, G, B) ending color (light).
        steps (int): Number of colors in the output list.

    Returns:
        list[tuple]: List of (R, G, B) colors from dark → light.
    """
    gradient = []

    for i in range(steps):
        t = i / (steps - 1)  # normalized [0, 1]

        r = int(low_color[0] + t * (high_color[0] - low_color[0]))
        g = int(low_color[1] + t * (high_color[1] - low_color[1]))
        b = int(low_color[2] + t * (high_color[2] - low_color[2]))

        gradient.append((r, g, b))

    return gradient


INPUTS = './inputs'
OUTPUTS = './outputs'

# Create Color Gradient
high_color = (218, 230, 248)
low_color = (163, 177, 197)
color_gradient = linear_color_gradient(
    low_color=low_color, 
    high_color=high_color, 
    steps=75
)

tolerance = 0.65

png_files = [f for f in os.listdir(f"{INPUTS}")]

for file in png_files:
    if file.lower().endswith(".png"):
        input_path = os.path.join(INPUTS, file)
        output_path = os.path.join(OUTPUTS, file)


        img = Image.open(input_path)

        for i, target_color in enumerate(color_gradient):
        
            result = make_color_transparent(img, target_color, tolerance)
            img = result

        result.save(output_path)

        print(f"Saved to {output_path}")
