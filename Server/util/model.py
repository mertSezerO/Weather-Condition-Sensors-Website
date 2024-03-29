from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='api_key.env')

database_uri = os.getenv("DATABASE_URI")
client = MongoClient(database_uri)

database = client['Sensor']
data_collection = database['data']
info_collection = database['info']

def insert_data(data_type, data_value, timestamp):
    data_document = {
        'type': data_type,
        'value': data_value,
        'timestamp': timestamp
    }
    data_collection.insert_one(data_document)

def insert_info(info_type, info_message):
    info_document = {
        'type': info_type,
        'message': info_message
    }
    info_collection.insert_one(info_document)

def get_humidity_data():
    humidity_data = []
    for document in data_collection.find({"type": "humidity"}):
        humidity_data.append(document["value"])
    return humidity_data

def get_temperature_data():
    temperature_data = []
    for document in data_collection.find({"type": "temperature"}):
        temperature_data.append(document["value"])
    return temperature_data