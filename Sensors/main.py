import threading

from sensor.temperature_sensor import TemperatureSensor
from sensor.humidity_sensor import HumiditySensor

humidity_sensor = HumiditySensor("localhost", 3000)
temperature_sensor = TemperatureSensor("localhost",3001)

temperature_thread = threading.Thread(target=temperature_sensor.start)
humidity_thread = threading.Thread(target=humidity_sensor.start)

temperature_thread.start()
humidity_thread.start()