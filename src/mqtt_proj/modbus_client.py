import time
from pymodbus.client import ModbusTcpClient
from .mongo_client import MongoClient


class ModbusClient:
    def __init__(self):
        # Connect to the Modbus TCP server
        self.client = ModbusTcpClient('localhost', port=5020)
        self.mongo_client = MongoClient("mongodb://localhost:27017/")

    def run(self):
        connected = self.client.connect()
        if not connected:
            msg = "Could not connect to the modbus infrastructure"
            print(msg)
            exit(1) 

        try:
            while True:
                response = self.client.read_holding_registers(0, 1)
                if response.isError():
                    print(f"Error reading holding registers")
                else:
                    print(f"Holding Register 0: {response.registers[0]}")
                    data = {"value": response.registers[0]}
                    self.mongo_client.insert_modbus(data)
                time.sleep(5)

        finally:
            self.mongo_client.close()
            self.client.close()

if __name__ == "__main__":
    client = ModbusClient()
    client.run()