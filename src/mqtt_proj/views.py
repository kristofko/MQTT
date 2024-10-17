from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .mq_client import MQTTClient
from .mongo_client import MongoClient

clients = {}

def get_mqtt_client(client_id) -> MQTTClient:
    if client_id not in clients:
        clients[client_id] = MQTTClient(client_id)
        clients[client_id].run()
    return clients[client_id]

@method_decorator(csrf_exempt, name='dispatch')
class ControlMQTTClient(View):
    def __init__(self) -> None:
        super().__init__()

    def post(self, 
             request: str = "", 
             client_id: str = "", 
             action: str = ""):
        mqtt_client = get_mqtt_client(client_id)

        if action == "start":
            mqtt_client.start_sending()
            return JsonResponse({'status': f'Client {client_id}: sending started'})
        elif action == "stop":
            mqtt_client.stop_sending()
            return JsonResponse({'status': f'Client {client_id}: sending stopped'})
        elif action == "visualise":
            mongo_client = MongoClient("mongodb://localhost:27017/")
            data = mongo_client.get_all_documents()
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)