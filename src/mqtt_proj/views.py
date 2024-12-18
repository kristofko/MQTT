from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .mq_client import MQTTClient
from .mongo_client import MongoClient

clients = {}

def get_mqtt_client(client_id: str) -> MQTTClient:
    """
    Get a MQTTClient instance by its id, if it does
    not exist create a new one with the passed id.
    
    Args:
        client_id: Id of the client
    """
    if client_id not in clients:
        clients[client_id] = MQTTClient(client_id)
        clients[client_id].run()
    return clients[client_id]

@method_decorator(csrf_exempt, name='dispatch')
class ControlMQTTClient(View):
    def __init__(self) -> None:
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        super().__init__()

    def post(self, request: str = "", client_id: str = "", 
             action: str = ""):
        
        mqtt_client = get_mqtt_client(client_id)
        print(action)
        if action == "start":
            mqtt_client.start_sending()
            return JsonResponse({'status': f'Client {client_id}: sending started'})
        elif action == "stop":
            mqtt_client.stop_sending()
            return JsonResponse({'status': f'Client {client_id}: sending stopped'})
        elif action == "visualise":
            print("HERE")
            data = self.mongo_client.get_all_documents()
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)