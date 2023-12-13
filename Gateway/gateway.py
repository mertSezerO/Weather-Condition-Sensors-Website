from client import client_TCP, client_UDP
import threading
import queue
from util import logging
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
        self.temperature_listener_thread = self.create_temperature_listener()
        self.logger_thread = self.create_logger()
        self.temperature_clock = self.create_clock_thread(3)
        self.humidity_clock = self.create_clock_thread(7)
             
    def start(self):
        self.humidity_listener_thread.start()
        self.temperature_listener_thread.start()
        self.logger_thread.start()
        
    def create_humidity_listener(self) -> threading.Thread:
        humidity_listener_thread = threading.Thread(target=self.listen_humidity)
        return humidity_listener_thread
    
    def create_temperature_listener(self) -> threading.Thread:
        temperature_listener_thread = threading.Thread(target=self.listen_temperature)
        return temperature_listener_thread
        
    def create_logger(self) -> threading.Thread:
        logger_thread = threading.Thread(target=self.log)
        return logger_thread
    
    def create_clock_thread(self, time: int):
        clock_thread = threading.Thread(target=self.startClock)
        clock_thread.time = time
        return clock_thread
    
    def listen_humidity(self):
        while True:
            message = self.udp_socket.recv(1024).decode('utf-8')
            self.log_queue.put((logging.receive_humidity_log, {"humidity": message}))
        
    def listen_temperature(self):
        while True:
            message = self.tcp_socket.recv(1024).decode("utf-8")
            self.log_queue.put((logging.receive_temperature_log, {"temperature": message}))
    
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)        
    
    def startClock(self):
        pass