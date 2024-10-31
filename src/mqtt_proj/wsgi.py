import threading
import time
from .modbus_client import ModbusClient
from .modbus_server import ModbusServer
from .mq_broker import MQTTBroker
from django.core.wsgi import get_wsgi_application
from .views import get_mqtt_client


application = get_wsgi_application()

def start_mqtt_client(client_id):
    client = get_mqtt_client(client_id)
    client.run()

def start_broker():
    server = MQTTBroker()
    server.run()

def start_modbus_server():
    server = ModbusServer()
    server.run()

def start_modbus_client():
    time.sleep(2)
    client = ModbusClient()
    client.run()


threading.Thread(target=start_broker, daemon=True).start()
client_ids = ["Client1", "Client2", "Client3"]  
for client_id in client_ids:
    threading.Thread(target=start_mqtt_client, args=(client_id,), daemon=True).start()

threading.Thread(target=start_modbus_server, daemon=True).start()
threading.Thread(target=start_modbus_client, daemon=True).start()
