#!/usr/bin/env python3
"""
Deep Zoom Image (DZI) generator - creates tiled images for OpenSeadragon
"""

import os
import math
import json
from PIL import Image


def generate_dzi_tiles(input_path, output_dir, tile_size=512, overlap=1):
    """Generate DZI tiles from a large image."""

    img = Image.open(input_path)
    width, height = img.size

    os.makedirs(output_dir, exist_ok=True)

    # Calculate number of zoom levels (pyramid)
    max_dimension = max(width, height)
    levels = int(math.ceil(math.log2(max_dimension / tile_size))) + 1

    print(f"Image: {width}x{height}")
    print(f"Levels: {levels}")

    # Create DZI XML
    dzi_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Image TileSize="{tile_size}" Overlap="{overlap}" Format="png" xmlns="http://schemas.microsoft.com/deepzoom/2008">
    <Size Width="{width}" Height="{height}"/>
</Image>'''

    with open(f"{output_dir}.dzi", "w") as f:
        f.write(dzi_xml)

    # Generate tiles for each level
    current_img = img
    level = 0

    for level in range(levels):
        level_dir = os.path.join(output_dir, str(level))
        os.makedirs(level_dir, exist_ok=True)

        current_width, current_height = current_img.size
        tiles_x = math.ceil(current_width / tile_size)
        tiles_y = math.ceil(current_height / tile_size)

        print(
            f"Level {level}: {current_width}x{current_height}, {tiles_x}x{tiles_y} tiles"
        )

        for ty in range(tiles_y):
            for tx in range(tiles_x):
                # Calculate tile boundaries
                x = tx * tile_size
                y = ty * tile_size

                # Add overlap
                x_start = max(0, x - overlap)
                y_start = max(0, y - overlap)
                x_end = min(current_width, x + tile_size + overlap)
                y_end = min(current_height, y + tile_size + overlap)

                # Crop and save tile
                tile = current_img.crop((x_start, y_start, x_end, y_end))
                tile_path = os.path.join(level_dir, f"{tx}_{ty}.png")
                tile.save(tile_path, "PNG")

        # Prepare next level (downsample by 2)
        if level < levels - 1:
            new_width = max(1, current_width // 2)
            new_height = max(1, current_height // 2)
            current_img = current_img.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )

    print(f"\nDZI files created in: {output_dir}")
    print(f"- {output_dir}.dzi (descriptor)")
    print(f"- {output_dir}/ (tile folders)")


if __name__ == "__main__":
    import sys

    input_file = "Parfaron.png"
    output_name = "parfaron_tiles"

    generate_dzi_tiles(input_file, output_name, tile_size=512, overlap=1)
