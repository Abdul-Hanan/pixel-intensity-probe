# pixel-intensity-probe

Reports BGR channel intensity range for specified pixels on an image.

## Overview

This project simulates user "clicks" on a static image in a headless environment. For each simulated click, it calculates and reports the numerical range (maximum minus minimum) of the Blue, Green, and Red channel intensities at that exact pixel. It then saves an annotated version of the image, highlighting the "clicked" pixel and its calculated values.

Since this tool is designed to run on headless servers without a graphical user interface, traditional interactive clicks are replaced by predefined coordinates within the script.

## Setup

1.  **Save the `main.py` file and `requirements.txt` to a new directory.**

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

Simply execute the `main.py` script:

```bash
python main.py
```

## Output

When you run the script, it will:

1.  Create an `output_results/` directory if it doesn't exist.
2.  Generate a synthetic test image named `generated_image.png` inside `output_results/`.
3.  Process a predefined list of "click" coordinates on this image.
4.  For each "click", it will print the BGR values, minimum intensity, maximum intensity, and the calculated channel intensity range to the console.
5.  Save an annotated image (e.g., `clicked_pixel_1.png`, `clicked_pixel_2.png`, etc.) for each processed click into the `output_results/` directory. These images visually mark the "clicked" pixel and display its BGR values and range for easy verification.
6.  Handle out-of-bounds "clicks" gracefully by printing a warning and skipping them.

Example console output for a pixel:

```
Processing simulated click 1 at pixel (x=75, y=50):
  BGR values: B=100, G=150, R=200
  Minimum intensity: 100
  Maximum intensity: 200
  Channel intensity range (Max - Min): 100
  Saved annotated image to: output_results/clicked_pixel_1.png
```