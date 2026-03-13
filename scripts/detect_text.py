#!/usr/bin/env python3
"""
Improved text detection using MSER algorithm
Better filtering for Russian text on fantasy maps
"""

import cv2
import json


def detect_text_regions(img_path, output_file):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape
    debug_img = img.copy()

    # Method 1: MSER - best for text detection
    mser = cv2.MSER_create()
    mser.setMinArea(50)
    mser.setMaxArea(5000)
    mser.setMaxVariation(0.5)
    regions_mser, _ = mser.detectRegions(gray)

    all_regions = []
    print(f"MSER found {len(regions_mser)} regions")

    for region in regions_mser:
        x, y, bw, bh = cv2.boundingRect(region)
        aspect = bw / float(bh) if bh > 0 else 0

        # Text characteristics for Russian text:
        # Height: 15-80px, Width: 30-500px, Aspect: 1.2-15
        if 15 <= bh <= 80 and 30 <= bw <= 500 and 1.2 <= aspect <= 15:
            pad = 3
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(w, x + bw + pad)
            y2 = min(h, y + bh + pad)
            all_regions.append(
                {
                    "x": x1,
                    "y": y1,
                    "w": x2 - x1,
                    "h": y2 - y1,
                    "orig_x": x,
                    "orig_y": y,
                    "orig_w": bw,
                    "orig_h": bh,
                    "method": "MSER",
                }
            )
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    print(f"After MSER filtering: {len(all_regions)} regions")

    # Method 2: Additional threshold-based detection
    for thresh_val in [35, 45, 55, 65]:
        _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            aspect = bw / float(bh) if bh > 0 else 0

            if 15 <= bh <= 80 and 40 <= bw <= 400 and 1.2 <= aspect <= 15:
                # Check if already detected
                is_duplicate = False
                for r in all_regions:
                    if abs(r["orig_x"] - x) < 20 and abs(r["orig_y"] - y) < 20:
                        is_duplicate = True
                        break

                if not is_duplicate:
                    pad = 3
                    x1 = max(0, x - pad)
                    y1 = max(0, y - pad)
                    x2 = min(w, x + bw + pad)
                    y2 = min(h, y + bh + pad)
                    all_regions.append(
                        {
                            "x": x1,
                            "y": y1,
                            "w": x2 - x1,
                            "h": y2 - y1,
                            "orig_x": x,
                            "orig_y": y,
                            "orig_w": bw,
                            "orig_h": bh,
                            "method": "threshold",
                        }
                    )
                    cv2.rectangle(debug_img, (x1, y1), (x2, y2), (255, 0, 0), 2)

    print(f"After threshold method: {len(all_regions)} regions")

    # Merge overlapping regions
    all_regions = merge_regions(all_regions)
    all_regions.sort(key=lambda r: (r["y"] // 100, r["x"]))

    cv2.imwrite("detection_debug.png", debug_img)

    with open(output_file, "w") as f:
        json.dump(all_regions, f, indent=2)

    print(f"Final: {len(all_regions)} regions saved to {output_file}")
    return all_regions


def merge_regions(regions):
    if not regions:
        return []

    merged = True
    while merged:
        merged = False
        i = 0
        while i < len(regions):
            j = i + 1
            while j < len(regions):
                r1, r2 = regions[i], regions[j]
                if (
                    r1["x"] < r2["x"] + r2["w"]
                    and r1["x"] + r1["w"] > r2["x"]
                    and r1["y"] < r2["y"] + r2["h"]
                    and r1["y"] + r1["h"] > r2["y"]
                ):
                    new_x = min(r1["x"], r2["x"])
                    new_y = min(r1["y"], r2["y"])
                    new_w = max(r1["x"] + r1["w"], r2["x"] + r2["w"]) - new_x
                    new_h = max(r1["y"] + r1["h"], r2["y"] + r2["h"]) - new_y
                    regions[i] = {
                        "x": new_x,
                        "y": new_y,
                        "w": new_w,
                        "h": new_h,
                        "orig_x": new_x,
                        "orig_y": new_y,
                        "orig_w": new_w,
                        "orig_h": new_h,
                        "method": "merged",
                    }
                    regions.pop(j)
                    merged = True
                else:
                    j += 1
            i += 1

    return regions


if __name__ == "__main__":
    detect_text_regions("Parfaron.png", "detected_regions.json")
