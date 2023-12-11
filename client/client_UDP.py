from threading import Thread
import socket

class ClientUDP(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as self.socket:
            self.socket.connect((host,port))