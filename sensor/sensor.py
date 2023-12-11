import threading
import queue
from abc import ABC, abstractmethod

#add sender thread to sensor class for sending process
class Sensor:
    def __init__(self, log_queue: queue.Queue, send_queue: queue.Queue) -> None:
        self.log_queue =  log_queue
        self.send_queue = send_queue
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