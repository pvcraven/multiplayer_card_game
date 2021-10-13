import time
import logging

from server.channel_server import ChannelServer
from game_engine import GameEngine

logging.basicConfig(level=logging.DEBUG)


class UserConnection:
    def __init__(self):
        self.channel = None
        self.user_name = None


def server():
    channel_server = ChannelServer(my_ip_address='127.0.0.1', my_ip_port=10000)
    channel_server.start_listening()
    user_connections = []
    game = GameEngine()

    while True:
        # Check for new connections
        channel = channel_server.get_new_channel()

        # There's a new connection
        if channel:
            user_connection = UserConnection()
            user_connection.channel = channel
            user_connections.append(user_connection)

        # List of closing connections
        user_connections_to_remove = []

        # Loop through each connection
        for user_connection in user_connections:

            # Give time to process input
            user_connection.channel.service_channel()

            # Check to see if we have any messages to process
            if not user_connection.channel.receive_queue.empty():

                # We do!
                data = user_connection.channel.receive_queue.get()

                # Grab the command out of the list and process
                command = data["command"]
                logging.debug(command)
                game.process_data(data, user_connection)

                # The only command this thread cares about, disconnect
                if command == "logout":
                    logging.debug(f"Logout from {user_connection.user_name}")
                    user_connection.channel.close()
                    user_connections_to_remove.append(user_connection)

                # Send everyone an update
                channel_server.broadcast(game.game_data)

        for user_connection in user_connections_to_remove:
            user_connections.remove(user_connection)
            logging.debug(f"Done with logout from {user_connection.user_name}")

        # Pause
        time.sleep(0.1)


server()
