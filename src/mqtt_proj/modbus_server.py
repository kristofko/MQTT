import time
import threading
import requests

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from .postgre_client import PostgreClient

class ModbusServer:
    def __init__(self) -> None:
        self.store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [17]*100),  # Discrete Inputs
            co=ModbusSequentialDataBlock(0, [17]*100),  # Coils
            hr=ModbusSequentialDataBlock(0, [0]*100),   # Holding Registers initialized to 0
            ir=ModbusSequentialDataBlock(0, [17]*100)   # Input Registers
        )

        self.context = ModbusServerContext(slaves=self.store, single=True)

        # Setup Modbus server identity
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = "modbus"
        self.identity.ProductCode = "SiskaPC"
        self.identity.ProductName = "Server SiskaModbus"
        self.identity.ModelName = "Server Model"
        self.identity.MajorMinorRevision = "1.0"
        postgre_client = PostgreClient()
        
        # Insert the newly created modbus server into postgre sql
        data = {
            "Product": self.identity.ProductCode,
            "Name":    self.identity.ProductName
        }

        postgre_client.insert_data_to_postgresql(data)
        
            
    def update_holding_registers(self):
        """
        Periodically fetch new data from 
        coincap api and update the holding
        register of modbus with the new data.
        """
        while True:
            url = 'https://api.coincap.io/v2/assets/bitcoin'
            response = requests.get(url)
            data = response.json()
            data = data["data"]["priceUsd"]
            data = int(float(data))
            self.store.setValues(3, 0, [data])  # 3 is the function code for holding registers
            #data = self.store.getValues(3, 0, 1)
            print(f"Updated register 0 with value: {data}")
            
            # Wait for 5 seconds before generating new data
            time.sleep(5)

    def run(self):
        
        # Start a thread to update holding registers periodically
        print("Starting modbus server")
        update_thread = threading.Thread(target=self.update_holding_registers)
        update_thread.daemon = True
        update_thread.start()

        # Start the Modbus TCP server
        StartTcpServer(context=self.context, 
                       identity=self.identity, 
                       address=("localhost", 5020))

        
if __name__ == "__main__":
    """
    Start the appli cation with:
    python3 modbus_server.py
    """
    client = ModbusServer()