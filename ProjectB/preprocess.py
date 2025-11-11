

from meteostat import Point, Hourly
from datetime import datetime
import pandas as pd
import numpy as np

# Parameters
lat, lon = 34.009289, -81.037086
start = datetime(2020,1,1)
end = datetime(2024,1,1)
city = Point(lat, lon)

# Fetch
df = Hourly(city, start, end).fetch()
#print(df)

# Select & rename columns
df = df[['temp', 'rhum', 'pres', 'wspd', 'prcp']]


# Ensure hourly continuity
full_idx = pd.date_range(start=df.index.min(), end=df.index.max(), freq='H', tz=df.index.tz)
df = df.reindex(full_idx)

# Impute missing timestamps
# short gaps (<=3h): linear; long gaps: forward fill and add mask
gap_mask = df.isna().any(axis=1)
print(gap_mask[1].sum())
df_short = df.interpolate(limit=3, limit_direction='both')
df_long = df_short.fillna(method='ffill')

# Standardize units and clip obvious outliers (3 sigma)
for col in ['temp','rhum','pres','wspd','prcp']:
    series = df_long[col]
    mu, sigma = series.mean(), series.std()
    df_long[col] = series.clip(lower=mu-3*sigma, upper=mu+3*sigma)

#print(df_long)

# Save cleaned dataset
#df_long.to_parquet('city_weather_clean.parquet')

arr = [False, False, True, False, True]
df = pd.DataFrame(arr)
print(df[0].sum())