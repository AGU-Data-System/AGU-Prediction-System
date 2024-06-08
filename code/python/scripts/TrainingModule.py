import json
import sys
from datetime import datetime

import pandas as pd
from sklearn.linear_model import LinearRegression


def media_movel(df, tmin, tmax):
    """
    Calculate the moving average of the 'consumption' column over a specified range.

    :param df: DataFrame containing the data.
    :param tmin: Minimum range for calculating the moving average.
    :param tmax: Maximum range for calculating the moving average.

    :return: List of moving average values.
    """
    ma = []  # Initialize a list to store moving averages
    for i in range(len(df)):  # Iterate over the dataframe
        if i >= abs(tmin):  # Ensure the index is within range for calculation
            # Calculate the mean of the 'consumption' column over the range [i+tmin, i+tmax]
            media = df.iloc[i + tmin: i + tmax + 1]['consumption'].mean()
        else:
            media = None  # If index is out of range, append None
        ma.append(media)  # Append the result to the list

    return ma  # Return the list of moving averages


def day_type(df):
    """
    Determine the type of day (weekend or holiday).

    :param df: DataFrame containing the data.

    :return: A list indicating the type of day (1 for weekend/holiday, 0 for weekday).
    """
    lista = [0] * len(df)  # Initialize a list to store day types
    # List of holidays
    holly_day = [
        "2023-01-01", "2023-04-25", "2023-05-01", "2023-06-10", "2023-08-15",
        "2023-10-05", "2023-11-01", "2023-12-01", "2023-12-08", "2023-12-25"
    ]
    df['date'] = pd.to_datetime(df['date'])  # Convert date column to datetime
    for i in range(len(df)):  # Iterate over the dataframe
        data_str = df.loc[i, 'date'].strftime("%Y-%m-%d")  # Convert date to string
        data = datetime.strptime(data_str, "%Y-%m-%d")  # Parse string to a datetime object
        for j in holly_day:  # Iterate over holidays
            holly_day = datetime.strptime(j, "%Y-%m-%d")  # Parse holiday to a datetime object
            if data.month == holly_day.month and data.day == holly_day.day:  # Check if date is a holiday
                lista[i] = 1  # Mark as holiday
                break

        if data.weekday() == 5 or data.weekday() == 6:  # Check if date is a weekend
            lista[i] = 1  # Mark as weekend

    return lista  # Return the list of day types


# Read temperature and consumption data from command line arguments
temperature_json = sys.argv[1]
consumption_json = sys.argv[2]

# Convert temperature and consumption data from JSON strings to DataFrames
temperatures_data = json.loads(temperature_json)
consumptions_data = json.loads(consumption_json)
temperatures = pd.DataFrame(temperatures_data)
consumptions = pd.DataFrame(consumptions_data)

# Select relevant columns from the DataFrames
df_temp = temperatures[["dateHour", "minValue", "maxValue"]]
df = consumptions[["date", "consumption"]]

# Calculate moving averages and add them as new columns to the dataframe
df['MA_3a5'] = media_movel(df, -5, -2)
df['MA_3a9'] = media_movel(df, -9, -2)

# Determine the type of day and add it as a new column
df['DayType'] = day_type(df)

# Add temperature data to the dataframe
df['minValue'] = df_temp['minValue']
df['maxValue'] = df_temp['maxValue']

# Drop rows with missing values
df = df.dropna()

# Select feature columns (X) and target column (Y) for regression
X = df.iloc[:, 3:]  # All columns from the 4th to the last
Y = df.iloc[:, 1]  # The 'consumption' column

# Perform linear regression
reg = LinearRegression().fit(X, Y)

# Get the R^2 score, coefficients, and intercept of the regression model
score = reg.score(X, Y)
coefficients = reg.coef_
intercept = reg.intercept_

# Store results in a dictionary and convert to JSON
result = {
    "R^2 Score": score,
    "Coefficients": list(coefficients),
    "Intercept": intercept
}

# Print the results as a JSON string
result_json = json.dumps(result)
print(f"\n{result_json}")
