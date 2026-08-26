import os
import glob
import cv2
import numpy as np
from pathlib import Path

# Configuration
INPUT_DIR = r"C:\Users\Vamshi\OneDrive\Documents\GitHub\ehmi-vehicles\public\img\stimuli"          # Path where stimuli are located
OUTPUT_DIR = r"C:\Users\Vamshi\OneDrive\Documents\GitHub\ehmi-vehicles\public\img\stimuli_masked"   # Path to save masked images
BACKUP_DIR = r"C:\Users\Vamshi\OneDrive\Documents\GitHub\ehmi-vehicles\public\img\stimuli_backup"   # Backup folder for originals
MASK_TYPE = "pixelate"                     # Options: 'blur', 'pixelate', 'solid'

# Pretrained Haar cascade for license plates (included with OpenCV)
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_russian_plate_number.xml"
plate_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def apply_mask(image, x, y, w, h, mask_type="pixelate"):
    """Applies blur, pixelation, or solid fill over the bounding box."""
    h_img, w_img = image.shape[:2]  # Get image height and width
    
    # Add a slight padding around the detected box
    pad_x, pad_y = int(w * 0.05), int(h * 0.05)
    x1 = max(0, x - pad_x)
    y1 = max(0, y - pad_y)
    x2 = min(w_img, x + w + pad_x)  # Fixed: bounds width to image width
    y2 = min(h_img, y + h + pad_y)  # Bounds height to image height
    
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return image

    if mask_type == "blur":
        # Heavy Gaussian blur
        k_w = (x2 - x1) // 2 * 2 + 1
        k_h = (y2 - y1) // 2 * 2 + 1
        blurred = cv2.GaussianBlur(roi, (max(25, k_w), max(25, k_h)), 30)
        image[y1:y2, x1:x2] = blurred

    elif mask_type == "pixelate":
        # Downscale and upscale to create mosaic pixelation
        h_roi, w_roi = roi.shape[:2]
        small = cv2.resize(roi, (max(1, w_roi // 8), max(1, h_roi // 8)), interpolation=cv2.INTER_LINEAR)
        pixelated = cv2.resize(small, (w_roi, h_roi), interpolation=cv2.INTER_NEAREST)
        image[y1:y2, x1:x2] = pixelated

    elif mask_type == "solid":
        # Neutral dark gray fill
        image[y1:y2, x1:x2] = (30, 30, 30)

    return image

def process_stimuli():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

    image_files = sorted(glob.glob(os.path.join(INPUT_DIR, "image_*.jpg")) + 
                         glob.glob(os.path.join(INPUT_DIR, "image_*.png")))

    if not image_files:
        print(f"No stimuli images found in {INPUT_DIR}")
        return

    print(f"Found {len(image_files)} stimuli images. Processing...")

    detected_count = 0
    for img_path in image_files:
        filename = os.path.basename(img_path)
        img = cv2.imread(img_path)
        if img is None:
            continue

        # Save backup copy
        cv2.imwrite(os.path.join(BACKUP_DIR, filename), img)

        # Convert to grayscale for detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect plates
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 15))

        if len(plates) > 0:
            detected_count += 1
            for (x, y, w, h) in plates:
                img = apply_mask(img, x, y, w, h, mask_type=MASK_TYPE)

        # Save output image
        cv2.imwrite(os.path.join(OUTPUT_DIR, filename), img)

    print(f"Processing complete. Detected and masked plates in {detected_count}/{len(image_files)} images.")
    print(f"Originals backed up to: {BACKUP_DIR}")
    print(f"Masked images saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_stimuli()