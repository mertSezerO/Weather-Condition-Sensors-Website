import threading
import queue
from abc import ABC, abstractmethod

class Sensor:
    def __init__(self, queue: queue.Queue) -> None:
        self.log_queue =  queue
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def generate(self):
        pass
    
    @abstractmethod
    def send(self):
        pass
    
    def create_logger(self) -> threading.Thread:
        logger_thread = threading.Thread(target=self.log)
        return logger_thread
    
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)