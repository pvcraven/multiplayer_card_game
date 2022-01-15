import socket
import queue
import json
import logging

from network.constants import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CommunicationsChannel:

    def __init__(self,
                 my_ip_address=None,
                 my_ip_port=None,
                 their_ip=None,
                 their_port=None):

        self.my_ip_address = my_ip_address
        self.my_ip_port = my_ip_port
        self.their_ip = their_ip
        self.their_port = their_port
        self.current_state = NO_CONNECTION

        self.my_socket = None
        self.connection = None
        self.receive_queue = queue.Queue()
        self.send_queue = queue.Queue()

    def connect(self):
        logger.debug(f"Connecting {self.their_ip}:{self.their_port}...")
        # Create a socket for IPv4 (AF_INET), TCP stream (SOCK_STREAM)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to this specified server and port
        # Note that Python expects ip and port as a list
        destination = (self.their_ip, self.their_port)
        self.my_socket.connect(destination)
        self.my_socket.settimeout(0.0)
        self.current_state = CONNECTED
        self.connection = self.my_socket
        logger.debug("Connected.")

    def service_channel(self):

        # If we have a connection, receive data
        if self.current_state == CONNECTED:
            try:
                # Read in the data, up to the number of characters in BUFFER_SIZE
                data = self.connection.recv(BUFFER_SIZE)

                # See if we have data
                if len(data) > 0:
                    logger.debug(f"Receiving data...")
                    # Decode the byte string to a normal string
                    data_string = data.decode("UTF-8")
                    decoded_data = json.loads(data_string)

                    # Print what we read in, and from where
                    # print(f"Data from {self.client_ip}:{self.client_port} --> '{data_string}'")
                    self.receive_queue.put(decoded_data)
                    logger.debug(f"<<< {decoded_data}")

                # self.current_state = NO_CONNECTION
                # self.connection.close()

            except BlockingIOError:
                # There was no data. Wait before checking again.
                pass

        if self.current_state == CONNECTED and not self.send_queue.empty():
            data = self.send_queue.get()
            logger.debug(f">>> {data}")
            encoded_data = json.JSONEncoder().encode(data).encode('utf-8')
            self.connection.sendall(encoded_data)
            logger.debug(">>> Data sent")

    def close(self):
        logger.debug("--- Close connection requested.")
        if self.connection:
            logger.debug("--- Closing.")
            self.connection.close()
            logger.debug("--- Closed.")

        self.connection = None
        self.current_state = NO_CONNECTION
