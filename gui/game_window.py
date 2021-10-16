import arcade
import time
import logging

from gui.constants import *

logging.basicConfig(level=logging.DEBUG)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.communications_channel = None
        self.server = None
        self.game_data = None
        self.user_name = None

    def on_close(self):
        print("Closing")
        self.close()

    def on_close(self):
        logging.debug("Closing connection...")
        if self.communications_channel:
            self.communications_channel.send_queue.put({"command": "logout"})
            while not self.communications_channel.send_queue.empty():
                self.communications_channel.service_channel()
                time.sleep(0.1)
            self.communications_channel.close()
        logging.debug("Closed.")
        self.close()
