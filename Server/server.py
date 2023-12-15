import threading
import queue
import socket
import os
from dotenv import load_dotenv
from mongoengine import connect

from util import Data, Info, HttpHandler, HTTPServer, logging

class Server:    
    def __init__(self, host='localhost', port=8080):
        load_dotenv(dotenv_path="api_key.env")
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
    
    def create_logger(self):
        self.log_queue = queue.Queue()
        self.logger_thread = threading.Thread(target=self.log)
    
    def listen_gateway(self):
        while True:
            connection, (_,_) = self.gateway_socket.accept()
            if connection is not None:
                break
        while True:
            message = connection.recv(1024)
            self.store_queue.put({"message": message})
            self.log_queue.put((logging.gateway_log, message.body.message))
            
    
    def store(self):
        database_url = os.getenv("DATABASE_URI")
        connect(database_url)
        
        while True:
            data = self.store_queue.get()
            report = data.get("message", None)
            if report.header.data_type == "weather info":
                sensor_data = Data(type=report.body.data_type, value=report.body.value , timestamp=report.header.timestamp)
                sensor_data.save()
            else:
                sensor_info = Info(type=report.body.data_type, message= report.body.message)
                sensor_info.save()
                
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)   