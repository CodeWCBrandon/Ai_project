import numpy as np
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

Tk().withdraw()
file_path = filedialog.askopenfilename()
data = pd.read_csv(file_path)

# normalize column names (strip spaces)
data.columns = data.columns.str.strip()

# ensure types
data['Item Code'] = data['Item Code'].astype('string')
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')                     # convert to datetime
data['Quantity Sold (kilo)'] = pd.to_numeric(data['Quantity Sold (kilo)'], errors='coerce')

# print(data.head())
# print(data['Item Code'].unique())

for unique_code in data['Item Code'].unique():
    item_data = data[data['Item Code'] == unique_code].copy()

    # aggregate by date
    item_data = item_data.groupby('Date', as_index=False)['Quantity Sold (kilo)'].sum()

    # drop invalid dates / negative or NaN y
    item_data = item_data[item_data['Date'].notna()]
    item_data = item_data[item_data['Quantity Sold (kilo)'].notna() & (item_data['Quantity Sold (kilo)'] >= 0)]

    if item_data.shape[0] < 2:
        print(f"Not enough data for {unique_code}, skipping.")
        continue

    item_data = item_data.rename(columns={'Date': 'ds', 'Quantity Sold (kilo)': 'y'})

    # initialize and fit
    model = Prophet(yearly_seasonality=False, changepoint_prior_scale=0.001)
    model.add_seasonality(name='yearly', period=365.25, fourier_order=9)
    model.add_seasonality(name='weekly', period=7, fourier_order=3)
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)

    model.fit(item_data)        # pass the DataFrame directly

    future = model.make_future_dataframe(periods=360)
    forecast = model.predict(future)

    # Print on specific date
    predicted_demand = forecast[forecast['ds'] == '2023-02-08']['yhat'].item()
    print('Predicted demand on 2024-06-20 is', predicted_demand)

    # Print based on forecast
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    # plotting
    # fig = model.plot(forecast)
    # plt.show()
    break
