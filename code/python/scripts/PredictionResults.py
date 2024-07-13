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
    DATE = 'date'
    CONSUMPTION = 'consumption'
    MA_3A5 = 'MA_3a5'
    MA_3A9 = 'MA_3a9'
    DAY_TYPE = 'DayType'
    T_MIN = 'minTemps'
    T_MAX = 'maxTemps'


def calculate_moving_avg(d_frame, window):
    """
    Calculate the moving average of the 'consumption' column over a specified window.

    :param d_frame: DataFrame containing the data.
    :param window: Window size for calculating the moving average.

    :return: Series of moving average values.
    """
    return d_frame[DataFrameColumns.CONSUMPTION.value].rolling(window=window, min_periods=1).mean()


def load_file(file_path):
    """
    Loads the content from a file.

    :param file_path: The path to the file.

    :return: A list representing the content of the file as strings.
    """
    content = []
    with open(file_path, 'r') as file:
        for line in file:
            treated_line = line.strip()
            if treated_line:  # Make sure it's not an empty line
                content.append(treated_line)
    return content


def determine_day_type(d_frame, path):
    """
    Determine the type of day (weekend or holiday).

    :param d_frame: DataFrame containing the data.
    :param path: Path for the holiday file.

    :return: A list indicating the type of day (1 for weekend/holiday, 0 for weekday).
    """
    lista = [0] * len(d_frame)
    holly_days = load_file(path)
    for k, idx in enumerate(d_frame.index):
        data_str = d_frame.loc[idx, DataFrameColumns.DATE.value].strftime("%Y-%m-%d")
        data = datetime.strptime(data_str, "%Y-%m-%d")
        for j in holly_days:
            holly_day = datetime.strptime(j, "%Y-%m-%d")
            if data.month == holly_day.month and data.day == holly_day.day:
                lista[k] = 1
                break
        if data.weekday() in [5, 6]:
            lista[k] = 1
    return lista


def load_data_from_json(temperature_json, consumption_json):
    """
    Load temperature and consumption data from JSON strings.

    :param temperature_json: JSON string containing temperature data.
    :param consumption_json: JSON string containing consumption data.

    :return: Two DataFrames, one for temperatures and one for consumption.
    """
    temperatures_data = json.loads(temperature_json)
    consumptions_data = json.loads(consumption_json)
    temperatures = pd.DataFrame(temperatures_data)
    consumptions = pd.DataFrame(consumptions_data)
    return temperatures, consumptions


def preprocess_data(temperatures, consumptions, size):
    """
    Preprocess the data: convert dates, prepare DataFrame, and fill initial values.

    :param temperatures: DataFrame containing temperature data.
    :param consumptions: DataFrame containing consumption data.
    :param size: Size of the DataFrame.
    :return: Preprocessed DataFrame.
    """
    temperatures[DataFrameColumns.DATE.value] = pd.to_datetime(temperatures[DataFrameColumns.DATE.value])
    temperature_dates = temperatures[DataFrameColumns.DATE.value].tolist()
    temperature_min_values = temperatures[DataFrameColumns.T_MIN.value].tolist()
    temperature_max_values = temperatures[DataFrameColumns.T_MAX.value].tolist()

    consumptions[DataFrameColumns.DATE.value] = pd.to_datetime(consumptions[DataFrameColumns.DATE.value])
    consumption_dates = consumptions[DataFrameColumns.DATE.value].tolist()
    consumption_values = consumptions[DataFrameColumns.CONSUMPTION.value].tolist()

    df = pd.DataFrame({
        DataFrameColumns.DATE.value: [None] * size,
        DataFrameColumns.CONSUMPTION.value: [None] * size,
        DataFrameColumns.MA_3A5.value: [None] * size,
        DataFrameColumns.MA_3A9.value: [None] * size,
        DataFrameColumns.DAY_TYPE.value: [None] * size,
        DataFrameColumns.T_MIN.value: [None] * size,
        DataFrameColumns.T_MAX.value: [None] * size
    })

    for i in range(9):
        df.at[i, DataFrameColumns.CONSUMPTION.value] = consumption_values[i]
        df.at[i, DataFrameColumns.DATE.value] = consumption_dates[i]
    for i in range(9, size):
        df.at[i, DataFrameColumns.DATE.value] = temperature_dates[i - 9]
        df.at[i, DataFrameColumns.T_MIN.value] = temperature_min_values[i - 9]
        df.at[i, DataFrameColumns.T_MAX.value] = temperature_max_values[i - 9]
    return df


