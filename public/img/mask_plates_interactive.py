import os
import glob
import cv2

# Configuration
INPUT_DIR = r"C:\Users\Vamshi\OneDrive\Documents\GitHub\ehmi-vehicles\public\img\stimuli"
OUTPUT_DIR = r"C:\Users\Vamshi\OneDrive\Documents\GitHub\ehmi-vehicles\public\img\stimuli_masked"
BACKUP_DIR = r"C:\Users\Vamshi\OneDrive\Documents\GitHub\ehmi-vehicles\public\img\stimuli_backup"

# Maximum dimensions for display window on screen
MAX_DISP_WIDTH = 1200
MAX_DISP_HEIGHT = 700

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

image_files = sorted(glob.glob(os.path.join(INPUT_DIR, "image_*.jpg")) + 
                     glob.glob(os.path.join(INPUT_DIR, "image_*.png")))

if not image_files:
    print(f"No stimuli images found in {INPUT_DIR}")
    exit()

print("=" * 60)
print("INTERACTIVE MASKING INSTRUCTIONS:")
print("1. Drag a box over the number plate.")
print("2. Press SPACE or ENTER to apply the mask and move to next image.")
print("3. Press 'c' to skip an image if no plate is present.")
print("4. Press ESC or 'q' to quit.")
print("=" * 60)

for idx, img_path in enumerate(image_files, 1):
    filename = os.path.basename(img_path)
    img_orig = cv2.imread(img_path)
    if img_orig is None:
        continue

    # Backup original
    backup_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(backup_path):
        cv2.imwrite(backup_path, img_orig)

    # Calculate scale factor to fit screen
    orig_h, orig_w = img_orig.shape[:2]
    scale = min(MAX_DISP_WIDTH / orig_w, MAX_DISP_HEIGHT / orig_h, 1.0)
    disp_w = int(orig_w * scale)
    disp_h = int(orig_h * scale)

    # Resize image for display
    img_disp = cv2.resize(img_orig, (disp_w, disp_h), interpolation=cv2.INTER_AREA)

    window_name = f"[{idx}/{len(image_files)}] {filename} (Press SPACE/ENTER to mask, 'c' to skip)"
    r = cv2.selectROI(window_name, img_disp, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow(window_name)

    # If ROI was selected
    disp_x, disp_y, disp_w_box, disp_h_box = r
    if disp_w_box > 0 and disp_h_box > 0:
        # Map coordinates back to original image resolution
        orig_x = int(disp_x / scale)
        orig_y = int(disp_y / scale)
        orig_w_box = int(disp_w_box / scale)
        orig_h_box = int(disp_h_box / scale)

        x1 = max(0, orig_x)
        y1 = max(0, orig_y)
        x2 = min(orig_w, orig_x + orig_w_box)
        y2 = min(orig_h, orig_y + orig_h_box)

        roi = img_orig[y1:y2, x1:x2]
        if roi.size > 0:
            h_roi, w_roi = roi.shape[:2]
            # Downscale & upscale for pixelation
            small = cv2.resize(roi, (max(1, w_roi // 8), max(1, h_roi // 8)), interpolation=cv2.INTER_LINEAR)
            img_orig[y1:y2, x1:x2] = cv2.resize(small, (w_roi, h_roi), interpolation=cv2.INTER_NEAREST)

    # Save full-resolution masked image
    cv2.imwrite(os.path.join(OUTPUT_DIR, filename), img_orig)

cv2.destroyAllWindows()
print(f"\nAll images processed. Masked files saved in: {OUTPUT_DIR}")