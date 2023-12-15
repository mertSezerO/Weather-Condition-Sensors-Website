class Datum():
    def __init__(self):
        self.header = Header()
        self.body = Body()
    
    def set_header_type(self, data_type: str):
        self.header.data_type = data_type
    
    def set_body_type(self, data_type: str):
        self.body.data_type = data_type
        
    def set_value(self, value: int):
        self.body.value = value
    
    def set_message(self, message: str):
        self.body.message = message
    
    @classmethod
    def from_dict(cls, data_dict):
        datum_instance = cls()
        header_dict = data_dict.get('header', {})
        body_dict = data_dict.get('body', {})

        datum_instance.header.data_type = header_dict.get('data_type', None)
        datum_instance.header.timestamp = header_dict.get('timestamp', None)

        datum_instance.body.data_type = body_dict.get('data_type', None)
        datum_instance.body.value = body_dict.get('value', None)
        datum_instance.body.message = body_dict.get('message', None)

        return datum_instance

from datetime import datetime
class Header():
    def __init__(self):
        self._data_type = None
        self.timestamp = datetime.now().strftime("%H:%M:%S")
    
    @property
    def data_type(self):
        return self._data_type
    
    @data_type.setter
    def data_type(self, type: str):
        self._data_type = type
    
class Body():
    def __init__(self):
        self._data_type = None
        self._value = None
        self._message = None
        
    @property
    def data_type(self):
        return self._data_type
    
    @data_type.setter
    def data_type(self, type: str):
        self._data_type = type
    
    @property
    def value(self):
        return self._value
    
    @value.setter    
    def value(self, value: int):
        self._value = value
    
    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self, message: str):
        self._message = message
