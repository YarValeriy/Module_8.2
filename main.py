import threading
import producer
import consumer_email
import consumer_sms

# Start producer.py in a separate thread
producer_thread = threading.Thread(target=producer.main)
producer_thread.start()

# Start consumer_email.py in a separate thread
email_thread = threading.Thread(target=consumer_email.main)
email_thread.start()

# Start consumer_sms.py in the main thread
consumer_sms.main()
