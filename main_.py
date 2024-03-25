import threading
import time
import producer
import consumer_sms
import consumer_email


def run_producer():
    producer.main()  

def run_consumer_sms():
    consumer_sms.main()  

def run_consumer_email():
    consumer_email.main()

if __name__ == "__main__":
 
    producer_thread = threading.Thread(target=run_producer)
    consumer_sms_thread = threading.Thread(target=run_consumer_sms)
    consumer_email_thread = threading.Thread(target=run_consumer_email)


    producer_thread.start()
    consumer_sms_thread.start()
    consumer_email_thread.start()

    producer_thread.join()
    consumer_sms_thread.join()
    consumer_email_thread.join()
