import xml.etree.ElementTree as ElementTree
from typing import List
from dataclasses import dataclass
import logging


MM_TO_PX = 3.7795

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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


@dataclass
class Text:
    id: str
    x: float
    y: float
    style: dict
    text: str


def get_rect_info(rect: Rect, origin_x, origin_y, scale):
    cx = (rect.x + rect.width / 2) * scale + origin_x
    cy = (rect.y - rect.height / 2) * scale + origin_y
    width = rect.width * scale
    height = rect.height * scale
    return cx, cy, width, height


def get_point_info(x, y, origin_x, origin_y, scale):
    cx = x * scale + origin_x
    cy = y * scale + origin_y
    return cx, cy


def get_shape_at(svg, origin_x, origin_y, scale, target_x, target_y):

    for shape in svg.shapes:
        cx, cy, width, height = get_rect_info(shape, origin_x, origin_y, scale)

        if (cx - width / 2) <= target_x <= (cx + width / 2) and (cy - height / 2) <= target_y <= (cy + height / 2):
            return shape


def get_rect_for_name(svg, name: str):
    for shape in svg.shapes:
        if shape.id == name:
            return shape


def get_style_dict(style_string):
    style_list = style_string.split(';')
    style_dict = {}
    for item in style_list:
        name, value = item.split(':')
        style_dict[name] = value
    return style_dict


def process_item(item: ElementTree, shapes: List, image_height: float):
    # Strip namespace
    _, _, item.tag = item.tag.rpartition('}')

    # Process groups
    if item.tag == "g":
        item_id = item.attrib['id']
        logger.debug(f"Found group {item_id}.")
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
        style_dict = get_style_dict(item.attrib['style'])

        if "stroke-width" in style_dict:
            style_dict["stroke-width"] = convert_mm_to_px(float(style_dict["stroke-width"]))

        # Create object and append to list
        rect = Rect(item_id, x, y, width, height, style_dict)
        logging.debug(rect)
        shapes.append(rect)

    elif item.tag == "text":
        # Grab id
        item_id = item.attrib['id']
        # Coordinates
        x = convert_mm_to_px(float(item.attrib['x']))
        # Reverse y
        y = image_height - convert_mm_to_px(float(item.attrib['y']))
        # Style info
        style_dict = get_style_dict(item.attrib['style'])

        text_string = item.find("{http://www.w3.org/2000/svg}tspan").text

        # Create object and append to list
        text = Text(item_id, x, y, style_dict, text_string)
        logging.debug(text)
        shapes.append(text)


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
    process_svg('gui/layout.svg')


main()
