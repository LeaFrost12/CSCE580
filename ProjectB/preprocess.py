

from meteostat import Point, Hourly
from datetime import datetime
import pandas as pd
import numpy as np

# Parameters
lat, lon = 34.0008, -81.0351
start = datetime(2024,5,26)
end = datetime(2024,5,27)
city = Point(lat, lon)

# Fetch
df = Hourly(city, start, end).fetch()
#print(df)

# ensure timestamps are datetime
df.index = pd.to_datetime(df.index)


# Select & rename columns
df = df[['temp', 'dwpt', 'rhum', 'prcp', 'wdir', 'wspd', 'pres', 'coco']]


# Ensure hourly continuity
full_idx = pd.date_range(start=df.index.min(), end=df.index.max(), freq='H', tz=df.index.tz)
df = df.reindex(full_idx)

# Assume NaN precip means 0
df['prcp'] = df['prcp'].fillna(0)
# add a rain flag (0 or 1)
df['rain_flag'] = (df['prcp'] > 0).astype(int)
print(df)

# Impute missing timestamps
# short gaps (<=3h): linear; long gaps: forward fill and add mask
gap_mask = df.isna().any(axis=1)
#print(gap_mask[1].sum())
df_short = df.interpolate(limit=3, limit_direction='both')
print(df_short)
df_long = df_short.fillna(method='ffill')
print(df_long)

# Standardize numerical units and clip outliers (3 sigma)
df_std= df_long.copy()
for col in ['temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'pres']:
    var = df_long[col]
    mu, sigma = var.mean(), var.std()
    # clip values greater than 3 stds
    clipped = var.clip(lower=mu - 3*sigma, upper=mu + 3*sigma)
    # standardize by subtracting mean then dividing by std
    df_long[col] = (clipped - clipped.mean()) / clipped.std()

print(df_long)

# Save cleaned dataset
df_long.to_parquet('city_weather_clean.parquet')

arr = [False, False, True, False, True]
df = pd.DataFrame(arr)
#print(df[0].sum())