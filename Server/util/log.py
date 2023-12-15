import logging
import sys

logging.basicConfig(filename="logs_server.log",
                    filemode='a',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    )
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def gateway_log(message: str):
    logging.info(f"Message received by server: {message}")