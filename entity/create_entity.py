import pandas as pd
import requests
from entity.entities import *


def data_preparation(info: pd.Series):
    var = info.to_dict()
    var_name = var['variable']

    var.pop('slave')
    var.pop('variable')

    return var_name, var


def load_variables(data: pd.DataFrame, entities: list) -> None:
    for index, row in data.iterrows():
        for entity in entities:
            if row.slave == 1 and isinstance(entity, BessBiblBatteryMonitor):
                name, var_info = data_preparation(row)
                entity.set_variables_info(name, var_info)

            elif row.slave == 12 and isinstance(entity, BessBiblInverter1Phase1):
                name, var_info = data_preparation(row)
                entity.set_variables_info(name, var_info)

            elif row.slave == 10 and isinstance(entity, BessBiblInverter2Phase2):
                name, var_info = data_preparation(row)
                entity.set_variables_info(name, var_info)

            elif row.slave == 13 and isinstance(entity, BessBiblInverter3Phase3):
                name, var_info = data_preparation(row)
                entity.set_variables_info(name, var_info)


def create_entities(data: pd.DataFrame):
    url = 'http://localhost:1026/v2/entities'

    # Cabeceras HTTP con el tipo de contenido JSON
    headers = {
        'Content-Type': 'application/json'
    }

    monitor = BessBiblBatteryMonitor()
    inverter1 = BessBiblInverter1Phase1()
    inverter2 = BessBiblInverter2Phase2()
    inverter3 = BessBiblInverter3Phase3()

    load_variables(data, [monitor, inverter1, inverter2, inverter3])

    entities = [monitor.to_json(),
                inverter1.to_json(),
                inverter2.to_json(),
                inverter3.to_json()]
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
