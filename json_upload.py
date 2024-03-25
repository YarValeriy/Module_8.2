import json
from mongoengine import connect
from models import Author, Quote
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine.errors import NotUniqueError


uri = "mongodb+srv://user_m8:567234@yarval.aryslwo.mongodb.net/?retryWrites=true&w=majority&appName=Yarval"


def upload_authors(authors_file):
    with open(authors_file, "r", encoding="utf-8") as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            try:
                author = Author(
                    fullname=author_data["fullname"],
                    born_date=author_data["born_date"],
                    born_location=author_data["born_location"],
                    description=author_data["description"],
                )
                author.save()
            except NotUniqueError:
                print(f"Author {author_data.get('fullname')} is already in the DB")


def upload_quotes(quotes_file):
    with open(quotes_file, "r", encoding="utf-8") as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data["author"]).first()
            if author:
                quote = Quote(
                    tags=quote_data["tags"], author=author, quote=quote_data["quote"]
                )
                quote.save()


if __name__ == "__main__":
   
    connect("module8", host= uri)
    upload_authors("authors.json")
    print("authors.json uploaded")
    upload_quotes("qoutes.json")
    print("qoutes.json uploaded")
