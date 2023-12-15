class Datum():
    def __init__(self):
        self.header = Header()
        self.body = Body()
    
    def set_header_type(self, datum_type: str):
        self.header.type = datum_type
    
    def set_data_type(self, data_type: str):
        self.body.type = data_type
        
    def set_value(self, value: int):
        self.body.value = value
    
    def set_message(self, message: str):
        self.body.message = message

class Header():
    def __init__(self):
        self._type = None
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type: str):
        self._type = type
    
class Body():
    def __init__(self):
        self._type = None
        self._value = None
        self._message = None
        
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type: str):
        self._type = type
    
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
