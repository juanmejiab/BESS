import pandas as pd
from subscriptions.create_subscription import create_subscription
from entity.create_entity import create_entities

if __name__ == '__main__':
    data = pd.read_excel("entity/variable_information.xlsx")
    create_entities(data)
    create_subscription(data)
