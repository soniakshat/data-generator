# Common plot


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.arima.model import ARIMA

# Load the data
data = pd.read_csv('ad_revenue.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Preprocess the data
data = data.asfreq('MS')  # Ensure monthly frequency
data['Revenue'] = data['Revenue'].interpolate(method='linear')  # Handle missing values

# Prepare data for models
X = np.array(range(len(data))).reshape(-1, 1)
y = data['Revenue'].values

# Train Linear Regression
lr_model = LinearRegression()
lr_model.fit(X, y)
lr_future = np.array(range(len(data), len(data) + 3)).reshape(-1, 1)
lr_predictions = lr_model.predict(lr_future)

# Train Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X, y)
rf_predictions = rf_model.predict(lr_future)

# Train ARIMA
arima_model = ARIMA(y, order=(5, 1, 0))
arima_model_fit = arima_model.fit()
arima_predictions = arima_model_fit.forecast(steps=3)

# Average predictions
average_predictions = (lr_predictions + rf_predictions + arima_predictions) / 3

# Print predictions
future_dates = [data.index[-1] + pd.DateOffset(months=i+1) for i in range(3)]
pred_df = pd.DataFrame({
    'Date': future_dates,
    'Linear Regression': lr_predictions,
    'Random Forest': rf_predictions,
    'ARIMA': arima_predictions,
    'Average': average_predictions
})
print(pred_df)

# Convert Timestamps to datetime for plotting
data.index = pd.to_datetime(data.index)
future_dates = pd.to_datetime(future_dates)

# Plot results
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Revenue'], label='Actual Revenue')

# Plot Linear Regression predictions
lr_full_predictions = np.concatenate([y, lr_predictions])
lr_dates = np.concatenate([data.index, future_dates])
plt.plot(lr_dates, lr_full_predictions, label='Linear Regression Predictions')

# Plot Random Forest predictions
rf_full_predictions = np.concatenate([y, rf_predictions])
plt.plot(lr_dates, rf_full_predictions, label='Random Forest Predictions')

# Plot ARIMA predictions
arima_full_predictions = np.concatenate([y, arima_predictions])
plt.plot(lr_dates, arima_full_predictions, label='ARIMA Predictions')

# Plot Average predictions
avg_full_predictions = np.concatenate([y, average_predictions])
plt.plot(lr_dates, avg_full_predictions, label='Average Predictions', linestyle='--')

plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Ad Revenue Predictions')
plt.legend()
plt.show()
