import time

from server import Server


def test_server():
    server = Server(my_ip_address='127.0.0.1', my_ip_port=10000)
    server.start_listening()
    channels = []
    server_data = {"users": []}

    while True:
        # Check for new connections
        channel = server.get_new_channel()
        if channel:
            channels.append(channel)

        # Service channels
        for channel in channels:
            channel.service_channel()
            if not channel.receive_queue.empty():
                data = channel.receive_queue.get()
                user = data["user_name"]
                server_data["users"].append(user)
                server.broadcast(server_data)

        # Pause
        time.sleep(0.1)


test_server()
