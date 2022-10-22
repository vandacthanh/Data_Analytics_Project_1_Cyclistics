#python3
import pandas as pd 
import glob 
import os 
from math import sin, cos, sqrt, atan2, radians


# Get the files path
csv_files = os.path.join("data/Sept_2021_Sept_2022/", "202*.csv")
csv_files = glob.glob(csv_files)

# Merge use concat
df = pd.concat(map(pd.read_csv, csv_files), ignore_index=True)

# Convert datetime format of two columns
df[['started_at_dt', 'ended_at_dt']] =  df[['started_at', 'ended_at']].apply(pd.to_datetime)

# Calculate Duration
df['duration'] = df['ended_at_dt'] - df['started_at_dt']

# Convert date to weekday (0=Monday, 6=Friday)
df['weekday'] =  pd.to_datetime(df['started_at']).dt.weekday

#Extract month-year
df['hour'] =  pd.to_datetime(df['started_at']).dt.hour
df['month'] =  pd.to_datetime(df['started_at']).dt.month
df['year'] =  pd.to_datetime(df['started_at']).dt.year
df['month'] = df['month'].astype(str)
df['year'] = df['year'].astype(str)
df['month-year'] = df['month'] + "-" + df['year']

# Calculate the distance between trip

R = 6373.0 # Earth Radius

df['lat1'], df['lon1'], df['lat2'], df['lon2']  = df['start_lat'].apply(radians), df['start_lng'].apply(radians), df['end_lat'].apply(radians), df['end_lng'].apply(radians)

df['diff_lat'] = df['lat2'] - df['lat1']
df['diff_long'] = df['lon2'] - df['lon1']

df['a'] = df['diff_lat'].apply(lambda x: sin(x/ 2)**2) + df['lat1'].apply(lambda x: cos(x)) * df['lat2'].apply(lambda x: cos(x)) * df['diff_long'].apply(lambda x: sin(x / 2)**2)
df['c'] = df['a'].apply(lambda x: 2 * atan2(sqrt(x), sqrt(1 - x)))

df['distance (Km)'] = R * df['c']
df['distance Rounded (Km)'] = df['distance (Km)'].apply(lambda x: round(x, 1))

# Drop redundant columns
df = df.drop(['started_at', 'ended_at', 'start_lat' , 'start_lng', 'end_lat', 'end_lng', 'started_at_dt', 'ended_at_dt', 'lat1', 'lon1', 'lat2', 'lon2', 'diff_lat', 'diff_long', 'a', 'c' ], axis=1)
# Write output
df.to_csv('Sept_2021_Sept_2022.csv')
