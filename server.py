import time
import logging

from server.channel_server import ChannelServer

logging.basicConfig(level=logging.DEBUG)


class UserConnection:
    def __init__(self):
        self.channel = None
        self.user_name = None


def server():
    channel_server = ChannelServer(my_ip_address='127.0.0.1', my_ip_port=10000)
    channel_server.start_listening()
    user_connections = []
    server_data = {"users": []}

    while True:
        # Check for new connections
        channel = channel_server.get_new_channel()

        if channel:
            user_connection = UserConnection()
            user_connection.channel = channel
            user_connections.append(user_connection)

        # Service channels
        user_connections_to_remove = []
        for user_connection in user_connections:
            user_connection.channel.service_channel()
            if not user_connection.channel.receive_queue.empty():
                data = user_connection.channel.receive_queue.get()
                command = data["command"]
                logging.debug(command)
                if command == "login":
                    user_name = data["user_name"]
                    user_connection.user_name = user_name
                    server_data["users"].append(user_name)
                    channel_server.broadcast(server_data)
                    logging.debug(f"Log in from  {user_connection.user_name}")
                elif command == "logout":
                    logging.debug(f"Logout from {user_connection.user_name}")
                    user_connection.channel.close()
                    user_connections_to_remove.append(user_connection)
                    server_data["users"].remove(user_connection.user_name)
                    channel_server.broadcast(server_data)

        for user_connection in user_connections_to_remove:
            user_connections.remove(user_connection)
            logging.debug(f"Done with logout from {user_connection.user_name}")

        # Pause
        time.sleep(0.1)


server()
