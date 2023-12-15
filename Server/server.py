import threading
import queue
import socket
from http.server import SimpleHTTPRequestHandler, HTTPServer

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/temperature':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        
            temperature_data = [25, 28, 30, 27]
            html_content = "<h1>Temperature Data</h1>"
            for temp in temperature_data:
                html_content += f"<p>{temp}</p>"
            
            self.wfile.write(html_content.encode())
            
        elif self.path == '/humidity':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            humidity_data = [40, 50, 60, 70]
            html_content = "<h1>Humidity Data</h1>"
            for temp in humidity_data:
                html_content += f"<p>{temp}</p>"
            
            self.wfile.write(html_content.encode())
            
        else:
            # Fallback to default behavior for other routes
            super().do_GET()
        
class Server:    
    def __init__(self, host='localhost', port=8080):
        self.store_queue = queue.Queue()
        
        self.create_gateway_socket()
        self.create_http_socket()
        self.create_gateway_listener()
        
        self.server_address = (host, port)
        self.http_server = HTTPServer(self.server_address, CustomRequestHandler)
        
    def start(self):
        self.http_server.serve_forever()

    def stop(self):
        self.http_server.shutdown()
        self.http_server.server_close()
    
    def create_gateway_socket(self):
       self.gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.gateway_socket.bind()
       self.gateway_socket.listen(1)
    
    def create_http_socket(self):
        self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def create_gateway_listener(self):
        self.gateway_listener = threading.Thread(target=self.listen_gateway)
    
    def listen_gateway(self):
        while True:
            connection, (_,_) = self.gateway_socket.accept()
            if connection is not None:
                break
        while True:
            message = connection.recv(1024).decode('utf-8')
            self.store_queue.put({"Stored message is": message})