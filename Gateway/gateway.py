import threading
import queue
import socket
import json

from util import logging, Datum
import time as time_module

class Gateway:
    def __init__(self, host="localhost", port_temp=3000, port_hum=3001, port_server=5000):    
        self.create_temperature_socket(host,port_temp)
        self.create_humidity_socket(host,port_hum)
        self.create_server_socket(host,port_server)
                
        self.create_humidity_listener()
        self.create_temperature_listener()
        self.create_sender()
        self.create_logger()
        self.create_temperature_clock()
        self.create_humidity_clock()
        
        self.temperature_alive = False
        self.humidity_alive = False
        self.temperature_terminated = False
        self.humidity_terminated = False
        
        self.start()
                     
    def start(self):
        self.humidity_listener_thread.start()
        self.temperature_listener_thread.start()
        self.logger_thread.start()
        self.humidity_clock_thread.start()
        self.temperature_clock_thread.start()
        self.sender.start()
        
    def create_humidity_listener(self):
        self.humidity_listener_thread = threading.Thread(target=self.listen_humidity)
    
    def create_temperature_listener(self):
        self.temperature_listener_thread = threading.Thread(target=self.listen_temperature)
    
    def create_sender(self):
        self.send_queue = queue.Queue()
        self.sender = threading.Thread(target=self.send)
    
    def create_logger(self):
        self.log_queue =  queue.Queue()
        self.logger_thread = threading.Thread(target=self.log)
    
    def create_humidity_clock(self):
        self.humidity_clock_thread = threading.Thread(target=self.start_humidity_clock)
    
    def create_temperature_clock(self):
        self.temperature_clock_thread = threading.Thread(target=self.start_temperature_clock)

    def create_temperature_socket(self, host, port):
        self.temperature_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.temperature_socket.bind((host, port))
        self.temperature_socket.listen(1)
    
    def create_humidity_socket(self, host, port):
        self.humidity_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.humidity_socket.bind((host, port))
        
    def create_server_socket(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((host,port))
    
    def listen_humidity(self):
        while True:
            if self.humidity_terminated:
                self.humidity_socket.close()
                break
            message,_ = self.humidity_socket.recvfrom(1024)
            message = message.decode('utf-8')
            if message is not None:
                if message == "ALIVE":
                    self.humidity_alive = True
                    self.log_queue.put((logging.receive_alive_log, {}))
                else:
                    self.log_queue.put((logging.receive_humidity_log, {"humidity": message}))
                    self.send_queue.put({"field":"humidity","value": message})
        
    def listen_temperature(self):
        while True:
            connection, (_,_) = self.temperature_socket.accept()
            if connection is not None:
                break

        while True:
            if self.temperature_terminated:
                self.temperature_socket.close()
                break
            message = connection.recv(1024).decode("utf-8")
            if message is not None:
                self.temperature_alive = True
                self.log_queue.put((logging.receive_temperature_log, {"temperature": message}))
                self.send_queue.put({"field":"temperature","value": message})

    
    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)           
    
    def start_humidity_clock(self):
        start_time = time_module.time()
        while True:
            if self.humidity_alive is False:
                current_time = time_module.time()
                passed_time = current_time- start_time
                if passed_time >= 7:
                    self.humidity_terminated = True
                    break
            else:
                self.humidity_alive = False
                start_time = time_module.time()
        self.log_queue.put((logging.humidity_off_log, {}))
        self.send_queue.put({"field":"humidity-off"})
        
    def start_temperature_clock(self):
        start_time = time_module.time()
        while True:
            if self.temperature_alive is False:
                current_time = time_module.time()
                passed_time = current_time- start_time
                if passed_time >= 3:
                    self.temperature_terminated = True
                    break
            else:
                self.temperature_alive = False
                start_time = time_module.time()
        self.log_queue.put((logging.temperature_off_log, {}))
        self.send_queue.put({"field":"temperature-off"})
        
    def send(self):
        while True:
            data = self.send_queue.get()
            data_type = data.get("field", None)
            data_value = data.get("value", None)
            if data_type == "temperature":
                self._send_weather_info("temperature", data_value)
            elif data_type == "humidity":
                self._send_weather_info("humidity", data_value)
            elif data_type == "temperature-off":
                self._send_sensor_info("temperature")
            else:
                self._send_sensor_info("humidity")
        
    def _send_weather_info(self, body_type, value):
        datum = Datum()
        datum.set_header_type("weather info")
        datum.set_body_type(body_type)
        datum.set_value(value)
        datum.set_message(f"{body_type} is now {value}")
        
        datum_json = json.dumps({
            'header': {
                'data_type': datum.header.data_type,
                'timestamp': datum.header.timestamp
            },
            'body': {
                'data_type': datum.body.data_type,
                'value': datum.body.value,
                'message': datum.body.message
            }
        })
        self.server_socket.send(datum_json.encode())
        self.log_queue.put((logging.send_weather_info_log, {}))
        
    
    def _send_sensor_info(self, body_type):
        datum = Datum()
        datum.set_header_type("sensor info")
        datum.set_body_type(body_type)
        datum.set_message(f"{body_type} Sensor OFF")
        
        datum_json = json.dumps({
            'header': {
                'data_type': datum.header.data_type,
                'timestamp': datum.header.timestamp
            },
            'body': {
                'data_type': datum.body.data_type,
                'message': datum.body.message
            }
        })
        self.server_socket.send(datum_json.encode())
        self.log_queue.put((logging.send_sensor_info_log, {}))

            