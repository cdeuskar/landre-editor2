# LandRe Editor

A browser-based map editor for land readjustment planning. Move and readjust land parcels on a satellite basemap, check in real time whether they comply with land readjustment parameters, and export the result as KML or CSV. Developed by Chandan Deuskar.

## Features

### Drawing tools
- **Trace parcels** — click to trace original parcel boundaries from the satellite image
- **Edit originals** — select and reshape original parcel boundaries after tracing or uploading
- **Draw polygon** — draw new parcels freehand; double-click or press Enter to close
- **Draw road** — draw a road centreline; a dialog asks for road name and width, then the road polygon is generated automatically
- **Select / Reshape** — click to select parcels, drag vertices to reshape, drag the polygon body to move
  - Hold **Shift** while dragging a polygon edge to constrain movement to the perpendicular direction (useful for rectangular plots)
  - **Double-click** a shared vertex or edge to move it simultaneously across all adjacent parcels, keeping the layout gap-free
- **Delete polygon** — click a parcel to remove it
- **Ruler** — click to place measurement points; per-segment and total distances shown in metres/km; double-click or Escape to clear

### Snapping
While drawing, vertices snap to:
- Existing parcel vertices (blue circle indicator)
- Edge-edge intersections between polygons (orange diamond indicator)

### Edge and vertex alignment
- **Polygon edge popup** — right-click (or long-press on mobile) any polygon edge in Select / Reshape mode to open a context menu:
  - **Make parallel to…** — click a reference edge to rotate the selected edge to match its direction
  - **Make perpendicular to…** — click a reference edge to rotate the selected edge 90° from it
  - **Insert vertex here** — add a new vertex at the clicked point on the edge
- **Road vertex popup** — short-click a road centreline vertex in Select / Reshape mode to open a context menu:
  - **Make parallel to…** — rotate the adjacent road segment to be parallel to a clicked reference edge
  - **Make perpendicular to…** — rotate the adjacent road segment to be perpendicular to a clicked reference edge
- **Align selected with…** — select one or more parcels, then click any edge on the map to rectangularize the selection and align it to that edge's direction

### Parcel management
- **Upload KML** — import existing parcel boundaries from a KML file
- **Rename** — double-click a parcel name in the table or on the map to rename it
- **Parcel types** — Private parcel, Road, Public commercial, Public social, Open space
- **Undo / Redo** — Ctrl+Z / Ctrl+Y (or Ctrl+Shift+Z)
- **Resize selected parcels** — grow or shrink selected parcels by a percentage (enter a negative value to reduce)
- **Clip overlaps** — automatically trim any parcel that overlaps a road polygon, keeping layers clean
- **Clip spillover** — trim any parcel area that extends outside the project boundary

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
- **Colour gradient by Δ%** — colour private parcels from red (most reduced) to green (least reduced), giving an immediate visual read of which owners are carrying a disproportionate share of the land contribution

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
| Escape | Cancel drawing / clear ruler / dismiss alignment mode |
| Shift (while dragging edge) | Constrain edge movement to perpendicular direction |
