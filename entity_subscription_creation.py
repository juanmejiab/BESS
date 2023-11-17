import pandas as pd
from subscriptions.create_subscription import create_subscription
from entity.create_entity import create_entities

if __name__ == '__main__':
    # Read data features
    data = pd.read_excel("entity/variable_information.xlsx")

    # Create entities
    create_entities(data)

    # Create subscription
    create_subscription(data)
