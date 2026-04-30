# LandRe Editor

A browser-based map editor for land readjustment planning. Move and readjust land parcels on a satellite basemap, check in real time whether they comply with land readjustment parameters, and export the result as KML or CSV. Developed by Chandan Deuskar.

## Features

### Drawing tools
- **Trace parcels** — click to trace original parcel boundaries from the satellite image
- **Draw polygon** — draw new parcels freehand; double-click or press Enter to close
- **Draw road** — draw a road centreline; double-click after the second point to finish
- **Select / Reshape** — click to select parcels, drag vertices to reshape, drag the polygon body to move
- **Delete polygon** — click a parcel to remove it
- **Ruler** — click to place measurement points; per-segment and total distances shown in metres/km; double-click or Escape to clear

### Snapping
While drawing, vertices snap to:
- Existing parcel vertices (blue circle indicator)
- Edge-edge intersections between polygons (orange diamond indicator)

### Parcel management
- **Upload KML** — import existing parcel boundaries from a KML file
- **Rename** — double-click a parcel name in the table or on the map to rename and retype it
- **Parcel types** — Private parcel, Road, Public commercial, Public social, Open space
- **Undo / Redo** — Ctrl+Z / Ctrl+Y (or Ctrl+Shift+Z)
- **Shrink selected parcels** — inset selected parcels by a percentage

### Table
The right panel shows a live parcel table with:

| Column | Description |
|--------|-------------|
| Name | Parcel name (double-click to rename) |
| Type | Parcel type (editable inline) |
| New m² | Current area |
| Orig m² | Original area from KML |
| Δ% | Area change from original |
| Ovlp% | Overlap with original parcel |
| Spill m² | Area outside the project boundary (flagged red if > 0) |

Click any column header to sort. Text columns sort A→Z first; numeric columns sort descending first. Click again to reverse.

### Project boundary
Automatically computed as the union of all original parcels. Parcels that extend outside this boundary are flagged in the Spill m² column.

### Visibility toggles
- Hide / show original parcels
- Hide / show new parcels

### Export
- **Export KML** — downloads original and readjusted parcels in two KML folders
- **Export CSV** — downloads the parcel table as a CSV file

---

## Running locally

```bash
cd landre_editor
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open [http://localhost:8000](http://localhost:8000).

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, uvicorn |
| Frontend | Vanilla JS, Leaflet 1.9.4, Turf.js v6 |
| Basemap | Esri World Imagery (satellite), OpenStreetMap |
| Deployment | Render (see `render.yaml`) |

---

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Z | Undo |
| Ctrl+Y / Ctrl+Shift+Z | Redo |
| Enter | Finish drawing current polygon or road |
| Escape | Cancel drawing / clear ruler |
