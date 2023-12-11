import random
import time
import threading
import queue

from util import logging
from client import client_TCP
from .sensor import Sensor

class TemperatureSensor(Sensor):
    def __init__(self, host, port):
        Sensor.__init__(self, queue=queue.Queue())
        self.client = client_TCP.ClientTCP(host, port, task=self.send)
        self.logger_thread = self.create_logger()
        self.start()
    
    def start(self):
        self.logger_thread.start()
        while True:
            start_time = time.time()
            temperature = self.generate()
            self.client.start()
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            time.sleep(sleep_time)
            
    def generate(self) -> int:
        return random.randint(20,30)
        
    def send(self, temp: int):
        self.client.socket.send(str(temp).encode('utf-8'))
        self.log_queue.put((logging.send_temperature_log, {"temp": temp}))
