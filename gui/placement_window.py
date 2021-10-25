import arcade
import time
import logging

from gui.constants import *

from layout import calculate_position
from layout import layout

logging.basicConfig(level=logging.DEBUG)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

    def draw_layout(self, layout_x, layout_y, layout_width, layout_height, layout):
        if "locations" in layout:
            for location_name in layout["locations"]:
                location = layout["locations"][location_name]
                x, y, width, height = calculate_position(layout_x,
                                                         layout_y,
                                                         layout_width,
                                                         layout_height,
                                                         location_name,
                                                         layout)

                if "color" in location:
                    color = location["color"]
                    if isinstance(color, str) and color.startswith("#"):
                        h = color.lstrip('#')
                        color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

                    cx = x + width / 2
                    cy = y + height / 2
                    arcade.draw_rectangle_filled(cx, cy, width, height, color)

                self.draw_layout(x, y, width, height, location)

    def on_draw(self):
        self.draw_layout(0, 0, self.width, self.height, layout)


GameWindow()
arcade.run()
