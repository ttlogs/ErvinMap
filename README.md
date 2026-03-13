# Parfaron - Interactive Layered World Map

An interactive, zoomable fantasy world map using layered 2D textures.

## Quick Start

```bash
python3 -m http.server 3000
```

Visit http://localhost:3000

## Features

- **Smooth Pan & Zoom** - Mouse wheel to zoom, click and drag to pan
- **Layer System** - Toggle terrain, labels, roads, and POIs independently
- **Infinite Zoom** - Each layer is a full-resolution texture
- **Layer Persistence** - Your layer preferences are saved locally

## Layer System

The map uses separate texture layers that stack together:

| Layer | File | Description |
|-------|------|-------------|
| Terrain | `Parfaron.png` | Base map (mountains, forests, water) |
| Labels | `layers/labels.png` | Place names (Russian text) |
| Roads | `layers/roads.png` | Trade routes and paths |
| POIs | `layers/pois.png` | City markers, dungeons, etc. |

Each layer is a full 8192x4096 PNG with transparency - no pixelation when zoomed in!

## Adding Content to Layers

### Option 1: Direct Image Editing
1. Open any layer in an image editor (Photoshop, GIMP, etc.)
2. Edit at full resolution (8192x4096)
3. Save as PNG (maintain transparency)

### Option 2: Generate from Data
The `scripts/` folder contains tools to:
- Detect text regions and create labels layer
- Draw roads between locations
- Generate POI markers

## Project Structure

```
ErvinMap/
├── index.html           # Layered map viewer
├── Parfaron.png        # Base terrain layer (8192x4096)
├── layers/
│   ├── labels.png      # Place names (empty - add your labels)
│   ├── roads.png       # Trade routes (empty - draw roads)
│   └── pois.png        # Points of interest (empty)
├── scripts/             # Layer generation tools
└── README.md
```

## Deployment to GitHub Pages

```bash
git add .
git commit -m "Add layered map system"
git push origin main
```

Then enable GitHub Pages in Settings → Pages → Deploy from main branch.

## Future Enhancements

- AI-generated terrain details
- Animated elements (moving characters)
- Real-time multiplayer character positions
- Custom campaign session markers
- Export/import map state

## Credits

- Base map: Parfaron fantasy world
- Built with vanilla JavaScript (no dependencies)
