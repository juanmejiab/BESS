class MonitorSubscription:
    def __init__(self):
        self.condition_attributes = []
        self.notification_attributes = []

    def load_attributes(self, attribute: list) -> None:
        condition_attributes = attribute.copy()

        notification_attributes = ["id"] + condition_attributes

        self.condition_attributes = condition_attributes
        self.notification_attributes = notification_attributes

    def create_subscription(self) -> dict:
        data = {
            "description": "BESS_BIBL_Monitor Subscription",
            "subject": {
                "entities": [
                    {
                        "idPattern": "BESS_BIBL_BatteryMonitor",
                        "type": "Modbus"
                    }
                ],
                "condition": {
                    "attrs": self.condition_attributes
                }
            },
            "notification": {
                "attrs": self.notification_attributes,
                "http": {
                    "url": "http://quantumleap:8668/v2/notify"
                }
            }
        }
        return data


class InverterSubscription:
    def __init__(self):
        self.description = ""
        self.id = ""
        self.condition_attributes = []
        self.notification_attributes = []

    def load_attributes(self, attribute: list) -> None:
        condition_attributes = attribute.copy()

        notification_attributes = ["id"] + condition_attributes

        self.condition_attributes = condition_attributes
        self.notification_attributes = notification_attributes

    def create_subscription(self) -> dict:
        data = {
            "description": self.description,
            "subject": {
                "entities": [
                    {
                        "idPattern": self.id,
                        "type": "Modbus"
                    }
                ],
                "condition": {
                    "attrs": self.condition_attributes
                }
            },
            "notification": {
                "attrs": self.notification_attributes,
                "http": {
                    "url": "http://quantumleap:8668/v2/notify"
                }
            }
        }
        return data


class Inverter1Subscription(InverterSubscription):
    def __init__(self):
        self.description = "UPB_BESS_BIBL_Inverter1_Phase1 Subscription"
        self.id = "UPB_BESS_BIBL_Inverter1_Phase1"


class Inverter2Subscription(InverterSubscription):
    def __init__(self):
        self.description = "UPB_BESS_BIBL_Inverter2_Phase2 Subscription"
        self.id = "UPB_BESS_BIBL_Inverter2_Phase2"


class Inverter3Subscription(InverterSubscription):
    def __init__(self):
        self.description = "UPB_BESS_BIBL_Inverter3_Phase3 Subscription"
        self.id = "UPB_BESS_BIBL_Inverter3_Phase3"
