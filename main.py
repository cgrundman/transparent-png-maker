from PIL import Image
import numpy as np

def make_color_transparent(input_path, output_path, target_color, tolerance_percent=10):
    """
    Makes pixels near target_color transparent in a PNG image.

    Args:
        input_path (str): Path to input PNG file.
        output_path (str): Path to save output PNG file.
        target_color (tuple): RGB color to make transparent, e.g. (255, 255, 255).
        tolerance_percent (float): Percentage of max color distance to allow.
    """
    # Load image and ensure RGBA mode
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)

    # Extract RGB channels
    rgb = data[:, :, :3].astype(np.int16)
    alpha = data[:, :, 3]

    # Compute color distance
    target = np.array(target_color, dtype=np.int16)
    distance = np.sqrt(np.sum((rgb - target) ** 2, axis=2))

    # Max possible color distance in RGB space
    max_distance = np.sqrt(255**2 * 3)
    tolerance = (tolerance_percent / 100) * max_distance

    # Create mask of pixels to make transparent
    mask = distance <= tolerance
    alpha[mask] = 0  # Set alpha to 0 (fully transparent)

    # Combine RGB and new alpha
    new_data = np.dstack((rgb, alpha))

    # Save the result
    new_img = Image.fromarray(new_data.astype(np.uint8), "RGBA")
    new_img.save(output_path)
    print(f"Saved to {output_path}")

make_color_transparent(
    input_path="./inputs/input.png",
    output_path="./outputs/output.png",
    target_color=(199, 211, 229),
    tolerance_percent=9
)
