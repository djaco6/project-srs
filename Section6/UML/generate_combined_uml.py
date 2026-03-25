#!/usr/bin/env python3
"""
Generate a combined UML class diagram SVG from 9 individual class SVGs.
All content is inlined -- no external references.
"""

import re
import os

BASE_DIR = "/Users/jacob/Spring2026/SoftwareEngineering/project/Section6/UML"

# SVG files and their dimensions (width, height)
svg_files = [
    ("01_user.svg",                386, 546),
    ("02_user_profile.svg",        400, 460),
    ("03_document.svg",            420, 680),
    ("04_doc_page.svg",            340, 200),
    ("05_entity.svg",              420, 680),
    ("06_annotation.svg",          400, 906),
    ("07_urban_population.svg",    360, 330),
    ("08_regional_population.svg", 440, 370),
    ("09_travel_speed_reference.svg", 320, 230),
]

# ── Layout positions ──
# We'll compute Y positions based on actual heights with ~60px gap between rows.
PADDING = 30
TITLE_HEIGHT = 50  # space for title at top
GAP = 60

# X positions for columns
COL1_X = 50
COL2_X = 550
COL3_X = 1050

# Row 1: User (386x546), UserProfile (400x460)
row1_y = TITLE_HEIGHT + PADDING
row1_max_h = max(546, 460)

# Row 2: Document (420x680), DocPage (340x200)
row2_y = row1_y + row1_max_h + GAP
row2_max_h = max(680, 200)

# Row 3: Entity (420x680), Annotation (400x906)
row3_y = row2_y + row2_max_h + GAP
row3_max_h = max(680, 906)

# Row 4: UrbanPopulation (360x330), RegionalPopulation (440x370), TravelSpeedReference (320x230)
row4_y = row3_y + row3_max_h + GAP
row4_max_h = max(330, 370, 230)

positions = {
    "01_user.svg":                (COL1_X, row1_y),
    "02_user_profile.svg":        (COL2_X, row1_y),
    "03_document.svg":            (COL1_X, row2_y),
    "04_doc_page.svg":            (COL2_X, row2_y),
    "05_entity.svg":              (COL1_X, row3_y),
    "06_annotation.svg":          (COL2_X, row3_y),
    "07_urban_population.svg":    (COL1_X, row4_y),
    "08_regional_population.svg": (COL2_X, row4_y),
    "09_travel_speed_reference.svg": (COL3_X, row4_y),
}

dims = {name: (w, h) for name, w, h in svg_files}


def extract_inner_svg(filepath):
    """Extract everything between the opening <svg ...> and closing </svg> tags."""
    with open(filepath, "r") as f:
        content = f.read()
    # Remove the outer <svg> opening tag
    content = re.sub(r'<svg[^>]*>', '', content, count=1)
    # Remove the closing </svg>
    content = content.rsplit('</svg>', 1)[0]
    return content.strip()


def make_unique_styles(inner_content, index):
    """Prefix CSS class names to avoid collisions between embedded SVGs."""
    # Each SVG uses classes like .class-name, .attr, .section-label, .class-note, .constraint
    # We'll prefix them with cls{index}_ to avoid conflicts
    prefix = f"c{index}_"

    # Replace class definitions in <style> blocks
    def replace_style_classes(match):
        style_block = match.group(1)
        # Replace .classname { with .c{i}_classname {
        style_block = re.sub(r'\.([a-zA-Z][\w-]*)', lambda m: f'.{prefix}{m.group(1)}', style_block)
        return f'<style>{style_block}</style>'

    inner_content = re.sub(r'<style>(.*?)</style>', replace_style_classes, inner_content, flags=re.DOTALL)

    # Replace class="..." references in elements
    def replace_class_attr(match):
        classes = match.group(1)
        new_classes = ' '.join(f'{prefix}{c}' for c in classes.split())
        return f'class="{new_classes}"'

    inner_content = re.sub(r'class="([^"]*)"', replace_class_attr, inner_content)

    return inner_content


