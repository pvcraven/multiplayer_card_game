import arcade
import time
import logging

from layout_xml import process_svg

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Test"

logging.basicConfig(level=logging.DEBUG)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.svg = process_svg("layout.svg")

    def draw_layout(self):

        ratio_width, ratio_height = self.svg.width, self.svg.height
        screen_width = self.width
        screen_height = self.height

        # Compare ratio to screen size, get the min so we can fit on screen
        ratio = min(screen_width / ratio_width, screen_height / ratio_height)

        # Get our display size based on this ratio
        display_width = ratio * ratio_width
        display_height = ratio * ratio_height

        # Calculate our lower-left origin
        origin_x = (screen_width - display_width) / 2
        origin_y = (screen_height - display_height) / 2

        for shape in self.svg.shapes:
            cx = (shape.x + shape.width / 2) * ratio + origin_x
            cy = (self.height - (shape.y + shape.height / 2) * ratio) - origin_y
            width = shape.width * ratio
            height = shape.height * ratio
            if "fill" in shape.style:
                color = shape.style["fill"]
                if isinstance(color, str) and color.startswith("#"):
                    h = color.lstrip('#')
                    color = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
                    if "fill-opacity" in shape.style:
                        opacity = int(float(shape.style["fill-opacity"]) * 255)
                        color.append(opacity)
                    arcade.draw_rectangle_filled(cx, cy, width, height, color)
            if "stroke" in shape.style:
                color = shape.style["stroke"]
                if isinstance(color, str) and color.startswith("#"):
                    h = color.lstrip('#')
                    color = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
                    if "stroke-opacity" in shape.style:
                        opacity = int(float(shape.style["stroke-opacity"]) * 255)
                        color.append(opacity)

                    stroke_width = shape.style["stroke-width"] * ratio
                    arcade.draw_rectangle_outline(cx, cy, width, height, color, stroke_width)

            # arcade.draw_rectangle_outline(cx, cy, shape.width, shape.height, arcade.color.BLACK, 2)

    def on_draw(self):
        self.clear(arcade.color.WHITE)
        self.draw_layout()


GameWindow()
arcade.run()
