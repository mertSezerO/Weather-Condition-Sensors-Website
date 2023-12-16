import random
import time
import socket

from util import logging
from .sensor import Sensor

class TemperatureSensor(Sensor):
    def __init__(self, host="localhost", port=3000):
        Sensor.__init__(self=self)
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
    
    def start(self):
        self.sender_thread.start()
        self.logger_thread.start()
        
        while True:
            start_time = time.time()
            temperature = self.generate()
            self.send_queue.put({"temperature": temperature})
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            time.sleep(sleep_time)
            
    def generate(self) -> int:
        return random.randint(20,30)
        
    def send(self):
        while True:
            data = self.send_queue.get()
            temperature = data.get("temperature", None)
            self.socket.send(str(temperature).encode('utf-8'))
            self.log_queue.put((logging.send_temperature_log, {"temperature": temperature}))
