import logging
import random

from gui.constants import *

logging.basicConfig(level=logging.DEBUG)

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


class GameEngine:

    def __init__(self):
        self.game_data = {"users": [],
                          "cards": [],
                          "pieces": [],
                          "placements": [],
                          "view": "waiting_for_players"}

    def process_data(self, data, user_connection):
        command = data["command"]

        if command == "login":
            user_name = data["user_name"]
            user = {"name": user_name,
                    "resource-1": 0,
                    "resource-2": 0,
                    "resource-3": 0,
                    "resource-4": 0,
                    "resource-5": 0,
                    }
            user_connection.user_name = user_name
            self.game_data["users"].append(user)
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

        elif command == "start_game":

            # # Put the cards in the game
            # for card_value in CARD_VALUES:
            #     x = random.randrange(600)
            #     y = random.randrange(600)
            #     card = {"id": f"Spades{card_value}",
            #             "location": [x, y]}
            #     self.game_data["cards"].append(card)

            for user_no in range(len(self.game_data["users"])):
                for piece_no in range(3):
                    x = DISTANCE_BETWEEN_USERS * user_no + 20 + piece_no * 32
                    y = 15
                    piece = {"image_name": f"player_pieces/player_{user_no + 1}",
                             "name": f"piece-{piece_no}",
                             "location": [x, y]}
                    self.game_data["pieces"].append(piece)

            x = 100
            y = 100
            placement = {"image_name": f"placements/placement_1",
                         "name": f"placement-1",
                         "location": [x, y],
                         "actions": ["add-resource-1"]}
            self.game_data["placements"].append(placement)

            x = 100
            y = 300
            placement = {"image_name": f"placements/placement_2",
                         "name": f"placement-2",
                         "location": [x, y],
                         "actions": ["add-resource-2"]}
            self.game_data["placements"].append(placement)

            self.game_data["view"] = "game_view"

        elif command == "move_piece":

            destination = data["destination"]
            placement = None
            for cur_placement in self.game_data["placements"]:
                if cur_placement["name"] == destination:
                    placement = cur_placement
            if not placement:
                logging.debug(f"Did not find placement for {destination}.")

            piece = None
            for cur_piece in self.game_data["pieces"]:
                if cur_piece["name"] == data["name"]:
                    piece = cur_piece
            if not piece:
                logging.debug(f"Did not find placement for {data['name']}.")

            player = None
            for cur_player in self.game_data["users"]:
                if cur_player["name"] == user_connection.user_name:
                    player = cur_player

            assert player is not None

            if piece and placement:
                piece["location"] = [placement["location"][0], placement["location"][1]]
                piece["location"][0] += PIECE_PLACEMENT_OFFSET[0]
                piece["location"][1] += PIECE_PLACEMENT_OFFSET[1]
                logging.debug(f"Moved piece to {destination}.")
                for action in placement["actions"]:
                    if action == "add-resource-1":
                        player["resource-1"] += 1
                    if action == "add-resource-2":
                        player["resource-2"] += 1

