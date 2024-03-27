from bson import json_util
from mongoengine import (
    connect,
    Document,
    StringField,
    ReferenceField,
    ListField,
    BooleanField,
    EmailField,
    CASCADE,
)

uri = "mongodb+srv://user_m8:567234@yarval.aryslwo.mongodb.net/?retryWrites=true&w=majority&appName=Yarval"
connect("module8", host= uri)
# connect("module8", host="mongodb://localhost:27017") # НЕ ПРАЦЮЄ! ЧОМУ?

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=40))
    quote = StringField()
    meta = {"collection": "quotes"}


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField()
    sent = BooleanField(default=False)
    preferred_method = StringField(choices=["email", "sms"], default="email")
    meta = {"collection": "contacts"}
