from django.urls import path
from .views import ControlMQTTClient

urlpatterns = [
    path("control/<str:client_id>/<str:action>/", ControlMQTTClient.as_view(), name="control_mqtt"),
    path("<str:action>", ControlMQTTClient.as_view(), name="visualize_mongo")
]
