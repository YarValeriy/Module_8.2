import pika
from mongoengine import connect
from models import Contact

uri = "mongodb+srv://user_m8:567234@yarval.aryslwo.mongodb.net/?retryWrites=true&w=majority&appName=Yarval"

# Connect to MongoDB
connect("module8", host=uri)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue="contact_queue")


def send_email(contact_id):
    # Simulate sending email (stub function)
    print(f"Sending email to contact with ID: {contact_id}")

    # Update the sent status of the contact to True
    contact = Contact.objects.get(id=contact_id.decode())
    contact.sent = True
    contact.save()
    print(f"Updated sent status of contact with ID {contact_id.decode()} to True")


def callback(ch, method, properties, body):
    print(" [x] Received", body)
    send_email(body)


# Consume messages from RabbitMQ
channel.basic_consume(
    queue="contact_queue", on_message_callback=callback, auto_ack=True
)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
