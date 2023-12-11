from threading import Thread
import socket

class ClientTCP(Thread):
    def __init__(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            self.socket.connect((self.server_host, self.server_port))