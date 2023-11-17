import pandas as pd
import requests
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, Endian
from entity.entities import *
from entity.create_entity import load_variables


def read_variable(entities: list) -> None:
    # Modbus connection
    client = ModbusTcpClient('10.60.48.22', port=502)

    for entity in entities:
        for x in entity.variables_info.values():
            time.sleep(0.1)

            # Set parameters
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
                else:
                    value = decoder.decode_32bit_int()
                    x["value"] = value / x["scale"]

            except Exception as e:
                continue


def update_data(entities: list) -> None:
    for entity in entities:
        info = entity.to_json()
        info.pop("id")
        info.pop("type")
        url = f"http://localhost:1026/v2/entities/{entity.id}/attrs"

        header = {
            'Content-Type': 'application/json'
        }

        try:
            # Realiza la solicitud PATCH
            response = requests.patch(url, json=info, headers=header)

            # Verifica si la solicitud fue exitosa (código de respuesta 204)
            if response.status_code == 204:
                pass
            else:
                print(
                    f"PATCH request failed with response code {response.status_code}.")
                print(response.text)

        except Exception as e:
            print(
                f"An error occurred while making the PATCH request: {str(e)}")


if __name__ == '__main__':
    monitor = BessBiblBatteryMonitor()
    inverter1 = BessBiblInverter1Phase1()
    inverter2 = BessBiblInverter2Phase2()
    inverter3 = BessBiblInverter3Phase3()

    # Read variable info
    data = pd.read_excel("entity/variable_information.xlsx")
    entities = [monitor, inverter1, inverter2, inverter3]

    load_variables(data, entities)

    while True:
        # Read vairables from BESS
        read_variable(entities)

        # PATCH request to update data
        update_data(entities)
