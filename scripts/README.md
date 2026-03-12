# Parfaron Map Scripts

Python scripts for processing and tiling the fantasy world map.

## Requirements

```bash
pip install pillow opencv-python-headless numpy
sudo apt install tesseract-ocr tesseract-ocr-rus  # for OCR
```

## Scripts

### 1. detect_text.py
Detects text regions on the map image using computer vision.

```bash
python scripts/detect_text.py
```
- Input: `Parfaron_original.png`
- Output: `text_regions.txt` (list of detected text bounding boxes)

### 2. remove_text.py
Removes detected text regions from the map using inpainting.

```bash
python scripts/remove_text.py
```
- Input: `Parfaron_original.png`, `text_regions.txt`
- Output: `Parfaron_clean.png`

### 3. generate_tiles.py
Creates Deep Zoom (DZI) tiles from the cleaned map image.

```bash
python scripts/generate_tiles.py
```
- Input: `Parfaron.png` (or any image named this)
- Output: `parfaron_tiles/` folder + `parfaron_tiles.dzi`

### 4. extract_text.py
Uses Tesseract OCR to read text from detected regions.

```bash
python scripts/extract_text.py
```
- Input: `Parfaron_original.png`, `text_regions.txt`
- Output: `pois.json` (detected text with coordinates)

## Workflow

1. Start with original map: `Parfaron_original.png`
2. Detect text: `python scripts/detect_text.py`
3. Remove text: `python scripts/remove_text.py`
4. Generate tiles: `python scripts/generate_tiles.py`
5. Extract text (optional): `python scripts/extract_text.py`

## Notes

- All scripts expect to be run from the project root directory
- Tesseract requires system installation (see requirements above)
- The viewer (`index.html`) expects tiles in `parfaron_tiles/` folder
- **Important**: `detect_text.py` and `extract_text.py` require `Parfaron_original.png` to be present
