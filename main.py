import os
import json
import xml.etree.ElementTree as ET
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/")
async def index():
    with open(os.path.join(BASE_DIR, "static", "index.html"), "r") as f:
        return HTMLResponse(f.read())


@app.post("/api/upload/kml")
async def upload_kml(file: UploadFile = File(...)):
    content = await file.read()
    root = ET.fromstring(content)

    # Support both namespaced and bare KML
    ns = {"k": "http://www.opengis.net/kml/2.2"}
    placemarks = root.findall(".//k:Placemark", ns)
    if not placemarks:
        placemarks = root.findall(".//Placemark")
        ns = {}

    def find(el, tag):
        if ns:
            return el.find(f".//k:{tag}", ns)
        return el.find(f".//{tag}")

    features = []
    for i, pm in enumerate(placemarks):
        name_el = find(pm, "name")
        name = name_el.text.strip() if name_el is not None and name_el.text else f"Parcel {chr(65 + i)}"

        poly_el = find(pm, "Polygon")
        if poly_el is None:
            continue
        coords_el = find(poly_el, "coordinates")
        if coords_el is None or not coords_el.text:
            continue

        coords = []
        for token in coords_el.text.strip().split():
            parts = token.split(",")
            if len(parts) >= 2:
                try:
                    coords.append([float(parts[0]), float(parts[1])])
                except ValueError:
                    continue

        if len(coords) < 3:
            continue
        if coords[0] != coords[-1]:
            coords.append(coords[0])

        features.append({
            "type": "Feature",
            "properties": {"name": name},
            "geometry": {"type": "Polygon", "coordinates": [coords]},
        })

    return {"type": "FeatureCollection", "features": features}


@app.post("/api/export/kml")
async def export_kml(data: dict):
    import html as _html

    originals  = data.get("originals", [])
    readjusted = data.get("readjusted", [])

    # KML colours are aabbggrr (alpha, blue, green, red)
    def hex_to_kml(hex_color: str, opacity: float = 1.0) -> str:
        h = hex_color.lstrip("#")
        r, g, b = h[0:2], h[2:4], h[4:6]
        a = format(round(opacity * 255), "02x")
        return (a + b + g + r).lower()

    # (styleId, lineHex, lineOpacity, fillHex, fillOpacity, lineWidth)
    STYLES = [
        ("style-private-parcel", "#1a7a1a", 1.0, "#90ee90", 0.45, 2.0),
        ("style-road",           "#333333", 1.0, "#888888", 0.65, 2.0),
        ("style-public",         "#1a5276", 1.0, "#aed6f1", 0.55, 2.0),
        ("style-open-space",     "#1a5c4a", 1.0, "#a2d9ce", 0.55, 2.0),
        ("style-original",       "#c0c0c0", 1.0, "#d8d8d8", 0.08, 1.5),
    ]
    TYPE_STYLE = {
        "Private parcel": "style-private-parcel",
        "Road":           "style-road",
        "Public":         "style-public",
        "Open space":     "style-open-space",
    }

    def style_xml(s):
        sid, lc, lo, fc, fo, w = s
        return (
            f'  <Style id="{sid}">\n'
            f'    <LineStyle><color>{hex_to_kml(lc, lo)}</color><width>{w}</width></LineStyle>\n'
            f'    <PolyStyle><color>{hex_to_kml(fc, fo)}</color></PolyStyle>\n'
            f'  </Style>'
        )

    def placemark(feature, is_original=False):
        props      = feature.get("properties", {})
        name       = _html.escape(props.get("name", "Unnamed"))
        ptype      = props.get("type", "")
        coords     = feature["geometry"]["coordinates"][0]
        coord_str  = " ".join(f"{c[0]},{c[1]},0" for c in coords)
        sid        = "style-original" if is_original else TYPE_STYLE.get(ptype, "style-private-parcel")
        desc_line  = f"      <description>{_html.escape(ptype)}</description>\n" if ptype else ""
        return (
            f"    <Placemark>\n"
            f"      <name>{name}</name>\n"
            f"{desc_line}"
            f"      <styleUrl>#{sid}</styleUrl>\n"
            f"      <Polygon><outerBoundaryIs><LinearRing>\n"
            f"        <coordinates>{coord_str}</coordinates>\n"
            f"      </LinearRing></outerBoundaryIs></Polygon>\n"
            f"    </Placemark>"
        )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
        *[style_xml(s) for s in STYLES],
        "  <Folder><name>Originals</name>",
        *[placemark(f, True) for f in originals],
        "  </Folder>",
        "  <Folder><name>Readjusted layout</name>",
        *[placemark(f) for f in readjusted],
        "  </Folder>",
        "</Document></kml>",
    ]

    return Response(
        content="\n".join(lines),
        media_type="application/vnd.google-earth.kml+xml",
        headers={"Content-Disposition": "attachment; filename=readjusted_layout.kml"},
    )
