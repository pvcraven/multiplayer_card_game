from typing import List
from dataclasses import dataclass
import xml.etree.ElementTree as ElementTree


@dataclass
class Rect:
    """Class for keeping track of an item in inventory."""
    id: str
    x: float
    y: float
    width: float
    height: float


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
        item_id = item.attrib['id']
        width = float(item.attrib['width'])
        height = float(item.attrib['height'])
        x = float(item.attrib['x'])
        y = float(item.attrib['y'])
        rect = Rect(item_id, x, y, width, height)
        shapes.append(rect)


def process_svg(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    width = root.attrib['width']
    height = root.attrib['height']
    print(width, height)

    shapes = []
    for item in root:
        process_item(item, shapes)

    return shapes


def main():
    process_svg('layout.svg')


main()
