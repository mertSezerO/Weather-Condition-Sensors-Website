from mongoengine import Document, StringField, IntField

class Data(Document):
    type = StringField(required=True)
    value = IntField(required=True)
    timestamp = StringField(required=True)