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


def process_item(item: ElementTree, shapes: List):
    # Strip namespace
    _, _, item.tag = item.tag.rpartition('}')

    # Process groups
    if item.tag == "g":
        item_id = item.attrib['id']
        print(f"Found group {item_id}.")
        for child in item:
            process_item(child, shapes)

    elif item.tag == "rect":
        # Grab id
        item_id = item.attrib['id']
        # Dimensions
        width = convert_mm_to_px(float(item.attrib['width']))
        height = convert_mm_to_px(float(item.attrib['height']))
        # Coordinates
        x = convert_mm_to_px(float(item.attrib['x']))
        y = convert_mm_to_px(float(item.attrib['y']))
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
        shapes.append(rect)


def process_svg(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    width = float(root.attrib['width'])
    height = float(root.attrib['height'])
    print(width, height)

    shapes = []
    for item in root:
        process_item(item, shapes)

    svg = SVG(shapes, width, height)
    return svg


def main():
    process_svg('layout.svg')


main()
