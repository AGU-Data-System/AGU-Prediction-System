import json
import sys
from datetime import datetime

import pandas as pd
from sklearn.linear_model import LinearRegression


def MediaMovel(df, tmin, tmax):
    MA = []
    for i in range(len(df)):
        if i >= abs(tmin):
            media = df.iloc[i + tmin: i + tmax + 1]['consumption'].mean()
        else:
            media = None
        MA.append(media)

    return MA


def DayType(df):
    lista = [0] * len(df)
    feriados = [
        "2023-01-01", "2023-04-25", "2023-05-01", "2023-06-10", "2023-08-15",
        "2023-10-05", "2023-11-01", "2023-12-01", "2023-12-08", "2023-12-25"
    ]
    df['date'] = pd.to_datetime(df['date'])
    for i in range(len(df)):
        data_str = df.loc[i, 'date'].strftime("%Y-%m-%d")
        data = datetime.strptime(data_str, "%Y-%m-%d")
        for j in feriados:
            feriado = datetime.strptime(j, "%Y-%m-%d")
            if data.month == feriado.month and data.day == feriado.day:
                lista[i] = 1
                break

        if data.weekday() == 5 or data.weekday() == 6:
            lista[i] = 1

    return lista


temperature_json = sys.argv[1]
consumption_json = sys.argv[2]

# Convert temperature and consumption data from strings to DataFrames
temperatures_data = json.loads(temperature_json)
consumptions_data = json.loads(consumption_json)
temperatures = pd.DataFrame(temperatures_data)
consumptions = pd.DataFrame(consumptions_data)

df_temp = temperatures[["dateHour", "minValue", "maxValue"]]
df = consumptions[["date", "consumption"]]

df['MA_3a5'] = MediaMovel(df, -5, -2)
df['MA_3a9'] = MediaMovel(df, -9, -2)
df['DayType'] = DayType(df)
df['minValue'] = df_temp['minValue']
df['maxValue'] = df_temp['maxValue']

df = df.dropna()

X = df.iloc[:, 3:]
Y = df.iloc[:, 1]
reg = LinearRegression().fit(X, Y)
score = reg.score(X, Y)
coefficients = reg.coef_
intercept = reg.intercept_

result = {
    "R^2 Score": score,
    "Coefficients": list(coefficients),
    "Intercept": intercept
}

result_json = json.dumps(result)
print(f"\n{result_json}")
