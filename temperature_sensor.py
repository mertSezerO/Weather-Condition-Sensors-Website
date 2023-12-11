import socket
import random
import time

from util import logger
from client import client_TCP

class TemperatureSensor:
    def __init__(self, host, port):
        self.client = client_TCP.ClientTCP(host, port)
        self.start()
    
    def start(self):
        while True:
            start_time = time.time()
            temperature = self.generate_temperature()
            self.send_temperature(temperature)
            print(temperature)
            logger.send_temperature_log(temp=temperature)
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            time.sleep(sleep_time)
            
    def generate_temperature(self) -> int:
        return random.randint(20,30)
        
    def send_temperature(self, temp: int):
        pass

