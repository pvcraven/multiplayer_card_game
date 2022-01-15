import logging

from server.channel_server import ChannelServer
from game_engine import GameEngine

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UserConnection:
    def __init__(self):
        self.channel = None
        self.user_name = None


class Server:
    def __init__(self, my_ip_address, my_ip_port):
        logger.debug(f"Starting to listen on {my_ip_address}:{my_ip_port}")
        self.channel_server = ChannelServer(my_ip_address=my_ip_address, my_ip_port=my_ip_port)
        self.channel_server.start_listening()
        self.user_connections = []
        self.game = GameEngine()

    def server_check(self):
        # Check for new connections
        channel = self.channel_server.get_new_channel()

        # There's a new connection
        if channel:
            user_connection = UserConnection()
            user_connection.channel = channel
            self.user_connections.append(user_connection)

        # List of closing connections
        user_connections_to_remove = []

        # Loop through each connection
        for user_connection in self.user_connections:

            # Give time to process input
            user_connection.channel.service_channel()

            # Check to see if we have any messages to process
            if not user_connection.channel.receive_queue.empty():

                # We do!
                data = user_connection.channel.receive_queue.get()

                # Grab the command out of the list and process
                command = data["command"]
                logger.debug(command)
                self.game.process_data(data, user_connection)

                # The only command this thread cares about, disconnect
                if command == "logout":
                    logging.debug(f"Logout from {user_connection.user_name}")
                    user_connection.channel.close()
                    user_connections_to_remove.append(user_connection)

                # Send everyone an update
                self.channel_server.broadcast(self.game.game_data)

        for user_connection in user_connections_to_remove:
            self.user_connections.remove(user_connection)
            logger.debug(f"Done with logout from {user_connection.user_name}")
