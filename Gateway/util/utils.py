import logging
import sys

logging.basicConfig(filename="logs_gateway.log",
                    filemode='a',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    )
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
def receive_humidity_log(humidity: int):
    logging.info(f"Humidity value received by Gateway: {humidity}")

def receive_temperature_log(temperature: int):
    logging.info(f"Temperature value received by Gateway: {temperature}")
    
def temperature_off_log():
    logging.info("TEMP SENSOR OFF")
    
def humidity_off_log():
    logging.info("HUMIDITY SENSOR OFF")