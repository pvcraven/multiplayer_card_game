import arcade


class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)

    def on_update(self, delta_time):

        self.window.communications_channel.service_channel()
        if not self.window.communications_channel.receive_queue.empty():
            data = self.window.communications_channel.receive_queue.get()
            self.window.game_data = data

    def on_draw(self):
        arcade.start_render()
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

