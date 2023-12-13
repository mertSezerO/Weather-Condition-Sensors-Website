import socket

class ClientTCP:
    def __init__(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            self.socket.bind((host,port))
    