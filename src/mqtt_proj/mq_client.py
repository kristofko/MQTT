import paho.mqtt.client as mqtt
import requests
import time
import json

CA_CERT = "/etc/ssl/mosquitto/ca.crt"
CLIENT_CERT = "/etc/ssl/mosquitto/client.crt"
CLIENT_KEY = "/etc/ssl/mosquitto/client.key"

class MQTTClient():
    def __init__(self, client_id: str):
        self.client = mqtt.Client(client_id=client_id)
        self.client.tls_set(ca_certs=CA_CERT, 
                            certfile=CLIENT_CERT, 
                            keyfile=CLIENT_KEY)
        self.client.tls_insecure_set(True)
        self.client.connect("localhost", 8883, 300)
        self.sending_data = False

    def fetch_data(self) -> json:
        """
        Send request to the coincap api and return the obtained data as json.
        """
        url = 'https://api.coincap.io/v2/assets/bitcoin'
        response = requests.get(url)
        return response.json()

    def start_sending(self):
        """
        Command the MQTTCLient to start sending data to the network.
        """
        self.sending_data = True

    def stop_sending(self):
        """
        Command the MQTTClient to stop sending data.
        """
        self.sending_data = False

    def run(self):
        while True:
            if self.sending_data:
                data = self.fetch_data()
                data_json = json.dumps(data)
                print(f"Sending data {data_json}")
                self.client.publish("sensors/cryptocurrency", data_json)
                time.sleep(5) 
            time.sleep(1)

if __name__ == "__main__":
    mqtt_client = MQTTClient()
    mqtt_client.run()