def diamond_marker(marker_id, filled=True):
    """Create a diamond marker definition for composition lines."""
    fill = "#333" if filled else "white"
    return (
        f'<marker id="{marker_id}" viewBox="0 0 12 8" refX="0" refY="4" '
        f'markerWidth="12" markerHeight="8" orient="auto">'
        f'<polygon points="0,4 6,0 12,4 6,8" fill="{fill}" stroke="#333" stroke-width="0.8"/>'
        f'</marker>'
    )


def arrow_marker(marker_id, dashed=False):
    """Create an open arrow marker for association/dependency lines."""
    color = "#666" if dashed else "#333"
    return (
        f'<marker id="{marker_id}" viewBox="0 0 10 10" refX="10" refY="5" '
        f'markerWidth="8" markerHeight="8" orient="auto">'
        f'<polyline points="0,0 10,5 0,10" fill="none" stroke="{color}" stroke-width="1.5"/>'
        f'</marker>'
    )


def box_center(filename):
    """Get the center point of a class box in the combined diagram."""
    x, y = positions[filename]
    w, h = dims[filename]
    return (x + w / 2, y + h / 2)


def box_bottom_center(filename):
    x, y = positions[filename]
    w, h = dims[filename]
    return (x + w / 2, y + h)


def box_top_center(filename):
    x, y = positions[filename]
    w, h = dims[filename]
    return (x + w / 2, y)


def box_right_center(filename):
    x, y = positions[filename]
    w, h = dims[filename]
    return (x + w, y + h / 2)


def box_left_center(filename):
    x, y = positions[filename]
    w, h = dims[filename]
    return (x, y + h / 2)


def box_right_at_y(filename, frac=0.5):
    """Right edge at a fractional Y position."""
    x, y = positions[filename]
    w, h = dims[filename]
    return (x + w, y + h * frac)


def box_left_at_y(filename, frac=0.5):
    x, y = positions[filename]
    w, h = dims[filename]
    return (x, y + h * frac)


def box_bottom_at_x(filename, frac=0.5):
    x, y = positions[filename]
    w, h = dims[filename]
    return (x + w * frac, y + h)


def box_top_at_x(filename, frac=0.5):
    x, y = positions[filename]
    w, h = dims[filename]
    return (x + w * frac, y)


