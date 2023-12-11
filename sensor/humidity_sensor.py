import random
import time
import threading
import queue

from util import logging
from client import client_UDP

class HumiditySensor():
    def __init__(self, host, port):
        self.client = client_UDP.ClientUDP(host=host, port=port)

    def start(self):
        pass