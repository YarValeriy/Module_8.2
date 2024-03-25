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


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField()
    sent = BooleanField(default=False)
    preferred_method = StringField(choices=["email", "sms"], default="email")
    meta = {"collection": "contacts"}
