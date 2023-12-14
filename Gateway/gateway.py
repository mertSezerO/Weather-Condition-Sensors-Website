import threading
import queue
import socket

from util import logging
import time as time_module

class Gateway:
    def __init__(self, host, port_temp, port_hum):
        self.log_queue =  queue.Queue()
        self.send_queue = queue.Queue() 
        
        self.temperature_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.temperature_socket.bind((host, port_temp))
        self.temperature_socket.listen(1)
        
        self.humidity_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.humidity_socket.bind((host, port_hum))
        
        self.create_humidity_listener()
        self.create_temperature_listener()
        self.create_logger()
        self.create_temperature_clock()
        self.create_humidity_clock()
        
        self.temperature_alive = False
        self.humidity_alive = False
        self.temperature_terminated = False
        self.humidity_terminated = False
        self.start()
                     
    def start(self):
        self.humidity_listener_thread.start()
        self.temperature_listener_thread.start()
        self.logger_thread.start()
        self.humidity_clock_thread.start()
        self.temperature_clock_thread.start()
        
    def create_humidity_listener(self):
        self.humidity_listener_thread = threading.Thread(target=self.listen_humidity)
    
    def create_temperature_listener(self):
        self.temperature_listener_thread = threading.Thread(target=self.listen_temperature)
        
    def create_logger(self):
        self.logger_thread = threading.Thread(target=self.log)
    
    def create_humidity_clock(self):
        self.humidity_clock_thread = threading.Thread(target=self.start_humidity_clock)
    
    def create_temperature_clock(self):
        self.temperature_clock_thread = threading.Thread(target=self.start_temperature_clock)

    def listen_humidity(self):
        while True:
            if self.humidity_terminated:
                self.humidity_socket.close()
                break
            message,_ = self.humidity_socket.recvfrom(1024)
            message = message.decode('utf-8')
            if message is not None:
                self.humidity_alive = True
                self.log_queue.put((logging.receive_humidity_log, {"humidity": message}))
        
    def listen_temperature(self):
        while True:
            connection, (_,_) = self.temperature_socket.accept()
            if connection is not None:
                break

        while True:
            if self.temperature_terminated:
                self.temperature_socket.close()
                break
            message = connection.recv(1024).decode("utf-8")
            if message is not None:
                self.temperature_alive = True
                self.log_queue.put((logging.receive_temperature_log, {"temperature": message}))
    
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)        
    
    def start_temperature_clock(self):
        start_time = time_module.time()
        while True:
            if self.temperature_alive is False:
                current_time = time_module.time()
                passed_time = current_time- start_time
                if passed_time >= 3:
                    self.temperature_terminated = True
                    break
            else:
                self.temperature_alive = False
                start_time = time_module.time()
        self.log_queue.put((logging.temperature_off_log, {}))         
    
    def start_humidity_clock(self):
        start_time = time_module.time()
        while True:
            if self.humidity_alive is False:
                current_time = time_module.time()
                passed_time = current_time- start_time
                if passed_time >= 7:
                    self.humidity_terminated = True
                    break
            else:
                self.humidity_alive = False
                start_time = time_module.time()
        self.log_queue.put((logging.humidity_off_log, {}))