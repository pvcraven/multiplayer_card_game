import time
from server.server import Server


def main():
    server = Server("127.0.0.1", 10000)

    while True:
        # Check server
        server.server_check()
        # Pause
        time.sleep(0.1)


main()
