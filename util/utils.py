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
    logging.info(f"Temperature sent to Gateway: {temp}")