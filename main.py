import cv2
import numpy as np
import os

# --- Configuration ---
OUTPUT_DIR = "output_results"
IMAGE_FILENAME = os.path.join(OUTPUT_DIR, "generated_image.png")
ANNOTATED_IMAGE_PREFIX = os.path.join(OUTPUT_DIR, "clicked_pixel_")

# --- Synthetic Test Image Generator ---
def generate_test_image(width=300, height=200):
    """
    Generates a synthetic test image with varying BGR values.
    Returns the image and its dimensions (height, width).
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Top-left: Pure Blue
    img[0:height//2, 0:width//2] = [255, 0, 0] # BGR
    # Top-right: Pure Green
    img[0:height//2, width//2:width] = [0, 255, 0] # BGR
    # Bottom-left: Red gradient from left to right (0-255)
    for x_col in range(width//2):
        # Scale x_col from 0 to (width//2 - 1) to 0 to 255
        red_intensity = int(255 * (x_col / (width//2 - 1))) if (width//2 - 1) > 0 else 0
        img[height//2:height, x_col] = [0, 0, red_intensity] # BGR
    # Bottom-right: White-ish gradient (diagonal)
    for y_row in range(height//2, height):
        for x_col in range(width//2, width):
            # Linearly interpolate intensity based on distance from top-left of quadrant
            # relative x and y
            rel_x = x_col - width//2
            rel_y = y_row - height//2
            
            # Max possible distance in this quadrant
            max_rel_x = width//2 - 1
            max_rel_y = height//2 - 1
            max_dist = np.sqrt(max_rel_x**2 + max_rel_y**2)
            
            # Current distance from top-left of quadrant
            current_dist = np.sqrt(rel_x**2 + rel_y**2)
            
            intensity = int(255 * (current_dist / max_dist)) if max_dist > 0 else 0
            img[y_row, x_col] = [intensity, intensity, intensity]

    # Add specific pixels to test with known, non-pure values
    # Pixel in top-left blue quadrant, explicitly set to B=100, G=150, R=200
    target_y1, target_x1 = height // 4, width // 4
    img[target_y1, target_x1] = [100, 150, 200] 
    
    # Pixel in bottom-left red gradient, explicitly set to B=20, G=40, R=60
    target_y2, target_x2 = height - 10, width // 4 
    img[target_y2, target_x2] = [20, 40, 60] 

    return img, height, width

# --- Core Logic ---
def get_pixel_channel_range(image_path, click_points):
    """
    Loads an image, simulates clicks, calculates and prints the BGR channel range
    for each specified pixel. Saves annotated images.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image at {image_path}")
        return

    print(f"\n--- Analyzing image: {os.path.basename(image_path)} ---")
    print(f"Image dimensions: {img.shape[1]}x{img.shape[0]} (WxH)") # WxH convention

    for i, (y, x) in enumerate(click_points):
        print(f"\nProcessing simulated click {i+1} at pixel (x={x}, y={y}):")

        # Check if coordinates are within image bounds
        if not (0 <= y < img.shape[0] and 0 <= x < img.shape[1]):
            print(f"  Warning: Click point (x={x}, y={y}) is out of image bounds (image is {img.shape[1]}x{img.shape[0]} WxH). Skipping.")
            continue

        pixel_bgr = img[y, x] # OpenCV stores as BGR
        b, g, r = pixel_bgr[0], pixel_bgr[1], pixel_bgr[2]

        # Calculate the range
        intensities = np.array([b, g, r])
        min_intensity = np.min(intensities)
        max_intensity = np.max(intensities)
        channel_range = max_intensity - min_intensity

        print(f"  BGR values: B={b}, G={g}, R={r}")
        print(f"  Minimum intensity: {min_intensity}")
        print(f"  Maximum intensity: {max_intensity}")
        print(f"  Channel intensity range (Max - Min): {channel_range}")

        # --- Visual Output (for headless debugging/verification) ---
        # Draw a crosshair and circle on a copy of the image to mark the "clicked" pixel
        annotated_img = img.copy()
        
        # Circle at click point
        cv2.circle(annotated_img, (x, y), 5, (0, 255, 255), 1) # Yellow circle outline
        # Crosshair
        cv2.line(annotated_img, (x-7, y), (x+7, y), (0, 255, 255), 1) # Horizontal line
        cv2.line(annotated_img, (x, y-7), (x, y+7), (0, 255, 255), 1) # Vertical line

        # Put text with pixel info
        text_bg_color = (0, 0, 0) # Black
        text_color = (255, 255, 255) # White
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        font_thickness = 1

        # Text line 1: BGR values
        text1 = f"BGR: ({b},{g},{r})"
        (text1_width, text1_height), baseline1 = cv2.getTextSize(text1, font, font_scale, font_thickness)
        text1_origin = (x + 10, y - 10) # Position text slightly above and to the right of click

        # Draw background rectangle for text for readability
        cv2.rectangle(annotated_img, (text1_origin[0] - 2, text1_origin[1] - text1_height - 2),
                      (text1_origin[0] + text1_width + 2, text1_origin[1] + baseline1 + 2),
                      text_bg_color, -1)
        cv2.putText(annotated_img, text1, text1_origin, font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        # Text line 2: Range
        text2 = f"Range: {channel_range}"
        (text2_width, text2_height), baseline2 = cv2.getTextSize(text2, font, font_scale, font_thickness)
        text2_origin = (x + 10, y + 5 + text2_height) # Offset below first text line

        # Draw background rectangle for text
        cv2.rectangle(annotated_img, (text2_origin[0] - 2, text2_origin[1] - text2_height - 2),
                      (text2_origin[0] + text2_width + 2, text2_origin[1] + baseline2 + 2),
                      text_bg_color, -1)
        cv2.putText(annotated_img, text2, text2_origin, font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        annotated_filename = f"{ANNOTATED_IMAGE_PREFIX}{i+1}.png"
        cv2.imwrite(annotated_filename, annotated_img)
        print(f"  Saved annotated image to: {annotated_filename}")

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting Pixel Intensity Probe...")

    # 1. Ensure output directory exists and generate the synthetic image
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    print(f"Generating synthetic image...")
    img_generated, img_height, img_width = generate_test_image()
    
    cv2.imwrite(IMAGE_FILENAME, img_generated)
    print(f"Saved generated image to: {IMAGE_FILENAME}")

    # 2. Define simulated "click" points (y, x)
    # These points target different regions and specific test pixels within the generated image.
    simulated_clicks = [
        # Targets the specifically set pixel [100, 150, 200] in the blue quadrant
        (img_height // 4, img_width // 4),  
        # Targets a pixel in the top-right pure green region [0, 255, 0]
        (img_height // 4, img_width * 3 // 4), 
        # Targets a pixel in the bottom-left red gradient region (will be [0, 0, ~128])
        (img_height * 3 // 4, img_width // 4), 
        # Targets a pixel in the bottom-right white-ish diagonal gradient (will be [~128, ~128, ~128])
        (img_height * 3 // 4, img_width * 3 // 4), 
        # Targets the specifically set pixel [20, 40, 60] in the red gradient
        (img_height - 10, img_width // 4), 
        # An out-of-bounds click to demonstrate error handling
        (1000, 1000) 
    ]

    # 3. Process the simulated clicks
    get_pixel_channel_range(IMAGE_FILENAME, simulated_clicks)

    print("\nPixel Intensity Probe finished.")