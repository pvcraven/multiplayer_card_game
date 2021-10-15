import logging

import arcade
import arcade.gui

from gui.game_view import GameView
from gui.connect_view import ConnectView


class ClientOrServerView(arcade.View):

    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.gui_manager = arcade.gui.UIManager()
        self.gui_manager.enable()
        self.networking_thread = None

        y = self.window.height - 150
        x_left = 30
        x_right = 350
        input_field_width = 300
        line_height = 150

        ui_text_label = arcade.gui.UILabel(x=x_left,
                                           y=y,
                                           text="Start Game",
                                           width=self.window.width,
                                           height=50,
                                           font_size=32,
                                           font_name="Kenney Future",
                                           align="center",
                                           text_color=arcade.color.WHITE)
        self.gui_manager.add(ui_text_label)

        y -= line_height

        ui_text_label = arcade.gui.UITextArea(x=x_left,
                                              y=y,
                                              text="User name:",
                                              width=450,
                                              height=40,
                                              font_size=24,
                                              font_name="Kenney Future",
                                              text_color=arcade.color.WHITE)
        self.gui_manager.add(ui_text_label)

        self.name_input_box = arcade.gui.UIInputText(x=x_right,
                                                     y=y,
                                                     width=input_field_width,
                                                     height=40,
                                                     font_size=24,
                                                     font_name="Kenney Future",
                                                     text="<enter>",
                                                     text_color=(255, 255, 255, 255))
        self.gui_manager.add(self.name_input_box)

        y -= line_height

        server_button = arcade.gui.UIFlatButton(text="Start Server", width=200,
                                                x=x_left,
                                                y=y,
                                                )

        @server_button.event("on_click")
        def on_click_settings(event):
            game_view = GameView()
            self.window.show_view(game_view)
            self.window.user_name = self.name_input_box.text
            logging.debug(f"Starting server with user name {self.window.user_name}")

        self.gui_manager.add(server_button)

        client_button = arcade.gui.UIFlatButton(text="Connect to Server", width=200,
                                                x=x_right,
                                                y=y,
                                                )

        @client_button.event("on_click")
        def on_click_settings(event):
            view = ConnectView()
            self.window.show_view(view)
            self.window.user_name = self.name_input_box.text
            logging.debug(f"Starting server with user name {self.window.user_name}")

        self.gui_manager.add(client_button)

        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        self.gui_manager.draw()

        # Draw box around input field
        x = self.name_input_box.x
        y = self.name_input_box.y
        width = self.name_input_box.width
        height = self.name_input_box.height
        x += width / 2 - 5
        y += height / 2
        arcade.draw_rectangle_outline(x, y, width, height, arcade.color.WHITE, 2)


