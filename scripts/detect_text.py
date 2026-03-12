#!/usr/bin/env python3
"""
Improved text detection for fantasy maps
"""

import cv2


def detect_text_regions(img_path, output_file):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    all_regions = []

    # Method 1: Inverted threshold for dark text
    for thresh in [30, 40, 50, 60, 80]:
        _, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            aspect = bw / float(bh) if bh > 0 else 0
            area = bw * bh

            if 0.3 < aspect < 25 and 200 < area < 80000 and 8 < bh < 200:
                all_regions.append((x, y, bw, bh))

    # Method 2: Canny edge detection
    for low, high in [(30, 100), (50, 150), (80, 200)]:
        edges = cv2.Canny(gray, low, high)
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            aspect = bw / float(bh) if bh > 0 else 0
            area = bw * bh

            if 0.5 < aspect < 18 and 300 < area < 60000 and 10 < bh < 120:
                all_regions.append((x, y, bw, bh))

    # Merge overlapping regions
    merged = merge_regions(all_regions)
    merged.sort(key=lambda r: (r[1] // 100, r[0]))

    print(f"Found {len(merged)} text regions")

    with open(output_file, "w") as f:
        for i, (x, y, bw, bh) in enumerate(merged):
            f.write(f"{i}: x={x}, y={y}, w={bw}, h={bh}\n")

    return merged


def merge_regions(regions):
    if not regions:
        return []

    rects = [[x, y, x + w, y + h] for (x, y, w, h) in regions]
    merged = []

    for rect in rects:
        x1, y1, x2, y2 = rect
        found = False
        for i, m in enumerate(merged):
            mx1, my1, mx2, my2 = m
            if x1 < mx2 and x2 > mx1 and y1 < my2 and y2 > my1:
                merged[i] = [min(x1, mx1), min(y1, my1), max(x2, mx2), max(y2, my2)]
                found = True
                break
        if not found:
            merged.append(rect)

    return [(m[0], m[1], m[2] - m[0], m[3] - m[1]) for m in merged]


if __name__ == "__main__":
    detect_text_regions("Parfaron_original.png", "text_regions.txt")
