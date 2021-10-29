from typing import List
from dataclasses import dataclass
import xml.etree.ElementTree as ElementTree


MM_TO_PX = 3.7795


def convert_mm_to_px(mm: float):
    return mm * MM_TO_PX


@dataclass
class SVG:
    shapes: list
    width: float
    height: float


@dataclass
class Rect:
    """Class for keeping track of an item in inventory."""
    id: str
    x: float
    y: float
    width: float
    height: float
    style: dict


def get_rect_info(rect: Rect, origin_x, origin_y, scale):
    cx = (rect.x + rect.width / 2) * scale + origin_x
    cy = (rect.y - rect.height / 2) * scale + origin_y
    width = rect.width * scale
    height = rect.height * scale
    return cx, cy, width, height


def get_shape_at(svg, origin_x, origin_y, scale, target_x, target_y):

    print("Click")
    for shape in svg.shapes:
        cx, cy, width, height = get_rect_info(shape, origin_x, origin_y, scale)

        if (cx - width / 2) <= target_x <= (cx + width / 2) and (cy - height / 2) <= target_y <= (cy + height / 2):
            print(f"Yes: {shape.id}")


def process_item(item: ElementTree, shapes: List, image_height: float):
    # Strip namespace
    _, _, item.tag = item.tag.rpartition('}')

    # Process groups
    if item.tag == "g":
        item_id = item.attrib['id']
        print(f"Found group {item_id}.")
        for child in item:
            process_item(child, shapes, image_height)

    elif item.tag == "rect":
        # Grab id
        item_id = item.attrib['id']
        # Dimensions
        width = convert_mm_to_px(float(item.attrib['width']))
        height = convert_mm_to_px(float(item.attrib['height']))
        # Coordinates
        x = convert_mm_to_px(float(item.attrib['x']))
        # Reverse y
        y = image_height - convert_mm_to_px(float(item.attrib['y']))
        # Style info
        style_string = item.attrib['style']
        style_list = style_string.split(';')
        style_dict = {}
        for item in style_list:
            name, value = item.split(':')
            style_dict[name] = value

        if "stroke-width" in style_dict:
            style_dict["stroke-width"] = convert_mm_to_px(float(style_dict["stroke-width"]))

        # Create object and append to list
        rect = Rect(item_id, x, y, width, height, style_dict)
        print(rect)
        shapes.append(rect)


def process_svg(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    image_width = float(root.attrib['width'])
    image_height = float(root.attrib['height'])

    shapes = []
    for item in root:
        process_item(item, shapes, image_height)

    svg = SVG(shapes, image_width, image_height)
    return svg


def main():
    process_svg('layout.svg')


main()
