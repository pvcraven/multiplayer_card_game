import logging

logging.basicConfig(level=logging.DEBUG)


class GameEngine:

    def __init__(self):
        self.game_data = {"users": [],
                          "cards": []}

        card = {"id": "SpadesA",
                "location": [100, 100]}
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


