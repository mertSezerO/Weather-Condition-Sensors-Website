import socket
import random
import time

class TemperatureSensor:
    def __init__(self):
        self.start()
    
    def start(self):
        while True:
            temperature = self.generate_temperature()
            self.send_temperature(temperature)
            time.sleep(1)
            
    def generate_temperature(self) -> int:
        return random.randint(20,30)
        
    def send_temperature(self, temp: int):
        pass