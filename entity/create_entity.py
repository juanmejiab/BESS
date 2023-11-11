import pandas as pd
import requests
from entities import *


def data_preparation(info: pd.Series):
    var = info.to_dict()
    var_name = var['variable']

    var.pop('slave')
    var.pop('variable')

    return var_name, var


def create_entities(url: str, entities: list, headers: dict):
    try:
        # Realiza la solicitud POST para crear las entidades
        for entity in entities:
            response = requests.post(url, json=entity, headers=headers)

            # Verifica si la solicitud fue exitosa (código de respuesta 201)
            if response.status_code == 201:
                print("Las entidades se crearon con éxito en Orion.")
            else:
                print(
                    f"La solicitud POST falló con código de respuesta {response.status_code}.")
                print(response.text)
    except Exception as e:
        print(f"Se produjo un error al realizar la solicitud POST: {str(e)}")


if __name__ == "__main__":
    # URL de Orion donde se agregarán las entidades
    orion_url = 'http://localhost:1026/v2/entities'

    # Cabeceras HTTP con el tipo de contenido JSON
    headers = {
        'Content-Type': 'application/json'
    }

    data = pd.read_excel(
        "entity/variable_information.xlsx", sheet_name="Sheet1")
    monitor = BessBiblBatteryMonitor()
    inverter1 = BessBiblInverter1Phase1()
    inverter2 = BessBiblInverter2Phase2()
    inverter3 = BessBiblInverter3Phase3()

    for index, row in data.iterrows():
        if row.slave == 1:
            name, var_info = data_preparation(row)
            monitor.set_variables_info(name, var_info)

        elif row.slave == 12:
            name, var_info = data_preparation(row)
            inverter1.set_variables_info(name, var_info)

        elif row.slave == 10:
            name, var_info = data_preparation(row)
            inverter2.set_variables_info(name, var_info)

        elif row.slave == 13:
            name, var_info = data_preparation(row)
            inverter3.set_variables_info(name, var_info)

    entity = [monitor.to_json(),
              inverter1.to_json(),
              inverter2.to_json(),
              inverter3.to_json()]
    create_entities(orion_url, entity, headers)
