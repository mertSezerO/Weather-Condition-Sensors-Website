import logging
import sys

logging.basicConfig(filename="logs.log",
                    filemode='a',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    )
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def send_temperature_log(temperature: int):
    logging.info(f"Temperature value sent to Gateway: {temperature}")
    
def send_humidity_log(humidity: int):
    logging.info(f"Humidity value sent to Gateway: {humidity}")

def send_alive():
    logging.info(f"ALIVE message sent to Gateway")