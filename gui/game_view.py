import arcade


CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)
        self.card_list = arcade.SpriteList()

        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

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

    def on_draw(self):
        arcade.start_render()

        self.card_list.draw()

        x = 20
        y = self.window.height - 50
        arcade.draw_text("Users:",
                         start_x=x,
                         start_y=y,
                         color=arcade.color.WHITE,
                         font_size=24,
                         font_name="Kenney Future",
                         )

        if self.window.game_data:
            users = self.window.game_data["users"]
            for user in users:
                y -= 30
                arcade.draw_text(user,
                                 start_x=x,
                                 start_y=y,
                                 color=arcade.color.WHITE,
                                 font_size=24,
                                 font_name="Kenney Future",
                                 )

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]

            # All other cases, grab the face-up card we are clicking on
            self.held_cards = [primary_card]
            # Save the position
            self.held_cards_original_position = [self.held_cards[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_cards[0])

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        card_list = []
        for card_sprite in self.held_cards:
            card = {"id": card_sprite.name,
                    "position": list(card_sprite.position)}
            card_list.append(card)

        data = {"command": "move_cards",
                "cards": card_list}

        self.window.communications_channel.send_queue.put(data)

        # We are no longer holding cards
        self.held_cards = []
