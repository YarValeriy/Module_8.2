import json
import mongoengine
import redis
import re
from models import Author, Quote
from redis_lru import RedisLRU

uri = "mongodb+srv://user_m8:567234@yarval.aryslwo.mongodb.net/?retryWrites=true&w=majority&appName=Yarval"

# Connect to MongoDB
# mongoengine.connect("module8", host="mongodb://localhost:27017/module8") - не працює. Чому?
# mongoengine.connect(db="module8", host="mongodb://localhost:27017", alias="default") - не працює. Чому?
mongoengine.connect("module8", host=uri)

# Connect to Redis

redis_client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(redis_client)

# Search function
@cache
def search_quotes(query):
    if query.startswith("name:"):
        # Search by author name
        author_name = query[len("name:") :].strip()
        cached_result = redis_client.get(f"author:{author_name}")
        if cached_result:
            return json.loads(cached_result.decode("utf-8"))
        else:
            author = Author.objects(
                fullname__iregex=f".*{re.escape(author_name)}.*"
            ).first()
            
            if author:
                quotes = Quote.objects(author=author)
                result = [
                    {
                        "author": quote.author.fullname,
                        "quote": quote.quote,
                        "tags": quote.tags,
                    }
                    for quote in quotes
                ]
                redis_client.setex(f"author:{author_name}", 3600, json.dumps(result))
                return result
            else:
                return "Author not found."
    elif query.startswith("tag:"):
        # Search by tag
        tag = query[len("tag:") :].strip()
        cached_result = redis_client.get(f"tag:{tag}")
        if cached_result:
            return json.loads(cached_result.decode("utf-8"))
        else:
            quotes = Quote.objects(tags__icontains=tag)
            result = [
                {
                    "author": quote.author.fullname,
                    "quote": quote.quote,
                    "tags": quote.tags,
                }
                for quote in quotes
            ]
            redis_client.setex(f"tag:{tag}", 3600, json.dumps(result))
            return result
    elif query.startswith("tags:"):
        # Search by multiple tags
        tags = query[len("tags:") :].strip().split(",")
        cached_result = redis_client.get(f"tags:{','.join(tags)}")
        if cached_result:
            return json.loads(cached_result.decode("utf-8"))
        else:
            quotes = Quote.objects(tags__all=tags)
            result = [
                {
                    "author": quote.author.fullname,
                    "quote": quote.quote,
                    "tags": quote.tags,
                }
                for quote in quotes
            ]
            redis_client.setex(f"tags:{','.join(tags)}", 3600, json.dumps(result))
            return result
    elif query == "exit":
        return None
    else:
        return "Invalid query."


# Infinite loop to accept commands
while True:
    query = input("Enter command: ")
    result = search_quotes(query)
    if result is None:
        break
    elif isinstance(result, list):
        for item in result:
            print(
                f'Author: {item["author"]}, Quote: {item["quote"]}, Tags: {", ".join(item["tags"])}'
            )
    else:
        print(result)