def update_moving_avg_and_predictions(df, intercept, coefficients, size, path):
    """
    Update the DataFrame with moving averages and predictions.

    :param path: Path to the file containing the list of holidays.
    :param df: DataFrame containing the data.
    :param intercept: Intercept value for the linear regression model.
    :param coefficients: Coefficients for the linear regression model.
    :param size: Size of the DataFrame.
    :return: Updated DataFrame with predictions.
    """
    df[DataFrameColumns.DAY_TYPE.value] = determine_day_type(df, path)
    for i in range(9, size):
        df.at[i, DataFrameColumns.MA_3A5.value] = calculate_moving_avg(df.iloc[:i], 5).iloc[-1]
        df.at[i, DataFrameColumns.MA_3A9.value] = calculate_moving_avg(df.iloc[:i], 9).iloc[-1]
        df.at[i, DataFrameColumns.CONSUMPTION.value] = intercept + np.dot(coefficients, df.iloc[i, 3:])
    return df


def main():
    """
    Main function to orchestrate the data processing and prediction.
    """
    temperature_json = sys.argv[1]
    consumption_json = sys.argv[2]
    coefficients_array_string = sys.argv[3]
    intercept = float(sys.argv[4])
    holiday_file_path = 'holidays.txt'

    coefficients_array_string = coefficients_array_string.strip('[]')
    coefficients = np.fromstring(coefficients_array_string, dtype=float, sep=',')

    size = 9 + 5
    temperatures_data, consumptions_data = load_data_from_json(temperature_json, consumption_json)
    df = preprocess_data(temperatures_data, consumptions_data, size)
    df = update_moving_avg_and_predictions(df, intercept, coefficients, size, holiday_file_path)

    prediction = df[[DataFrameColumns.DATE.value, DataFrameColumns.CONSUMPTION.value]][9:]
    prediction[DataFrameColumns.DATE.value] = prediction[DataFrameColumns.DATE.value].astype(str).str.strip("T").str[
                                              :10]
    print(prediction.to_json(orient='records', date_format='iso'))


if __name__ == "__main__":
    main()

# Today is the 20th, and I can predict the consumption for the 20th to 24th

# Input:
# Future temperature
# "{\"date\": [\"2024-07-20\", \"2024-07-21\", \"2024-07-22\", \"2024-07-23\", \"2024-07-24\"],
# \"minTemps\": [18, 18, 16, 16, 16], \"maxTemps\": [24, 23, 28, 28, 23]}"

# Past consumptions
# "{\"date\": [\"2024-07-11\", \"2024-07-12\", \"2024-07-13\", \"2024-07-14\", \"2024-07-15\", \"2024-07-16\",
# \"2024-07-17\", \"2024-07-18\", \"2024-07-19\"], \"consumption\":[-1,-1,-1,-1,-1,-1,-1,-1,-1]}"

# From the model generated by the training
# {"R^2 Score": NaN, "Coefficients": [0.0, 0.0, 0.0, 0.0], "Intercept": -1.0}
# Coefficients: "[0.0, 0.0, 0.0, 0.0]"
# Intercept = -1.0

# Output: Predicted consumption for the 20th to 24th
# [{"date":"2024-07-20", "consumption":-1.0}, {"date":"2024-07-21", "consumption":-1.0}, {"date":"2024-07-22",
# "consumption":-1.0}, {"date":"2024-07-23", "consumption":-1.0}, {"date":"2024-07-24", "consumption":-1.0}]

# working input
# "{\"date\": [\"2024-07-03\", \"2024-07-04\", \"2024-07-05\", \"2024-07-06\", \"2024-07-07\", \"2024-07-08\",
# \"2024-07-09\", \"2024-07-10\", \"2024-07-11\", \"2024-07-12\", \"2024-07-13\", \"2024-07-14\", \"2024-07-15\",
# \"2024-07-16\"], \"minTemps\": [16, 15, 17, 14, 13, 16, 15, 17, 14, 13, 16, 15, 17, 14], \"maxTemps\": [24, 23, 22,
# 24, 25, 24, 23, 22, 24, 25, 24, 23, 22, 24]}"

# "{\"date\": [\"2024-07-03\", \"2024-07-04\", \"2024-07-05\", \"2024-07-06\", \"2024-07-07\", \"2024-07-08\",
# \"2024-07-09\", \"2024-07-10\", \"2024-07-11\"], \"consumption\":[-2,-3,-4,-2,-2,-3,-2,-3,-4]}"

# "[2.398851648470614, 1.4125466531591617, -0.042812821903454396,-0.22633592977142003]"

# 9.127584881596157


# working output

# [{"date":"2024-07-03", "consumption":-3.6529593847}, {"date":"2024-07-04", "consumption":-3.8243888935},
# {"date":"2024-07-05", "consumption":-3.9034104583}, {"date":"2024-07-06", "consumption":-2.7893523121},
# {"date":"2024-07-07", "consumption":-3.1832686528}]
