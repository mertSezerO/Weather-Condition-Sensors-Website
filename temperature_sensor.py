import random
import time
import threading
import queue

from util import logging
from client import client_TCP

class TemperatureSensor:
    def __init__(self, host, port):
        self.client = client_TCP.ClientTCP(host, port, task=self.send_temperature)
        self.log_queue = queue.Queue()
        self.logger_thread = self.create_logger()
        self.start()
    
    def create_logger(self) -> threading.Thread:
        logger_thread = threading.Thread(target=self.log)
        return logger_thread
    
    def start(self):
        self.logger_thread.start()
        while True:
            start_time = time.time()
            temperature = self.generate_temperature()
            self.send_temperature(temperature)
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            time.sleep(sleep_time)
            
    def generate_temperature(self) -> int:
        return random.randint(20,30)
        
    def send_temperature(self, temp: int):
        client_TCP.socket.send(str(temp).encode('utf-8'))
        self.log_queue.put((logging.send_temperature_log, {"temp": temp}))
    
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)
