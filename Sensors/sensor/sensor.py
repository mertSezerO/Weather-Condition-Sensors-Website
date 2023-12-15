import threading
import queue
from abc import ABC, abstractmethod

class Sensor:
    def __init__(self) -> None:
        self.create_sender()
        self.create_logger()
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def generate(self):
        pass
    
    @abstractmethod
    def send(self):
        pass
    
    def create_sender(self):
        self.send_queue = queue.Queue()
        self.sender_thread = threading.Thread(target=self.send)
    
    def create_logger(self):
        self.log_queue =  queue.Queue()
        self.logger_thread = threading.Thread(target=self.log)
    
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)