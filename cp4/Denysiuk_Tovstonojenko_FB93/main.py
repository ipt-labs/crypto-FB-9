import rsa_tools as rt
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)

subscriberA=rt.Subscriber("A", *rt.generate_key("A"))
subscriberB=rt.Subscriber("B", *rt.generate_key("B"))

subscriberA.set_public_key_of_comrade(subscriberB.get_public_key())
subscriberB.set_public_key_of_comrade(subscriberA.get_public_key())

k=rt.randint(1,rt.min_value_of_key)
logging.info(f"Chosen value for k:{k}")

sent_key=subscriberA.send_key(k)

if subscriberB.receive_key(*sent_key):
    sleep(0.2)
    print("Successfully sent a key")
else:
    print("Fail")
