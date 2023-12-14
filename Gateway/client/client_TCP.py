import socket

class ClientTCP:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
    
    @property
    def get_socket(self):
        return self.socket