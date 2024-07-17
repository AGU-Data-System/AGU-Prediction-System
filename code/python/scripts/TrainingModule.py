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
    content = ["2024-01-01",
               "2024-04-25",
               "2024-05-01",
               "2024-06-10",
               "2024-08-15",
               "2024-10-05",
               "2024-11-01",
               "2024-12-01",
               "2024-12-08",
               "2024-12-25"
               ]
#     with open(file_path, 'r') as file:
#         for line in file:
#             treated_line = line.strip()
#             if treated_line:  # Make sure it's not an empty line
#                 content.append(treated_line)
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


def preprocess_data(temperatures, consumptions, path):
    """
    Preprocess the data: calculate moving averages, determine day types, and merge data.

    :param temperatures: DataFrame containing temperature data.
    :param consumptions: DataFrame containing consumption data.
    :param path: Path for the holiday file.

    :return: Preprocessed DataFrame.
    """
    temperatures[DataFrameColumns.DATE.value] = pd.to_datetime(temperatures[DataFrameColumns.DATE.value])
    consumptions[DataFrameColumns.DATE.value] = pd.to_datetime(consumptions[DataFrameColumns.DATE.value])

    df_temp = temperatures[[DataFrameColumns.DATE.value, DataFrameColumns.T_MIN.value, DataFrameColumns.T_MAX.value]]
    df = consumptions[[DataFrameColumns.DATE.value, DataFrameColumns.CONSUMPTION.value]]

    df[DataFrameColumns.MA_3A5.value] = calculate_moving_avg(df, 5)
    df[DataFrameColumns.MA_3A9.value] = calculate_moving_avg(df, 9)
    df[DataFrameColumns.DAY_TYPE.value] = determine_day_type(df, path)

    df = df.merge(df_temp, on=DataFrameColumns.DATE.value, how='left')

    print("DataFrame before dropping NaNs:")
    print(df)

    df = df.dropna()

    print("DataFrame after dropping NaNs:")
    print(df)

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
        "coefficients": list(coefficients),
        "intercept": intercept
    }
    return result


def main():
    """
    Main function to orchestrate the data processing and regression analysis.
    """
    temperature_json = sys.argv[1]
    consumption_json = sys.argv[2]
    holidays_file_path = './holidays.txt'

    temperatures, consumptions = load_data_from_json(temperature_json, consumption_json)
    df = preprocess_data(temperatures, consumptions, holidays_file_path)
    result = perform_regression(df)

    result_json = json.dumps(result)
    print(f"\n{result_json}")


if __name__ == "__main__":
    main()

# Today is the 20th, and I can predict the consumption for the 20th and generate the model to predict from 20 to 24

# Input:
# Future temperature
# "{\"date\": [\"2024-07-20\", \"2024-07-21\", \"2024-07-22\", \"2024-07-23\", \"2024-07-24\",
# \"minTemps\": [18, 18, 16, 16, 16], \"maxTemps\": [24, 23, 28, 28, 23]}"

# Past consumptions
# "{\"date\": [\"2024-07-11\", \"2024-07-12\", \"2024-07-13\", \"2024-07-14\", \"2024-07-15\",
# \"2024-07-16\", \"2024-07-17\", \"2024-07-18\", \"2024-07-19\"], \"consumption\":[-1,-1,-1,-1,-1,-1,-1,-1,-1]}"

# Output:
# Generated model
# {"R^2 Score": NaN, "coefficients": [0.0, 0.0, 0.0, 0.0], "intercept": -1.0}


# working input
#
# "{\"date\": [\"2024-07-03\", \"2024-07-04\", \"2024-07-05\", \"2024-07-06\", \"2024-07-07\", \"2024-07-08\",
# \"2024-07-09\", \"2024-07-10\", \"2024-07-11\"], \"minTemps\": [16, 15, 17, 14, 13, 16, 15, 17, 14], \"maxTemps\":
# [24, 23, 22, 24, 25, 24, 23, 22, 24]}"
#
# "{\"date\": [\"2024-07-03\", \"2024-07-04\", \"2024-07-05\", \"2024-07-06\", \"2024-07-07\", \"2024-07-08\",
# \"2024-07-09\", \"2024-07-10\", \"2024-07-11\"], \"consumption\":[2,3,4,2,2,3,2,3,4]}"

# working output
#
# {"R^2 Score": 0.7601530334519065, "coefficients": [2.398851648470614, 1.4125466531591617, -0.042812821903454396,
# -0.22633592977142003], "intercept": 9.127584881596157}
