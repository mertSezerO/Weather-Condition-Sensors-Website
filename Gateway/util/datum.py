# Our Protocol's Class Implementation
"""
It includes a header and a body which are also objects defined below.
We want it to be as modular as possible. Thus in creation, all fields
are set to None by default. They can then be filled with real data according to data type
of the message.
"""


class Datum:
    def __init__(self):
        self.header = Header()
        self.body = Body()

    # Sets header as either 'weather info' or 'sensor info'
    def set_header_type(self, data_type: str):
        self.header.data_type = data_type

    # Sets body as either 'temperature' or 'humidity' to notify the info type
    def set_body_type(self, data_type: str):
        self.body.data_type = data_type

    # Sets if weather info, holds numerical value of type
    def set_value(self, value: int):
        self.body.value = value

    # Sets message of sending datum
    def set_message(self, message: str):
        self.body.message = message


from datetime import datetime


class Header:
    def __init__(self):
        self._data_type = None
        self.timestamp = datetime.now().strftime("%H:%M:%S")

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, type: str):
        self._data_type = type


class Body:
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
