import json
import sys
from datetime import datetime
from enum import Enum

import pandas as pd
from sklearn.linear_model import LinearRegression


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
    T_MIN = 'minValue'
    T_MAX = 'maxValue'


def calculate_moving_avg(d_frame, t_min, t_max):
    """
    Calculate the moving average of the 'consumption' column over a specified range.

    :param d_frame: DataFrame containing the data.
    :param t_min: Minimum range for calculating the moving average.
    :param t_max: Maximum range for calculating the moving average.

    :return: List of moving average values.
    """
    ma = []
    for idx in range(len(d_frame)):
        if idx >= abs(t_min):
            media = d_frame.iloc[idx + t_min:idx + t_max + 1][DataFrameColumns.CONSUMPTION.value].mean()
        else:
            media = None
        ma.append(media)
    return ma


def determine_day_type(d_frame):
    """
    Determine the type of day (weekend or holiday).

    :param d_frame: DataFrame containing the data.

    :return: A list indicating the type of day (1 for weekend/holiday, 0 for weekday).
    """
    lista = [0] * len(d_frame)
    holly_days = [
        "2023-01-01", "2023-04-25", "2023-05-01", "2023-06-10", "2023-08-15",
        "2023-10-05", "2023-11-01", "2023-12-01", "2023-12-08", "2023-12-25"
    ]
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


def preprocess_data(temperatures, consumptions):
    """
    Preprocess the data: calculate moving averages, determine day types, and merge data.

    :param temperatures: DataFrame containing temperature data.
    :param consumptions: DataFrame containing consumption data.

    :return: Preprocessed DataFrame.
    """
    df_temp = temperatures[["dateHour", DataFrameColumns.T_MIN.value, DataFrameColumns.T_MAX.value]]
    df = consumptions[[DataFrameColumns.DATE.value, DataFrameColumns.CONSUMPTION.value]]

    df[DataFrameColumns.MA_3A5.value] = calculate_moving_avg(df, -5, -2)
    df[DataFrameColumns.MA_3A9.value] = calculate_moving_avg(df, -9, -2)
    df[DataFrameColumns.DAY_TYPE.value] = determine_day_type(df)

    df[DataFrameColumns.T_MIN.value] = df_temp[DataFrameColumns.T_MIN.value]
    df[DataFrameColumns.T_MAX.value] = df_temp[DataFrameColumns.T_MAX.value]
    df = df.dropna()
    return df


def perform_regression(df):
    """
    Perform linear regression on the preprocessed data.

    :param df: Preprocessed DataFrame.

    :return: Dictionary containing the R^2 score, coefficients, and intercept of the regression model.
    """
    x = df.iloc[:, 3:]
    y = df[DataFrameColumns.CONSUMPTION.value]

    reg = LinearRegression().fit(x, y)
    score = reg.score(x, y)
    coefficients = reg.coef_
    intercept = reg.intercept_

    result = {
        "R^2 Score": score,
        "Coefficients": list(coefficients),
        "Intercept": intercept
    }
    return result


def main():
    """
    Main function to orchestrate the data processing and regression analysis.
    """
    temperature_json = sys.argv[1]
    consumption_json = sys.argv[2]

    temperatures, consumptions = load_data_from_json(temperature_json, consumption_json)
    df = preprocess_data(temperatures, consumptions)
    result = perform_regression(df)

    result_json = json.dumps(result)
    print(f"\n{result_json}")


if __name__ == "__main__":
    main()
