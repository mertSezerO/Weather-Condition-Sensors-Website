import random
import time
import threading
import queue

from util import logging
from client import client_UDP
from .sensor import Sensor

class HumiditySensor(Sensor):
    def __init__(self, host, port):
        Sensor.__init__(self=self, queue=queue.Queue())
        #self.client = client_UDP.ClientUDP(host=host, port=port, task=self.send)
        self.logger_thread = self.create_logger()
        self.alive_clock = 3
        self.start()

    def start(self):
        self.logger_thread.start()
        while True:
            self.alive_clock = self.alive_clock - 1
            start_time = time.time()
            hum = self.generate()
            #self.client.start()
            self.send(hum)
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            time.sleep(sleep_time)

    def generate(self):
        return random.randint(40,90)

    def send(self, hum: int):
        if hum > 80:
            #self.client.socket.send(str(hum).encode('utf-8'))
            self.log_queue.put((logging.send_humidity_log, {"hum": hum}))
        if self.alive_clock <= 0:
            #self.client.socket.send("ALIVE".encode('utf-8'))
            self.log_queue.put((logging.send_alive, {}))
            self.alive_clock = 3
 
        