# ── Build relationship lines ──
def build_relationships():
    lines = []

    # Helper: composition line (solid, filled diamond at parent)
    def composition(parent_file, child_file, parent_mult, child_mult,
                    p_start, p_end, label_offset_start=(0,0), label_offset_end=(0,0),
                    waypoints=None):
        x1, y1 = p_start
        x2, y2 = p_end

        if waypoints:
            points = [(x1, y1)] + waypoints + [(x2, y2)]
            path_d = f"M {points[0][0]},{points[0][1]}"
            for px, py in points[1:]:
                path_d += f" L {px},{py}"
            lines.append(
                f'<path d="{path_d}" fill="none" stroke="#333" stroke-width="2" '
                f'marker-start="url(#diamond-filled)"/>'
            )
        else:
            lines.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="#333" stroke-width="2" marker-start="url(#diamond-filled)"/>'
            )

        # Multiplicity labels
        lx1 = x1 + label_offset_start[0]
        ly1 = y1 + label_offset_start[1]
        lx2 = x2 + label_offset_end[0]
        ly2 = y2 + label_offset_end[1]
        lines.append(
            f'<text x="{lx1}" y="{ly1}" font-size="13" font-family="sans-serif" '
            f'fill="#333" font-weight="bold">{parent_mult}</text>'
        )
        lines.append(
            f'<text x="{lx2}" y="{ly2}" font-size="13" font-family="sans-serif" '
            f'fill="#333" font-weight="bold">{child_mult}</text>'
        )

    # Helper: association line (solid, open arrow at target)
    def association(source_file, target_file, source_mult, target_mult,
                    p_start, p_end, label_offset_start=(0,0), label_offset_end=(0,0)):
        x1, y1 = p_start
        x2, y2 = p_end
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#333" stroke-width="1.5" marker-end="url(#arrow-solid)"/>'
        )
        lx1 = x1 + label_offset_start[0]
        ly1 = y1 + label_offset_start[1]
        lx2 = x2 + label_offset_end[0]
        ly2 = y2 + label_offset_end[1]
        lines.append(
            f'<text x="{lx1}" y="{ly1}" font-size="13" font-family="sans-serif" '
            f'fill="#333" font-weight="bold">{source_mult}</text>'
        )
        lines.append(
            f'<text x="{lx2}" y="{ly2}" font-size="13" font-family="sans-serif" '
            f'fill="#333" font-weight="bold">{target_mult}</text>'
        )

    # Helper: dependency line (dashed, open arrow at target)
    def dependency(source_file, target_file, label,
                   p_start, p_end, label_pos=None):
        x1, y1 = p_start
        x2, y2 = p_end
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#666" stroke-width="1.5" stroke-dasharray="8,4" '
            f'marker-end="url(#arrow-dashed)"/>'
        )
        if label_pos:
            lx, ly = label_pos
        else:
            lx = (x1 + x2) / 2
            ly = (y1 + y2) / 2 - 8
        lines.append(
            f'<text x="{lx}" y="{ly}" font-size="12" font-family="sans-serif" '
            f'fill="#666" font-style="italic" text-anchor="middle">{label}</text>'
        )

    # ── 1. User ── UserProfile (composition, 1:1, horizontal) ──
    p_start = box_right_at_y("01_user.svg", 0.08)
    p_end = box_left_at_y("02_user_profile.svg", 0.08)
    composition("01_user.svg", "02_user_profile.svg", "1", "1",
                p_start, p_end,
                label_offset_start=(8, -8), label_offset_end=(-20, -8))

    # ── 2. User ── Document (composition, 1:*, vertical) ──
    p_start = box_bottom_at_x("01_user.svg", 0.3)
    p_end = box_top_at_x("03_document.svg", 0.3)
    composition("01_user.svg", "03_document.svg", "1", "*",
                p_start, p_end,
                label_offset_start=(8, 18), label_offset_end=(8, -6))

    # ── 3. Document ── DocPage (composition, 1:*, horizontal) ──
    p_start = box_right_at_y("03_document.svg", 0.06)
    p_end = box_left_at_y("04_doc_page.svg", 0.2)
    composition("03_document.svg", "04_doc_page.svg", "1", "*",
                p_start, p_end,
                label_offset_start=(8, -8), label_offset_end=(-20, -8))

    # ── 4. Document ── Entity (composition, 1:*, vertical) ──
    p_start = box_bottom_at_x("03_document.svg", 0.25)
    p_end = box_top_at_x("05_entity.svg", 0.25)
    composition("03_document.svg", "05_entity.svg", "1", "*",
                p_start, p_end,
                label_offset_start=(8, 18), label_offset_end=(8, -6))

    # ── 5. Document ── Annotation (composition, 1:*, vertical going down-right) ──
    p_start = box_bottom_at_x("03_document.svg", 0.75)
    p_end = box_top_at_x("06_annotation.svg", 0.5)
    # Route: go down from Document, then right to Annotation
    mid_y = (p_start[1] + p_end[1]) / 2
    composition("03_document.svg", "06_annotation.svg", "1", "*",
                p_start, p_end,
                label_offset_start=(8, 18), label_offset_end=(8, -6),
                waypoints=[(p_start[0], mid_y), (p_end[0], mid_y)])

    # ── 6. Entity ── Annotation (association, 1:*, horizontal) ──
    p_start = box_right_at_y("05_entity.svg", 0.08)
    p_end = box_left_at_y("06_annotation.svg", 0.04)
    association("05_entity.svg", "06_annotation.svg", "1", "*",
                p_start, p_end,
                label_offset_start=(8, -8), label_offset_end=(-20, -8))

    # ── 7. Entity ── UrbanPopulation (association, *:0..1, vertical) ──
    p_start = box_bottom_at_x("05_entity.svg", 0.3)
    p_end = box_top_at_x("07_urban_population.svg", 0.5)
    association("05_entity.svg", "07_urban_population.svg", "*", "0..1",
                p_start, p_end,
                label_offset_start=(8, 18), label_offset_end=(8, -6))

    # ── 8. Annotation ── RegionalPopulation (dependency, <<lookup>>) ──
    p_start = box_bottom_at_x("06_annotation.svg", 0.35)
    p_end = box_top_at_x("08_regional_population.svg", 0.5)
    dependency("06_annotation.svg", "08_regional_population.svg", "&lt;&lt;lookup&gt;&gt;",
               p_start, p_end)

    # ── 9. Annotation ── TravelSpeedReference (dependency, <<lookup>>) ──
    p_start = box_bottom_at_x("06_annotation.svg", 0.75)
    p_end = box_top_at_x("09_travel_speed_reference.svg", 0.5)
    # Route: down from Annotation, then right to TravelSpeedRef
    mid_y = (p_start[1] + p_end[1]) / 2
    lines.append(
        f'<path d="M {p_start[0]},{p_start[1]} L {p_start[0]},{mid_y} '
        f'L {p_end[0]},{mid_y} L {p_end[0]},{p_end[1]}" '
        f'fill="none" stroke="#666" stroke-width="1.5" stroke-dasharray="8,4" '
        f'marker-end="url(#arrow-dashed)"/>'
    )
    label_x = (p_start[0] + p_end[0]) / 2
    label_y = mid_y - 8
    lines.append(
        f'<text x="{label_x}" y="{label_y}" font-size="12" font-family="sans-serif" '
        f'fill="#666" font-style="italic" text-anchor="middle">&lt;&lt;lookup&gt;&gt;</text>'
    )

    return '\n    '.join(lines)


