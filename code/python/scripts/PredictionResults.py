# !/usr/bin/env python
# coding: utf-8

# In[87]:

import json
import sys
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd


class DataFrameColumns(Enum):
    """
    Enum for DataFrame column names.

    This Enum provides symbolic names for the DataFrame column names used in the script.
    """
    DATE = 'Data'
    CONSUMPTION = 'Consumption'
    MA_3A5 = 'MA_3a5'
    MA_3A9 = 'MA_3a9'
    DAY_TYPE = 'DayType'
    T_MIN = 'T_min'
    T_MAX = 'T_max'


def moving_avg(df, t_min, t_max):
    """
    Calculate the moving average of the 'Consumption' column over a specified window.

    :param df: DataFrame containing the data.
    :param t_min: Minimum time offset for the moving average window.
    :param t_max: Maximum time offset for the moving average window.
    :return: List of moving average values.
    """
    ma = []
    for idx in range(len(df)):
        if idx >= abs(t_min):
            media = df.iloc[idx + t_min:idx + t_max + 1][DataFrameColumns.CONSUMPTION.value].mean()
        else:
            media = None
        ma.append(media)
    return ma


def day_type(df):
    """
    Identify the type of each day (0 for regular days, 1 for holidays and weekends).

    :param df: DataFrame containing the data.
    :return: List indicating the type of each day.
    """
    lista = [0] * len(df)
    holly_days = [
        "2023-01-01", "2023-04-25", "2023-05-01", "2023-06-10", "2023-08-15",
        "2023-10-05", "2023-11-01", "2023-12-01", "2023-12-08", "2023-12-25"
    ]
    for k, idx in enumerate(df.index):
        data_str = df.loc[idx, DataFrameColumns.DATE.value].strftime("%Y-%m-%d")
        data = datetime.strptime(data_str, "%Y-%m-%d")
        for j in holly_days:
            holly_day = datetime.strptime(j, "%Y-%m-%d")
            if data.month == holly_day.month and data.day == holly_day.day:
                lista[k] = 1
                break
        if data.weekday() in [5, 6]:
            lista[k] = 1
    return lista


def load_data(temperatures_json, consumptions_json):
    """
    Load temperature and consumption data from JSON strings.

    :param temperatures_json: JSON string containing temperature data.
    :param consumptions_json: JSON string containing consumption data.
    :return: Two lists of dictionaries, one for temperatures and one for consumption.
    """
    temperatures_data = json.loads(temperatures_json)
    consumptions_data = json.loads(consumptions_json)
    return temperatures_data, consumptions_data


def preprocess_data(temperatures_data, consumptions_data, size):
    """
    Preprocess the data: convert dates, prepare DataFrame, and fill initial values.

    :param temperatures_data: List of dictionaries containing temperature data.
    :param consumptions_data: List of dictionaries containing consumption data.
    :param size: Size of the DataFrame.
    :return: Preprocessed DataFrame.
    """
    temperature_dates = [datetime.strptime(entry['dateHour'], "%Y-%m-%d") for entry in temperatures_data]
    temperature_min_values = [entry['minValue'] for entry in temperatures_data]
    temperature_max_values = [entry['maxValue'] for entry in temperatures_data]

    consumption_dates = [datetime.strptime(entry['date'], "%Y-%m-%d") for entry in consumptions_data][:-1]
    consumption_values = [entry['consumption'] for entry in consumptions_data][:-1]

    df = pd.DataFrame({
        DataFrameColumns.DATE.value: [None] * size,
        DataFrameColumns.CONSUMPTION.value: [None] * size,
        DataFrameColumns.MA_3A5.value: [None] * size,
        DataFrameColumns.MA_3A9.value: [None] * size,
        DataFrameColumns.DAY_TYPE.value: [None] * size,
        DataFrameColumns.T_MIN.value: [None] * size,
        DataFrameColumns.T_MAX.value: [None] * size
    })

    for i in range(8):
        df.at[i, DataFrameColumns.CONSUMPTION.value] = consumption_values[i]
        df.at[i, DataFrameColumns.DATE.value] = consumption_dates[i]
    for i in range(9, size):
        df.at[i, DataFrameColumns.DATE.value] = temperature_dates[i - 9]
        df.at[i, DataFrameColumns.T_MIN.value] = temperature_min_values[i - 9]
        df.at[i, DataFrameColumns.T_MAX.value] = temperature_max_values[i - 9]

    return df


def update_moving_avg_and_predictions(df, intercept, coefficients, size):
    """
    Update the DataFrame with moving averages and predictions.

    :param df: DataFrame containing the data.
    :param intercept: Intercept value for the linear regression model.
    :param coefficients: Coefficients for the linear regression model.
    :param size: Size of the DataFrame.
    :return: Updated DataFrame with predictions.
    """
    df[DataFrameColumns.DAY_TYPE.value] = day_type(df)
    for i in range(9, size):
        df.at[i, DataFrameColumns.MA_3A9.value] = moving_avg(df, -9, -3)[i]
        df.at[i, DataFrameColumns.CONSUMPTION.value] = intercept + np.dot(coefficients, df.iloc[i, 3:])
    return df


def main():
    """
    Main function to orchestrate the data processing and prediction.
    """
    temperatures_json = sys.argv[1]
    consumptions_json = sys.argv[2]
    coefficients_array_string = sys.argv[3]
    intercept = float(sys.argv[4])

    coefficients_array_string = coefficients_array_string.strip('[]')
    coefficients = np.fromstring(coefficients_array_string, dtype=float, sep=',')

    size = 9 + 5
    temperatures_data, consumptions_data = load_data(temperatures_json, consumptions_json)
    df = preprocess_data(temperatures_data, consumptions_data, size)
    df = update_moving_avg_and_predictions(df, intercept, coefficients, size)

    prediction = df[[DataFrameColumns.DATE.value, DataFrameColumns.CONSUMPTION.value]][9:]
    prediction[DataFrameColumns.DATE.value] = prediction[DataFrameColumns.DATE.value].astype(str).str.strip("T").str[
                                              :10]
    print(prediction.to_json(orient='records', date_format='iso'))


if __name__ == "__main__":
    main()
