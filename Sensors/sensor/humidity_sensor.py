import random
import time
import threading
import socket

from util import logging
from .sensor import Sensor


class HumiditySensor(Sensor):
    def __init__(self, host="localhost", port=3001):
        Sensor.__init__(self=self)
        # Socket creation
        self.create_socket()
        self.host = host
        self.port = port

        # Special thread creation for ALIVE message
        self.create_alive_thread()

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def create_alive_thread(self):
        self.alive_thread = threading.Thread(target=self.send_alive)

    # Start method to start sensor
    def start(self):
        self.sender_thread.start()
        self.logger_thread.start()
        self.alive_thread.start()

        # Main thread is responsible for value generation
        while True:
            start_time = time.time()
            humidity = self.generate()
            self.send_queue.put({"humidity": humidity})
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            time.sleep(sleep_time)

    # Generates random humidity value
    def generate(self):
        return random.randint(40, 90)

    # Sends the generated humidity value to gateway if condition holds
    def send(self):
        while True:
            data = self.send_queue.get()
            humidity = data.get("humidity", None)
            if humidity > 80:
                self.socket.sendto(
                    str(humidity).encode("utf-8"), (self.host, self.port)
                )
                self.log_queue.put((logging.send_humidity_log, {"humidity": humidity}))

    # Sends alive message every 3 seconds
    def send_alive(self):
        while True:
            alive_time = time.time()
            self.socket.sendto(("ALIVE".encode("utf-8")), (self.host, self.port))
            self.log_queue.put((logging.send_alive, {}))
            elapsed_time = time.time() - alive_time
            sleep_time = max(0, 3 - elapsed_time)
            time.sleep(sleep_time)
