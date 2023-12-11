import random
import time
import threading

from util import logging
from client import client_UDP
from .sensor import Sensor

class HumiditySensor(Sensor):
    def __init__(self, host, port):
        Sensor.__init__(self=self)
        self.socket = client_UDP.ClientUDP(host=host, port=port).socket
        self.alive_thread = self.create_alive_thread()

    def start(self):
        self.sender_thread.start()
        self.logger_thread.start()
        self.alive_thread.start()
        
        while True:
            start_time = time.time()
            humidity = self.generate()
            self.send_queue.put({"humidity": humidity})
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            time.sleep(sleep_time)

    def create_alive_thread(self):
        alive_thread = threading.Thread(target=self.send_alive)
        return alive_thread
    
    def generate(self):
        return random.randint(40,90)

    def send(self):
        while True:
            data = self.send_queue.get()
            humidity = data.get("humidity", None)
            if humidity > 80:
                self.client.socket.send(str(humidity).encode('utf-8'))
                self.log_queue.put((logging.send_humidity_log, {"humidity": humidity}))
    
    def send_alive(self):
        while True:
            time.sleep(3)
            self.log_queue.put((logging.send_alive, {}))
        
 
        
