import socket

class ClientUDP:
    def __init__(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as self.socket:
            self.socket.connect((host,port))