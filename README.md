# Parfaron - Interactive Fantasy World Map

An interactive, zoomable map of the fantasy world built with OpenSeadragon.

## Quick Start

### View the Map

Simply open `index.html` in a web browser, or serve locally:

```bash
python3 -m http.server 3000
```

Then visit http://localhost:3000

### Features

- **Smooth Pan & Zoom** - Mouse wheel to zoom, click and drag to pan
- **Minimap** - Overview in bottom-right corner
- **Points of Interest** - Click "Show POIs" button to display labeled locations
- **Fullscreen** - Press the fullscreen button for immersive viewing

## Project Structure

```
ErvinMap/
├── index.html              # Main map viewer (OpenSeadragon)
├── Parfaron.png            # Source map image (8192x4096)
├── parfaron_tiles.dzi      # Tile configuration file
├── parfaron_tiles_files/   # Deep Zoom tiles (5 zoom levels)
├── pois.json               # Points of Interest data
└── scripts/                # Map processing tools
    ├── README.md           # Script documentation
    ├── detect_text.py      # Detect text regions on map
    ├── remove_text.py      # Remove text via inpainting
    ├── generate_tiles.py   # Create DZI tiles
    └── extract_text.py     # OCR text extraction
```

## Deployment to GitHub Pages

1. Push to GitHub:
```bash
git add .
git commit -m "Add interactive fantasy map"
git push origin main
```

2. Go to **Settings → Pages** in your repository:
   - Source: Deploy from a branch
   - Branch: `main` / `root`
   - Click Save

Your map will be live at `https://yourusername.github.io/repo-name/`

## Technical Details

- **Viewer**: OpenSeadragon 5.0
- **Tile Format**: Deep Zoom (DZI)
- **Image Size**: 8192x4096 pixels
- **Zoom Levels**: 5 (512px to 8192px)
- **Total Tile Size**: ~11MB

## Future Enhancements

- AI-generated detailed map (via upscaling services like Magnific AI)
- Real-time character positions (WebSocket)
- Interactive roads and routes
- Custom markers for campaign sessions

## Credits

Map image: Parfaron (fantasy world)
Viewer: OpenSeadragon
