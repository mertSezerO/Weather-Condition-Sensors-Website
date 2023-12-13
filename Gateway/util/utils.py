import logging
import sys

logging.basicConfig(filename="logs_sensors.log",
                    filemode='a',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    )
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
def receive_humidity_log(humidity: int):
    logging.info(f"Humidity value received by Gateway: {humidity}")

