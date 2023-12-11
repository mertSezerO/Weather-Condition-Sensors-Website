import random
import time
import threading
import queue

from util import logging
from client import client_TCP
from .sensor import Sensor

class TemperatureSensor(Sensor):
    def __init__(self, host, port):
        Sensor.__init__(self=self, log_queue=queue.Queue(), send_queue=queue.Queue())
        self.socket = client_TCP.ClientTCP(host, port).socket
        self.start()
    
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
            self.client.socket.send(str(temperature).encode('utf-8'))
            self.log_queue.put((logging.send_temperature_log, {"temperature": temperature}))
