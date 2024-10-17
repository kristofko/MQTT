import paho.mqtt.client as mqtt
import json

from pymongo import MongoClient
from mongo_client import MongoClient

CA_CERT = "/etc/ssl/mosquitto/ca.crt"
BROKER_CERT = "/etc/ssl/mosquitto/client.crt"
BROKER_KEY = "/etc/ssl/mosquitto/client.key"

class MQTTBroker():
    def __init__(self):
        self.collection = None
        self.broker_address = "localhost"
        self.mongo_client = MongoClient("mongodb://localhost:27017/")

    def on_message(self, client, userdata, message: mqtt.MQTTMessage):
        data = json.loads(message.payload.decode('utf-8'))
        self.mongo_client.insert_sensor(data)
        print(f"Stored in MongoDB: {data}")

    # MQTT Subscriber Configuration
    def on_connect(self, client: mqtt.Client, userdata, flags, rc: int):
        if rc == 0:
            print("Connected to broker")
            client.subscribe("sensors/cryptocurrency")  # Subscribe to the topic
        else:
            print("Connection failed with code", rc)

    def run(self):
        client = mqtt.Client(client_id="Broker1")
        client.tls_set(ca_certs=CA_CERT, 
                       certfile=BROKER_CERT, 
                       keyfile=BROKER_KEY)
        client.tls_insecure_set(True)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.broker_address, 8883)  # Use port 8883 for TLS
        client.loop_forever()

if __name__ == "__main__":
    mqtt_broker = MQTTBroker()
    mqtt_broker.run()