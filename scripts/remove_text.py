#!/usr/bin/env python3
"""Remove text regions from map using inpainting"""

import cv2
import re
import numpy as np

img = cv2.imread("Parfaron_original.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = np.zeros(gray.shape, dtype=np.uint8)

text_regions = []
with open("text_regions.txt", "r") as f:
    for line in f:
        match = re.search(r"x=(\d+),\s*y=(\d+),\s*w=(\d+),\s*h=(\d+)", line)
        if match:
            x, y, w, h = int(match[1]), int(match[2]), int(match[3]), int(match[4])
            text_regions.append((x, y, w, h))

print(f"Processing {len(text_regions)} regions...")

for i, (x, y, w, h) in enumerate(text_regions):
    pad = 5
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(img.shape[1], x + w + pad)
    y2 = min(img.shape[0], y + h + pad)
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

cv2.imwrite("text_mask.png", mask)
print("Mask saved")

result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
cv2.imwrite("Parfaron_clean.png", result)
print("Clean map saved to Parfaron_clean.png")
