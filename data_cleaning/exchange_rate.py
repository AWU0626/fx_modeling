import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame


CURRENCY_NAME = {
    'EXCAUS': 'CAD',
    'EXCHUS': 'CNY',
    'EXHKUS': 'HKD',
    'EXJPUS': 'JPY',
    'EXKOUS': 'KRW',
    'EXMXUS': 'MXN',
    'EXNOUS': 'NOK',
    'EXSDUS': 'SEK',
    'EXSIUS': 'SGD',
    'EXSZUS': 'CHF',
    'EXUSAL': 'AUD',
    'EXUSEU': 'EUR',
    'EXUSNZ': 'NZD',
    'EXUSUK': 'GBP',
}


def load_initial_data():
    # read data
    data = pd.read_csv('../initial_data/Exchange_Rates_txt/Exchange_Rates_Monthly.txt', sep='\t')

    # Data Cleaning
    ## Convert to Dataframe
    exchange_rate = DataFrame(data)

    ## drop null
    exchange_rate.dropna(inplace=True)

    ## convert all currencies to USD as base currency
    ## for Australian (), Euro, New Zealand, Pound
    inverse_list = ['EXUSAL', 'EXUSEU', 'EXUSNZ', 'EXUSUK']
    for element in inverse_list:
        exchange_rate[element] = 1/exchange_rate[element]

    # convert to foreign currency name
    exchange_rate.rename(CURRENCY_NAME, axis='columns', inplace=True)

    # convert date object to datetime
    exchange_rate['DATE'] = pd.to_datetime(exchange_rate['DATE'])

    return exchange_rate


def save_data_to_csv(data, index, columns, filename):
    data_columns = data.columns.tolist()
    missing = [col for col in columns if col not in data_columns]

    if missing:
        raise ValueError(
            f"The following columns are missing "
            f"in the DataFrame: {', '.join(missing)}"
        )

    # Set the specified index column
    data = data.set_index(index)

    # Select the specified columns
    selected_data = data[columns]

    # create the folder if doesn't exist
    target_path = os.path.join(os.path.dirname(os.path.abspath('')), 'data')
    os.makedirs(target_path, exist_ok=True)

    # Full path for the file
    filepath = os.path.join(target_path, filename)

    # Save the selected data to CSV
    selected_data.to_csv(filepath)
    print(f"Data saved to {filepath}")


exchange_rate = load_initial_data()

csv_list = exchange_rate.columns.tolist()[1:]

for file in csv_list:
    save_data_to_csv(exchange_rate, 'DATE', [file], f'{file}USD.csv')


print(exchange_rate)