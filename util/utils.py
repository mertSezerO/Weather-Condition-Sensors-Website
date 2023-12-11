import logging
import sys

logging.basicConfig(filename="logs.log",
                    filemode='a',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    )
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def send_temperature_log(temp: int):
    logging.info(f"Temperature value sent to Gateway: {temp}")
    
def send_humidity_log(hum: int):
    logging.info(f"Humidity value sent to Gateway: {hum}")

def send_alive():
    logging.info(f"ALIVE message sent to Gateway")