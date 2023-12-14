import threading
import queue
import socket

class Server:
    def __init__(self, host='localhost', port=8080):
        self.create_gateway_socket()
        self.create_http_socket()
        
        self.create_gateway_listener()
    
    def create_gateway_socket(self):
        self.gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def create_http_socket(self):
        self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def create_gateway_listener(self):
        self.gateway_listener = threading.Thread(target=self.listen)
    
    def listen(self):
        pass