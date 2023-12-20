import threading
import queue
import socket
import json

from util import insert_info, insert_data, get_temperature_data, get_humidity_data
from util import logging, Datum


class Server:
    def __init__(self, host="localhost", port=8080, port_gateway=5000):
        self.create_gateway_socket(host, port_gateway)
        self.create_http_socket(host, port)

        self.create_gateway_listener()
        self.create_http_listener()
        self.create_http_handler()

        self.create_store_thread()
        self.create_logger()

        self.start()

    def start(self):
        self.gateway_listener.start()
        self.http_listener.start()
        self.http_handler.start()
        self.storer.start()
        self.logger_thread.start()

    def create_gateway_socket(self, host, port):
        self.gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gateway_socket.bind((host, port))
        self.gateway_socket.listen(1)

    def create_http_socket(self, host, port):
        self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.http_socket.bind((host, port))
        self.http_socket.listen(0)

    def create_gateway_listener(self):
        self.gateway_listener = threading.Thread(target=self.listen_gateway)

    def create_http_listener(self):
        self.http_listener = threading.Thread(target=self.listen_http)
        self.client_queue = queue.Queue()

    def create_http_handler(self):
        self.http_handler = threading.Thread(target=self.handle_http)

    def create_store_thread(self):
        self.store_queue = queue.Queue()
        self.storer = threading.Thread(target=self.store)

    def create_logger(self):
        self.log_queue = queue.Queue()
        self.logger_thread = threading.Thread(target=self.log)

    def listen_gateway(self):
        while True:
            connection, (_, _) = self.gateway_socket.accept()
            if connection is not None:
                break

        while True:
            json_message = connection.recv(1024).decode()
            if json_message is not None:
                try:
                    message_dict = json.loads(json_message)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    continue
                message = Datum.from_dict(message_dict)
                self.store_queue.put({"message": message})
                self.log_queue.put(
                    (logging.gateway_log, {"message": message.body.message})
                )

    def listen_http(self):
        while True:
            connection, address = self.http_socket.accept()
            if connection is not None:
                self.client_queue.put({"client_socket": connection, "address": address})

    def handle_http(self):
        while True:
            data = self.client_queue.get()
            client_socket = data.get("client_socket", None)
            address = data.get("address", None)
            message = client_socket.recv(1024).decode("utf-8")
            path = self.extract_path(message)
            if path == "/temperature":
                temperature_list = get_temperature_data()
                html = "<h1>Temperature Data</h1>"
                for temperature in temperature_list:
                    html += f"<p>{temperature}</p>"
            elif path == "/humidity":
                humidity_list = get_humidity_data()
                html = "<h1>Humidity Data</h1>"
                for humidity in humidity_list:
                    html += f"<p>{humidity}</p>"
            else:
                html = "<h1>Invalid request</h1>"

            status_line = "HTTP/1.1 200 OK\r\n"
            content_type = "text/html; charset=utf-8"
            content_length = len(html)
            headers = f"Content-Type: {content_type}\r\nContent-Length: {content_length}\r\n\r\n"
            response = status_line + headers + html
            client_socket.sendall(response.encode())

    def extract_path(self, request):
        request_lines = request.split(" ")
        return request_lines[1]

    def store(self):
        while True:
            data = self.store_queue.get()
            report = data.get("message", None)
            if report.header.data_type == "weather info":
                insert_data(
                    data_type=report.body.data_type,
                    data_value=report.body.value,
                    timestamp=report.header.timestamp,
                )
            else:
                insert_info(
                    info_type=report.body.data_type, info_message=report.body.message
                )

    def log(self):
        while True:
            log_task, args = self.log_queue.get()
            log_task(**args)
