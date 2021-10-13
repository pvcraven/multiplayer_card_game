import logging
import random

logging.basicConfig(level=logging.DEBUG)

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


class GameEngine:

    def __init__(self):
        self.game_data = {"users": [],
                          "cards": []}

        for card_value in CARD_VALUES:
            x = random.randrange(600)
            y = random.randrange(600)
            card = {"id": f"Spades{card_value}",
                    "location": [x, y]}
            self.game_data["cards"].append(card)

    def process_data(self, data, user_connection):
        command = data["command"]

        if command == "login":
            user_name = data["user_name"]
            user_connection.user_name = user_name
            self.game_data["users"].append(user_name)
            logging.debug(f"Log in from  {user_connection.user_name}")

        elif command == "logout":
            logging.debug(f"Logout from {user_connection.user_name}")
            self.game_data["users"].remove(user_connection.user_name)

        elif command == "move_cards":

            logging.debug(f"Moving cards")
            client_cards = data["cards"]
            server_cards = self.game_data["cards"]

            for client_card in client_cards:
                client_id = client_card["id"]
                client_position = client_card["position"]
                logging.debug(f"  Processing {client_id}")
                for server_card in server_cards:
                    if client_id == server_card["id"]:
                        server_card["location"] = client_position
                        logging.debug(f"  Moved {client_id}")


