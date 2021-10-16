import arcade
import arcade.gui

from gui.waiting_for_players_view import WaitingForPlayersView
from network.communications_channel import CommunicationsChannel


class ConnectView(arcade.View):

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
        line_height = 40

        y -= line_height

        ui_text_label = arcade.gui.UITextArea(x=x_left,
                                              y=y,
                                              text="Server:",
                                              width=450,
                                              height=50,
                                              font_size=24,
                                              font_name="Kenney Future",
                                              text_color=arcade.color.WHITE)
        self.gui_manager.add(ui_text_label)

        self.server_input_box = arcade.gui.UIInputText(x=x_right,
                                                       y=y,
                                                       width=input_field_width,
                                                       height=50,
                                                       font_size=24,
                                                       font_name="Kenney Future",
                                                       text="192.168.1.75",
                                                       text_color=(255, 255, 255, 255))
        self.gui_manager.add(self.server_input_box)

        y -= line_height
        ui_text_label = arcade.gui.UITextArea(x=x_left,
                                              y=y,
                                              text="Port:",
                                              width=450,
                                              height=50,
                                              font_size=24,
                                              font_name="Kenney Future",
                                              text_color=arcade.color.WHITE)
        self.gui_manager.add(ui_text_label)

        self.port_input_box = arcade.gui.UIInputText(x=x_right,
                                                     y=y,
                                                     width=input_field_width,
                                                     height=50,
                                                     font_size=24,
                                                     font_name="Kenney Future",
                                                     text="10000",
                                                     text_color=(255, 255, 255, 255))
        self.gui_manager.add(self.port_input_box)

        y -= line_height

        connect_button = arcade.gui.UIFlatButton(text="Connect", width=200,
                                                 x=x_left,
                                                 y=y,
                                                 )

        @connect_button.event("on_click")
        def on_click_settings(event):
            print("Connect:", event)
            port = int(self.port_input_box.text)
            server = self.server_input_box.text

            user_name = self.window.user_name
            self.window.communications_channel = CommunicationsChannel(their_ip=server, their_port=port)
            self.window.communications_channel.connect()
            data = {"command": "login", "user_name": user_name}
            self.window.communications_channel.send_queue.put(data)

            view = WaitingForPlayersView()
            self.window.show_view(view)

        self.gui_manager.add(connect_button)

        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        self.gui_manager.draw()
