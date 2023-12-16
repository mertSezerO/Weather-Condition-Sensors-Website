from http.server import SimpleHTTPRequestHandler, HTTPServer
from mongoengine import connect

from .model import get_humidity_data, get_temperature_data

class HttpHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        connect(db="Sensor", host="localhost", port=27017)
        if self.path == '/temperature':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        
            temperature_data = get_temperature_data()
            html_content = "<h1>Temperature Data</h1>"
            for temp in temperature_data:
                html_content += f"<p>{temp}</p>"
            
            self.wfile.write(html_content.encode())
            
        elif self.path == '/humidity':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            humidity_data = get_humidity_data()
            html_content = "<h1>Humidity Data</h1>"
            for temp in humidity_data:
                html_content += f"<p>{temp}</p>"
            
            self.wfile.write(html_content.encode())
            
        else:
            # Fallback to default behavior for other routes
            super().do_GET()
            
        