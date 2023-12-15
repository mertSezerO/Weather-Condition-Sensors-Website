import threading
import queue
import socket
import os
from dotenv import load_dotenv
from mongoengine import connect

from utils import Data, HttpHandler, HTTPServer

class Server:    
    def __init__(self, host='localhost', port=8080):
        load_dotenv()
        self.create_gateway_socket()
        self.create_http_socket()
        self.create_gateway_listener()
        self.create_store_thread()
        
        self.server_address = (host, port)
        self.http_server = HTTPServer(self.server_address, HttpHandler)
        
    def start(self):
        self.http_server.serve_forever()

    def stop(self):
        self.http_server.shutdown()
        self.http_server.server_close()
    
    def create_gateway_socket(self):
       self.gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.gateway_socket.bind()
       self.gateway_socket.listen(1)
    
    def create_http_socket(self):
        self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def create_gateway_listener(self):
        self.gateway_listener = threading.Thread(target=self.listen_gateway)
    
    def create_store_thread(self):
        self.store_queue = queue.Queue()
        self.storer = threading.Thread(target=self.store)
    
    def listen_gateway(self):
        while True:
            connection, (_,_) = self.gateway_socket.accept()
            if connection is not None:
                break
        while True:
            message = connection.recv(1024).decode('utf-8')
            self.store_queue.put({"Stored message is": message})
    
    def store(self):
        #connect to database
        database_url = os.getenv("DATABASE_URL")
        connect(database_url)
        while True:
            #popping from queue
            sensor_data = Data(field="", value=3 , timestamp="")
            sensor_data.save()