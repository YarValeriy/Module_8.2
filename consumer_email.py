import pika
from mongoengine import connect
from models import Contact

uri = "mongodb+srv://user_m8:567234@yarval.aryslwo.mongodb.net/?retryWrites=true&w=majority&appName=Yarval"


def send_email(contact_id):
    contact_id = contact_id.decode()
    # Simulate sending email (stub function)
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending email to {contact.full_name} at {contact.email}")
        contact.sent = True
        contact.save()
    else:
        print("Contact not found")


def callback(ch, method, properties, body):
    print("Received", body)
    send_email(body)

# Connect to MongoDB
connect("module8", host=uri)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
# Declare the queue
channel.queue_declare(queue="email_queue")
channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)
print("Waiting for email contacts...")
channel.start_consuming()
