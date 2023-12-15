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

from datetime import datetime
class Header():
    def __init__(self):
        self._data_type = None
    
    @property
    def data_type(self):
        return self._data_type
    
    @data_type.setter
    def data_type(self, type: str):
        self._data_type = type
        self.timestamp = datetime.now().strftime("%H:%M:%S")
    
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
