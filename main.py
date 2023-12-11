from sensor.temperature_sensor import TemperatureSensor
from sensor.humidity_sensor import HumiditySensor
#return socket for udp and tcp
#sensor = TemperatureSensor("host",8080)
sensor = HumiditySensor("host", 8080)