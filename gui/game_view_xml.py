import arcade
import logging

from .layout_xml import process_svg
from .layout_xml import get_rect_info
from .layout_xml import get_point_info
from .layout_xml import get_shape_at
from .layout_xml import get_rect_for_name
from .layout_xml import Rect
from .layout_xml import Text

logging.basicConfig(level=logging.DEBUG)


class GameViewXML(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        arcade.set_background_color(arcade.color.PAPAYA_WHIP)

        # Pieces
        self.piece_list = arcade.SpriteList()

        # List of items we are dragging with the mouse
        self.held_items = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_items_original_position = []

        self.svg = process_svg("gui/layout.svg")

        self.process_game_data(self.window.game_data)

    def on_update(self, delta_time):

        # Service client network tasks
        self.window.communications_channel.service_channel()

        # Are we a server? If so, service that
        if self.window.server:
            self.window.server.server_check()

        # Any messages to process?
        if not self.window.communications_channel.receive_queue.empty():
            data = self.window.communications_channel.receive_queue.get()
            self.window.game_data = data
            self.process_game_data(data)

    def process_game_data(self, data):

        self.piece_list = arcade.SpriteList()

        def process_items(items):
            for item in items:
                logging.debug(f"{item['name']}, {item['location']}")
                rect = get_rect_for_name(self.svg, item["location"])
                if rect:
                    origin_x, origin_y, ratio = self.calculate_screen_data()
                    cx, cy, width, height = get_rect_info(rect, origin_x, origin_y, ratio)
                    sprite = arcade.Sprite(f"images/{item['image_name']}.png", ratio)
                    sprite.properties['name'] = item['name']
                    sprite.position = cx, cy
                    self.piece_list.append(sprite)
                    logging.debug(f"Placed {item['location']} at ({cx}, {cy})")
                else:
                    logging.warning(f"Can't find location for {item['location']}")

        placement_list = data["placements"]
        process_items(placement_list)
        pieces_list = data["pieces"]
        process_items(pieces_list)

    def calculate_screen_data(self):
        ratio_width, ratio_height = self.svg.width, self.svg.height
        screen_width = self.window.width
        screen_height = self.window.height

        # Compare ratio to screen size, get the min so we can fit on screen
        ratio = min(screen_width / ratio_width, screen_height / ratio_height)

        # Get our display size based on this ratio
        display_width = ratio * ratio_width
        display_height = ratio * ratio_height

        # Calculate our lower-left origin
        origin_x = (screen_width - display_width) / 2
        origin_y = (screen_height - display_height) / 2
        return origin_x, origin_y, ratio

    def draw_layout(self):

        origin_x, origin_y, ratio = self.calculate_screen_data()
        for shape in self.svg.shapes:
            if isinstance(shape, Rect):

                cx, cy, width, height = get_rect_info(shape, origin_x, origin_y, ratio)
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
            elif isinstance(shape, Text):
                x, y = get_point_info(shape.x, shape.y, origin_x, origin_y, ratio)
                arcade.draw_text(shape.text, x, y, arcade.color.BLACK, 24)

    def on_draw(self):
        arcade.start_render()
        self.draw_layout()
        self.piece_list.draw()

    def on_resize(self, width: float, height: float):
        self.process_game_data(self.window.game_data)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        pieces = arcade.get_sprites_at_point((x, y), self.piece_list)

        # Have we clicked on a card?
        if len(pieces) > 0:

            # Might be a stack, get the top one
            primary = pieces[-1]

            # All other cases, grab the face-up card we are clicking on
            self.held_items = [primary]
            # Save the position
            self.held_items_original_position = [self.held_items[0].position]

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding items, move them with the mouse
        for item in self.held_items:
            item.center_x += dx
            item.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_items) == 0:
            return

        origin_x, origin_y, scale = self.calculate_screen_data()
        destination = get_shape_at(self.svg, origin_x, origin_y, scale, x, y)

        if destination:
            for item in self.held_items:
                item_name = item.properties['name']
                destination_name = destination.id
                logging.debug(f"Move {item_name} to {destination_name}")

                data = {"command": "move_piece",
                        "name": item_name,
                        "destination": destination_name}

                self.window.communications_channel.send_queue.put(data)
        else:
            logging.debug(f"No item at dropped location")

        for i, item in enumerate(self.held_items):
            item.position = self.held_items_original_position[i]
        self.held_items = []

