import pandas as pd
import multiprocessing
import requests
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, Endian
from entity.entities import *
from entity.create_entity import load_variables


def read_variable(entities: list) -> None:
    client = ModbusTcpClient('10.60.48.22', port=502)

    for entity in entities:
        for x in entity.variables_info.values():
            time.sleep(0.2)
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
                print(e)
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
                    f"La solicitud PATCH falló con código de respuesta {response.status_code}.")
                print(response.text)

        except Exception as e:
            print(
                f"Se produjo un error al realizar la solicitud PATCH: {str(e)}")


if __name__ == '__main__':
    monitor = BessBiblBatteryMonitor()
    inverter1 = BessBiblInverter1Phase1()
    inverter2 = BessBiblInverter2Phase2()
    inverter3 = BessBiblInverter3Phase3()

    data = pd.read_excel("entity/variable_information.xlsx")
    entities = [monitor, inverter1, inverter2, inverter3]

    load_variables(data, entities)

    while True:
        read_variable(entities)
        update_data(entities)
        print("Lectura finalizada")
        time.sleep(2)
