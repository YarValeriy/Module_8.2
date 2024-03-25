import pika
from faker import Faker
from mongoengine import connect
from models import Contact

uri = "mongodb+srv://user_m8:567234@yarval.aryslwo.mongodb.net/?retryWrites=true&w=majority&appName=Yarval"

# Connect to MongoDB
# connect("module8", host="mongodb://localhost:27017/module8")
connect("module8", host=uri)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Declare a queue
# channel.queue_declare(queue="contact_queue")
channel.queue_declare(queue="sms_queue")
channel.queue_declare(queue="email_queue")


# Generate fake contacts and send them to RabbitMQ
fake = Faker("uk-UA")
for _ in range(10):  # Generate 10 fake contacts
    full_name = fake.name()
    email = fake.email()
    phone_number = fake.phone_number()
    preferred_method = fake.random_element(elements=("email", "sms"))

    contact = Contact(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        preferred_method=preferred_method,
    )
    contact.save()

    print(f"{contact.full_name}, {contact.email}, {contact.phone_number}")

    if preferred_method == 'email':
        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))
    else:
        channel.basic_publish(exchange='', routing_key='sms_queue', body=str(contact.id))

    print(f"Sent contact ID: {contact.id} to {preferred_method}")

# Close RabbitMQ connection
connection.close()