def main():
    # Compute total canvas size
    total_width = COL3_X + 320 + PADDING  # rightmost box (TravelSpeedRef width=320)
    total_height = row4_y + row4_max_h + PADDING

    # Build embedded class groups
    class_groups = []
    for i, (filename, w, h) in enumerate(svg_files):
        filepath = os.path.join(BASE_DIR, filename)
        inner = extract_inner_svg(filepath)
        inner = make_unique_styles(inner, i)
        x, y = positions[filename]
        class_groups.append(
            f'  <!-- {filename} -->\n'
            f'  <g transform="translate({x}, {y})">\n'
            f'    {inner}\n'
            f'  </g>'
        )

    relationships = build_relationships()

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {total_width} {total_height}"
     width="{total_width}" height="{total_height}">

  <!-- Background -->
  <rect x="0" y="0" width="{total_width}" height="{total_height}" fill="#FAFAFA"/>

  <!-- Title -->
  <text x="{total_width / 2}" y="38" text-anchor="middle"
        font-family="sans-serif" font-size="20" font-weight="bold" fill="#1a237e">
    Alexandria - UML Class Diagram
  </text>

  <!-- Marker definitions -->
  <defs>
    {diamond_marker("diamond-filled", filled=True)}
    {diamond_marker("diamond-open", filled=False)}
    {arrow_marker("arrow-solid", dashed=False)}
    {arrow_marker("arrow-dashed", dashed=True)}
  </defs>

  <!-- Relationship lines (drawn first so boxes render on top) -->
  <g id="relationships">
    {relationships}
  </g>

  <!-- Class boxes -->
{chr(10).join(class_groups)}

</svg>'''

    output_path = os.path.join(BASE_DIR, "combined_uml.svg")
    with open(output_path, "w") as f:
        f.write(svg)

    print(f"Generated: {output_path}")
    print(f"Canvas dimensions: {total_width} x {total_height}")


if __name__ == "__main__":
    main()
