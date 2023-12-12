import threading
import queue
from abc import ABC, abstractmethod

class Sensor:
    def __init__(self) -> None:
        self.log_queue =  queue.Queue()
        self.send_queue = queue.Queue()
        self.logger_thread = self.create_logger()
        self.sender_thread = self.create_sender()
    
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
        sender_thread = threading.Thread(target=self.send)
        return sender_thread
    
    def create_logger(self) -> threading.Thread:
        logger_thread = threading.Thread(target=self.log)
        return logger_thread
    
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)