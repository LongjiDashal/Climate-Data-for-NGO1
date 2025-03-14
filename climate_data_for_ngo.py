"""Climate Data for NGO

Original file is located at
    https://colab.research.google.com/drive/1P3dRgqsgM-X_19YujIiNvH1H9E1zvN7X
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import pymannkendall as mk
from scipy.stats import pearsonr
from climate_indices import indices
import geopandas as gpd
import xarray as xr

import pandas as pd
df = pd.read_csv("RoC.csv")

print(df.head(5))

# Convert to datetime format
df['Date'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']])
df.set_index('Date', inplace=True)

# 1. Check column names
print("Columns in DataFrame:", df.columns.tolist())

# 2. Plot
plt.figure(figsize=(12,5))
plt.plot(
    df.index,
    df['MERRA-2 Temperature at 2 Meters (C) '],  # Use the renamed column
    label='Temperature',
    color='blue'
)
plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Trend Over Time")
plt.legend()
plt.show()

temp_series = df['MERRA-2 Temperature at 2 Meters (C) ']

# Fit ARIMA Model
model = ARIMA(temp_series, order=(1,1,1))
arima_result = model.fit()

# Forecast Next 10 Years
forecast = arima_result.forecast(steps=365*10)

# Plot ARIMA Forecast
plt.figure(figsize=(12,5))
plt.plot(temp_series, label='Historical Data')
plt.plot(pd.date_range(start=temp_series.index[-1], periods=365*10, freq='D'), forecast, label='Forecast', color='red')
plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Forecast using ARIMA")
plt.legend()
plt.show()

from scipy.stats import pearsonr
precipitation = df['MERRA-2 Precipitation Corrected (mm/day)']
temperature = df['MERRA-2 Temperature at 2 Meters (C) ']

correlation, p_value = pearsonr(temperature, precipitation)
print(f"Pearson Correlation between Temperature and Precipitation: {correlation:.3f}, p-value: {p_value:.3f}")

# Scatter Plot
sns.scatterplot(x=temperature, y=precipitation)
plt.xlabel("Temperature (°C)")
plt.ylabel("Precipitation (mm/day)")
plt.title("Correlation between Temperature and Precipitation")
plt.show()

# Spatial Analysis 
import geopandas as gpd

# Convert 'Longitude' and 'Latitude' columns to numeric, handling errors
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')

# Remove rows with invalid coordinates (NaN after conversion)
df = df.dropna(subset=['Longitude', 'Latitude'])

# Now create the GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# Plot Spatial Distribution of Temperature
gdf.plot(column='MERRA-2 Temperature at 2 Meters (C) ', cmap="coolwarm", legend=True, figsize=(10,6))
plt.title("Spatial Distribution of Temperature")
plt.show()

#Extreme Value Analysis
from scipy.stats import genextreme

# Fit Generalized Extreme Value (GEV) Distribution
gev_params = genextreme.fit(df['MERRA-2 Temperature at 2 Meters (C) '])
print("GEV Distribution Parameters:", gev_params)

# Agriculture: Impact of Temp on Crop Yield (Hypothetical Example)
df['Crop_Yield'] = np.random.uniform(1, 5, len(df))  # Placeholder Crop Yield Data
crop_model = sm.OLS(df['Crop_Yield'], sm.add_constant(df[['MERRA-2 Temperature at 2 Meters (C) ', 'MERRA-2 Precipitation Corrected (mm/day)']])).fit()
print("Agriculture Impact Analysis:\n", crop_model.summary())

# Water Resources: Decline in Streamflow
df['Streamflow'] = np.random.uniform(10, 100, len(df))  # Placeholder Streamflow Data
streamflow_model = sm.OLS(df['Streamflow'], sm.add_constant(df[['MERRA-2 Temperature at 2 Meters (C) ', 'MERRA-2 Precipitation Corrected (mm/day)']])).fit()
print("Water Resources Impact Analysis:\n", streamflow_model.summary())

# Health: Climate Impact on Disease Cases
df['Disease_Cases'] = np.random.randint(5, 100, len(df))  # Placeholder Disease Data
health_model = sm.OLS(df['Disease_Cases'], sm.add_constant(df[['MERRA-2 Temperature at 2 Meters (C) ', 'MERRA-2 Precipitation Corrected (mm/day)']])).fit()
print("Health Impact Analysis:\n", health_model.summary())
