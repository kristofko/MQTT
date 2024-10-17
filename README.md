# MQTT, ModbusTCP and Django Integration Project

This project integrates an MQTT client with a Django web application. It allows sending and receiving data via MQTT messages. The project utilizes the Mosquitto broker for MQTT communication and stores data in a MongoDB database.

## Getting Started

### Prerequisites

1. Ensure you have Python 3.x installed on your system. (Mine was run with 3.12.3)
2. Install the necessary Python packages:
   ```bash
   pip install django paho-mqtt pymongo
   ```
   You might need to install more dependencies depending on your setup.
3. Make sure you have running mosquitto broker on you computer with the correct configuration ( Configure to run on port 8883 for tls support and also that the certificates and keys are present ).
4. Navigate to src folder and execute
5. ```bash
   python3 manage.py runserver
   ```
   , which will start the django server and after that you can start using some endpoints to check the resulting functionality.

### Endpoints

To start or stop capture on any specific device (you need to know the device id, right now the devices are Called Client1, Client2 and Client3) : 
```bash
curl -X POST http://127.0.0.1:8000/control/Client2/start/
```

To visualise current entries in mongo database
```bash
curl -X POST http://localhost:8000/visualise
```
