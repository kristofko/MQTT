from pymodbus.client import ModbusTcpClient
from mongo_client import MongoClient
import time


class ModbusClient:
    def __init__(self):
        # Connect to the Modbus TCP server
        client = ModbusTcpClient('localhost', port=5020)
        client.connect()
        mongo_client = MongoClient("mongodb://localhost:27017/")

        try:
            while True:
                response = client.read_holding_registers(0, 1)
                if response.isError():
                    print(f"Error reading holding registers")
                else:
                    print(f"Holding Register 0: {response.registers[0]}")
                    data = {"value": response.registers[0]}
                    mongo_client.insert_modbus(data)
                time.sleep(5)

        finally:
            client.close()

if __name__ == "__main__":
    client = ModbusClient()