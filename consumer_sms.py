import pika
from mongoengine import connect
from models import Contact

uri = "mongodb+srv://user_m8:567234@yarval.aryslwo.mongodb.net/?retryWrites=true&w=majority&appName=Yarval"


def send_sms(contact_id):
    contact_id = contact_id.decode()
    # Simulate sending sms (stub function)
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending SMS to {contact.full_name} at {contact.phone_number}")
        contact.sent = True
        contact.save()
    else:
        print("Contact not found")


def callback(ch, method, properties, body):
    print("Received", body)
    send_sms(body)

# Connect to MongoDB
connect("module8", host=uri)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
# Declare the queue
channel.queue_declare(queue="sms_queue")
channel.basic_consume(queue="sms_queue", on_message_callback=callback, auto_ack=True)
print("Waiting for SMS contacts...")
channel.start_consuming()
