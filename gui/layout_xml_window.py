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
        self.shapes = process_svg("layout.svg")
        print(self.shapes)

    def draw_layout(self):
        for shape in self.shapes:
            cx = shape.x + shape.width / 2
            cy = self.height - (shape.y + shape.height / 2)
            arcade.draw_rectangle_outline(cx, cy, shape.width, shape.height, arcade.color.BLACK, 2)

    def on_draw(self):
        self.clear(arcade.color.WHITE)
        self.draw_layout()


GameWindow()
arcade.run()
