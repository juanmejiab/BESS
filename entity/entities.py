import copy


class BessBiblBatteryMonitor:
    """
    Object reference for Monitor entity
    """

    def __init__(self) -> None:
        self.id = "BESS_BIBL_BatteryMonitor"
        self.slave = 1
        self.variables_info = {}
        self.variable_entity_creation = {}

    def set_variables_info(self, var_name: str, dict_variable: dict) -> None:
        """
        Set monitor's variable information such as:
        - Variable's name
        - Start Register
        - Bytes
        - Scale
        - Value
        """
        fixed_variables = {
            var_name: {x: y for x, y in dict_variable.items()}
        }
        self.variables_info.update(fixed_variables)

    def to_json(self) -> dict:
        variables_copy = copy.deepcopy(self.variables_info)
        self.variable_entity_creation = variables_copy

        data = {
            "id": self.id,
            "type": "Modbus",
        }

        for x, y in self.variable_entity_creation.items():
            y.pop('startRegister')
            y.pop('bytes')
            y.pop('scale')
        data.update(self.variable_entity_creation)

        return data


class Inverter:
    def __init__(self) -> None:
        self.id = ""
        self.variables_info = {}
        self.variable_entity_creation = {}

    def set_variables_info(self, var_name: str, dict_variable: dict) -> None:
        """
        Set inverter's variable information such as:
        - Variable's name
        - Start Register
        - Bytes
        - Scale
        - Value
        """
        fixed_variables = {
            var_name: {x: y for x, y in dict_variable.items()}
        }
        self.variables_info.update(fixed_variables)

    def to_json(self) -> dict:
        variables_copy = copy.deepcopy(self.variables_info)
        self.variable_entity_creation = variables_copy

        data = {
            "id": self.id,
            "type": "Modbus",
        }

        for x, y in self.variable_entity_creation.items():
            y.pop('startRegister')
            y.pop('bytes')
            y.pop('scale')
        data.update(self.variable_entity_creation)

        return data


class BessBiblInverter1Phase1(Inverter):
    def __init__(self):
        super().__init__()
        self.id = "UPB_BESS_BIBL_Inverter1_Phase1"
        self.slave = 12


class BessBiblInverter2Phase2(Inverter):
    def __init__(self):
        super().__init__()
        self.id = "UPB_BESS_BIBL_Inverter2_Phase2"
        self.slave = 10


class BessBiblInverter3Phase3(Inverter):
    def __init__(self):
        super().__init__()
        self.id = "UPB_BESS_BIBL_Inverter3_Phase3"
        self.slave = 13
