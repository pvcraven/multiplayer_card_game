import arcade
from gui.connect_view import ConnectView
from gui.game_window import GameWindow

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Network Demo"


def main():
    """ Main function """

    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = ConnectView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
