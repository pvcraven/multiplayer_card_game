import time

from communications_channel import CommunicationsChannel


def test_client():
    user_name = input("What is your name? ")
    data = {"user_name": user_name}

    channel = CommunicationsChannel(their_ip='127.0.0.1', their_port=10000)
    channel.connect()

    channel.send_queue.put(data)

    while True:
        channel.service_channel()
        if not channel.receive_queue.empty():
            data = channel.receive_queue.get()
            print(f"<<< {data}")

        time.sleep(0.1)


test_client()
