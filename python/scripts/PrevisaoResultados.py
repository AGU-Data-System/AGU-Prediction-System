# !/usr/bin/env python
# coding: utf-8

# In[87]:


import json
import sys
# import tensorflow as tf
from datetime import datetime

import numpy as np
import pandas as pd


def MediaMovel(df, tmin, tmax):
    MA = []
    for i in range(len(df)):
        if i >= abs(tmin):
            media = df.iloc[i + tmin:i + tmax + 1]['Consumo'].mean()
        else:
            media = None
        MA.append(media)

    return MA


def DayType(df):
    lista = [0] * len(df)
    feriados = ["2023-01-01", "2023-04-25", "2023-05-01", "2023-06-10", "2023-08-15", "2023-10-05", "2023-11-01",
                "2023-12-01", "2023-12-08", "2023-12-25"]
    k = 0
    for i in range(df.index[0], df.index[-1]):
        data_str = df.loc[i, 'Data'].strftime("%Y-%m-%d")
        data = datetime.strptime(data_str, "%Y-%m-%d")
        for j in feriados:
            feriado = datetime.strptime(j, "%Y-%m-%d")
            if data.month == feriado.month and data.day == feriado.day:
                lista[k] = 1;
                break

            if data.weekday() == 5 or data.weekday() == 6:
                lista[k] = 1
            k += 1

        return lista


size = 9 + 5

temperatures_json = sys.argv[1]
consumptions_json = sys.argv[2]
coefs_array_string = sys.argv[3]
intercept = sys.argv[4]

intercept = float(intercept)

coefs_array_string = coefs_array_string.strip('[]')

coefs = np.fromstring(coefs_array_string, dtype=float, sep=',')

temperatures_data = json.loads(temperatures_json)
consumptions_data = json.loads(consumptions_json)

temperature_dates = [datetime.strptime(entry['dateHour'], "%Y-%m-%d") for entry in temperatures_data]
temperature_min_values = [entry['minValue'] for entry in temperatures_data]
temperature_max_values = [entry['maxValue'] for entry in temperatures_data]

consumption_dates = [datetime.strptime(entry['date'], "%Y-%m-%d") for entry in consumptions_data]
consumption_dates = consumption_dates[:-1]

consumption_values = [entry['consumption'] for entry in consumptions_data]
consumption_values = consumption_values[:-1]
print(consumption_values)
print(temperature_max_values)
print(temperature_min_values)
print(consumption_dates)
print(temperature_dates)
print("test")
print("test")
print("test")

df = pd.DataFrame({
    'Data': [None] * size,
    'Consumo': [None] * size,
    'MA_3a5': [None] * size,
    'MA_3a9': [None] * size,
    'DayType': [None] * size,
    'Tmin': [None] * size,
    'Tmax': [None] * size
})

df

for i in range(8):
    df.at[i, 'Consumo'] = consumption_values[i]
    df.at[i, 'Data'] = consumption_dates[i]
for i in range(9, size):
    df.at[i, 'Data'] = temperature_dates[i - 9]
    df.at[i, 'Tmin'] = temperature_min_values[i - 9]
    df.at[i, 'Tmax'] = temperature_max_values[i - 9]

df['DayType'] = DayType(df)
df

for i in range(9, size):  # substituir pelo frame futuro correto
    df.at[i, 'MA_3a9'] = MediaMovel(df, -9, -3)[i]
    df.at[i, 'Consumo'] = intercept + np.dot(coefs, df.iloc[i, 3:])
df

previsão = df[['Data', 'Consumo']][9:]
previsão['Data'] = previsão['Data'].astype(str).str.strip("T").str[:10]
print(previsão.to_json(orient='records', date_format='iso'))
