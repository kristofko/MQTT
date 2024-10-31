import threading
from .modbus_client import ModbusClient
from .modbus_server import ModbusServer
from django.core.wsgi import get_wsgi_application
from .views import get_mqtt_client


application = get_wsgi_application()

def start_mqtt_client(client_id):
    client = get_mqtt_client(client_id)
    client.run()

client_ids = ["Client1", "Client2", "Client3"]  
for client_id in client_ids:
    threading.Thread(target=start_mqtt_client, args=(client_id,), daemon=True).start()

ModbusServer()
ModbusClient().run()

