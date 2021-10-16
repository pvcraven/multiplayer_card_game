import arcade


from gui.constants import *
from game_engine.constants import *


class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        arcade.set_background_color(arcade.color.PAPAYA_WHIP)
        self.card_list = arcade.SpriteList()
        self.piece_list = arcade.SpriteList()
        self.placement_list = arcade.SpriteList()
        self.placement_decorations = arcade.SpriteList()

        # List of items we are dragging with the mouse
        self.held_items = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_items_original_position = []

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

        cards = data["cards"]
        self.card_list = arcade.SpriteList()
        for card in cards:
            id = card["id"]
            location = card["location"]
            image_file_name = f":resources:images/cards/card{id}.png"
            sprite = arcade.Sprite(image_file_name, scale=0.5)
            sprite.position = location
            sprite.name = id
            self.card_list.append(sprite)

        pieces = data["pieces"]
        self.piece_list = arcade.SpriteList()
        for piece in pieces:
            name = piece["name"]
            image_name = piece["image_name"]
            location = piece["location"]
            image_file_name = f"images/{image_name}.png"
            sprite = arcade.Sprite(image_file_name, scale=0.5)
            sprite.position = location
            sprite.name = name
            self.piece_list.append(sprite)

        placements = data["placements"]
        self.placement_list = arcade.SpriteList()
        for placement in placements:
            name = placement["name"]
            image_name = placement["image_name"]
            location = placement["location"]
            image_file_name = f"images/{image_name}.png"
            sprite = arcade.Sprite(image_file_name, scale=0.5)
            sprite.position = location
            sprite.name = name
            self.placement_list.append(sprite)
            x = 51
            for action in placement["actions"]:
                for i in range(resource_count):
                    if action == f"add-resource-{i}":
                        image_file_name = f"images/resources/resource-{i}.png"

                sprite = arcade.Sprite(image_file_name, scale=0.5)
                sprite.position = [location[0] + x, location[1] - 27]
                self.placement_decorations.append(sprite)
                x -= 18

    def on_draw(self):
        arcade.start_render()

        self.card_list.draw()
        self.placement_list.draw()
        self.placement_decorations.draw()
        self.piece_list.draw()

        if self.window.game_data:
            users = self.window.game_data["users"]
            for user_no, user in enumerate(users):
                x = USER_NAME_OFFSET[0] + (DISTANCE_BETWEEN_USERS * user_no)
                y = USER_NAME_OFFSET[1]

                arcade.draw_text(user["name"],
                                 start_x=x,
                                 start_y=y,
                                 color=arcade.color.PASTEL_BROWN,
                                 font_size=24,
                                 font_name="Kenney Future",
                                 )

                x = RESOURCE_LIST_OFFSET[0] + (DISTANCE_BETWEEN_USERS * user_no)
                y = RESOURCE_LIST_OFFSET[1]

                for i in range(resource_count):
                    resources_text = ""
                    x += RESOURCE_LIST_SEPARATION[0]
                    y += RESOURCE_LIST_SEPARATION[1]
                    letter = chr(i+65)
                    resources_text += f"{letter}-{user['resources'][i]}"

                    arcade.draw_text(resources_text,
                                     start_x=x,
                                     start_y=y,
                                     color=arcade.color.PASTEL_BROWN,
                                     font_size=20,
                                     )

                x += DISTANCE_BETWEEN_USERS

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

        # If we are holding cards, move them with the mouse
        for item in self.held_items:
            item.center_x += dx
            item.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_items) == 0:
            return

        destination = "None"
        for item in self.held_items:
            collision = arcade.check_for_collision_with_list(item, self.placement_list)
            for placement in collision:
                destination = placement.name

            data = {"command": "move_piece",
                    "name": item.name,
                    "destination": destination}

            self.window.communications_channel.send_queue.put(data)

        # We are no longer holding cards
        self.held_items = []
