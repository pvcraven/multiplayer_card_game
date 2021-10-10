import time

from communications_channel import CommunicationsChannel


def test_server():
    channel = CommunicationsChannel(their_ip='127.0.0.1', their_port=10000)
    channel.connect()
    count = 0
    while True:
        count += 1
        if count % 20 == 0:
            data = f"{count//20}"
            channel.send_queue.put(data)
            print(f">>> {data}")

        channel.service_channel()
        time.sleep(0.1)
        if not channel.receive_queue.empty():
            data = channel.receive_queue.get()
            print(f"<<< {data}")


test_server()
