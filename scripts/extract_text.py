#!/usr/bin/env python3
"""
Extract text from detected regions using Tesseract OCR
Run locally with: pip install pytesseract pillow && sudo apt install tesseract-ocr tesseract-ocr-rus
"""

import re
import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Load image
img = cv2.imread("Parfaron.png")

# Read regions
text_regions = []
with open("text_regions.txt", "r") as f:
    for line in f:
        match = re.search(r"x=(\d+),\s*y=(\d+),\s*w=(\d+),\s*h=(\d+)", line)
        if match:
            x, y, w, h = int(match[1]), int(match[2]), int(match[3]), int(match[4])
            text_regions.append((x, y, w, h))

print(f"Processing {len(text_regions)} regions with OCR...")

pois = []
for i, (x, y, w, h) in enumerate(text_regions):
    # Add padding
    pad = 3
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(img.shape[1], x + w + pad)
    y2 = min(img.shape[0], y + h + pad)

    # Extract region
    roi = img[y1:y2, x1:x2]

    # OCR
    try:
        text = pytesseract.image_to_string(roi, lang="rus+eng").strip()
        text = " ".join(text.split())  # Normalize whitespace
    except:
        text = ""

    if text:
        pois.append({"x": x + w // 2, "y": y + h // 2, "name": text})
        print(f"{len(pois)}: {text}")

    if (i + 1) % 50 == 0:
        print(f"Processed {i + 1}/{len(text_regions)}...")

# Save POI data
import json

with open("pois.json", "w", encoding="utf-8") as f:
    json.dump(pois, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(pois)} POIs to pois.json")
