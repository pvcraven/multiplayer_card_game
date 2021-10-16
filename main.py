import arcade
from gui.client_or_server_view import ClientOrServerView
from gui.game_window import GameWindow


def main():
    """ Main function """

    window = GameWindow()
    start_view = ClientOrServerView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
