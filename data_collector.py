import pandas as pd
import multiprocessing
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, Endian
from entity.entities import *
from entity.create_entity import load_variables


def load_data(entities: list) -> None:
    client = ModbusTcpClient('10.60.48.22', port=502)
    # response = client.read_holding_registers(80, 2, slave=12)

    for entity in entities:
        for x in entity.variables_info.values():
            time.sleep(0.11)
            register = x['startRegister']
            bytes = x['bytes']
            slave = entity.slave

            try:
                response = client.read_holding_registers(
                    register, bytes, slave=slave)

                client.close()

                decoder = BinaryPayloadDecoder.fromRegisters(response.registers,
                                                             byteorder=Endian.BIG,
                                                             wordorder=Endian.BIG)
                if x['bytes'] == 1:
                    value = decoder.decode_16bit_int()
                    x["value"] = value / x["scale"]
                    print(x["value"])
                else:
                    value = decoder.decode_32bit_int()
                    x["value"] = value / x["scale"]
                    print(x["value"])

            except Exception as e:
                # Handle the exception appropriately
                # Log the error, retry the operation, or take other necessary actions
                print(f"Error occurred: {e}")
                # Retry the operation
                continue


if __name__ == '__main__':
    monitor = BessBiblBatteryMonitor()
    inverter1 = BessBiblInverter1Phase1()
    inverter2 = BessBiblInverter2Phase2()
    inverter3 = BessBiblInverter3Phase3()

    data = pd.read_excel("entity/variable_information.xlsx")

    load_variables(data, [monitor, inverter1, inverter2, inverter3])

    while True:
        load_data([monitor, inverter1, inverter2, inverter3])
        print("Lectura finalizada")
        time.sleep(10)
