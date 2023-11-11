import pandas as pd
import multiprocessing
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, Endian
from entity.entities import *
from entity.create_entity import load_variables


def load_data(entities: list) -> None:
    client = ModbusTcpClient('10.60.48.22', port=502)
    response = client.read_holding_registers(80, 2, slave=12)

    for entity in entities:
        for x in entity.variables_info.values():
            response = client.read_holding_registers(80, 2, slave=12)

            client.close()

            decoder = BinaryPayloadDecoder.fromRegisters(response.registers,
                                                         byteorder=Endian.Big,
                                                         wordorder=Endian.Big)
            valuer = decoder.decode_32bit_int()
            v = decoder.decode_16bit_int()
            print(valuer)


if __name__ == '__main__':
    monitor = BessBiblBatteryMonitor()
    inverter1 = BessBiblInverter1Phase1()
    inverter2 = BessBiblInverter2Phase2()
    inverter3 = BessBiblInverter3Phase3()

    data = pd.read_excel("entity/variable_information.xlsx")

    load_variables(data, [monitor, inverter1, inverter2, inverter3])

    pool = multiprocessing.Pool(4)  # 4 procesos
    pool.map(load_data, [monitor, inverter1, inverter2, inverter3])
    pool.close()
    pool.join()
    """for x in monitor.variables_info.values():
        print(x['startRegister'])
        print(x['bytes'])
        x['value'] = 10
        print("slave: ", monitor.slave)
        print("valor: ", x['value'])"""
