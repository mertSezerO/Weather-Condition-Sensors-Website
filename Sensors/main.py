import threading

from sensor.temperature_sensor import TemperatureSensor
from sensor.humidity_sensor import HumiditySensor

temperature_sensor = TemperatureSensor("host",8080)
humidity_sensor = HumiditySensor("host", 8080)

temperature_thread = threading.Thread(target=temperature_sensor.start)
humidity_thread = threading.Thread(target=humidity_sensor.start)

temperature_thread.start()
humidity_thread.start()