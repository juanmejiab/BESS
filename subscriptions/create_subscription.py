import requests
import pandas as pd
from subscriptions.subscription import *


def create_subscription(data: pd.DataFrame):
    # Initialize entities' structure
    monitor_subscription = MonitorSubscription()
    inverter1_subscription = Inverter1Subscription()
    inverter2_subscription = Inverter2Subscription()
    inverter3_subscription = Inverter3Subscription()

    monitor_variable = []
    inverter_variable = []

    for index, row in data.iterrows():
        if row.slave == 1:
            monitor_variable.append(row.variable)
        elif row.slave == 12:
            inverter_variable.append(row.variable)

    monitor_subscription.load_attributes(monitor_variable)
    inverter1_subscription.load_attributes(inverter_variable)
    inverter2_subscription.load_attributes(inverter_variable)
    inverter3_subscription.load_attributes(inverter_variable)

    subscription_data = [monitor_subscription.create_subscription(),
                         inverter1_subscription.create_subscription(),
                         inverter2_subscription.create_subscription(),
                         inverter3_subscription.create_subscription()]

    url = "http://localhost:1026/v2/subscriptions"
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # POST request to create subscription
        for sub in subscription_data:
            response = requests.post(url, json=sub, headers=headers)

            # Verify if the request was successful
            if response.status_code == 201:
                print("The subscription was created successfully")
            else:
                print(
                    f"POST request failed with response code {response.status_code}.")
                print(response.text)

    except Exception as e:
        print(
            f"An error occurred while making the POST request to create the subscription: {str(e)}")
