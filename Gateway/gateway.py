from client import client_TCP, client_UDP
import threading
import queue
from util import logging

class Gateway:
    def __init__(self, host, port):
        self.log_queue =  queue.Queue()
        #self.send_queue = queue.Queue() 
        self.tcp_socket = client_TCP.ClientTCP(host=host, port=port).socket
        self.udp_socket = client_UDP.ClientUDP(host=host, port=port).socket
        self.humidity_listener_thread = self.create_humidity_listener()
        self.logger_thread = self.create_logger()
             
    def start(self):
        self.humidity_listener_thread.start()
        self.logger_thread.start()
        
    def create_humidity_listener_thread(self) -> threading.Thread:
        humidity_listener_thread = threading.Thread(target=self.listen_humidity)
        return humidity_listener_thread
    
    def listen_humidity(self):
        while True:
            message = self.udp_socket.recv(1024).decode('utf-8')
            log_queue.put((logging.receive_humidity_log, {"humidity": message}))
    
    def create_logger(self) -> threading.Thread:
        logger_thread = threading.Thread(target=self.log)
        return logger_thread
    
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)
