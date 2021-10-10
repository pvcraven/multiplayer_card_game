import socket

from constants import *
from communications_channel import CommunicationsChannel


class Server:

    def __init__(self,
                 my_ip_address=None,
                 my_ip_port=None):

        self.my_ip_address = my_ip_address
        self.my_ip_port = my_ip_port
        self.my_socket = None

    def start_listening(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.settimeout(0.0)
        listen_to = (self.my_ip_address, self.my_ip_port)
        self.my_socket.bind(listen_to)
        self.my_socket.listen(2)

    def get_new_channel(self):

        try:
            # Get a connection, and the address that hooked up to us.
            # The 'client address' is an array that has the IP and the port.
            connection, client_address = self.my_socket.accept()
            their_ip = client_address[0]
            their_port = client_address[1]

            communications_channel = CommunicationsChannel()
            communications_channel.connection = connection
            communications_channel.their_ip = their_ip
            communications_channel.their_port = their_port
            communications_channel.my_ip_address = self.my_ip_address
            communications_channel.my_ip_port = self.my_ip_port
            communications_channel.current_state = CONNECTED
            print("Client connected...")
            return communications_channel

        except BlockingIOError:
            # There was no connection. Wait before checking again.
            return None