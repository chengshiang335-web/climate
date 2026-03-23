from datetime import date
import matplotlib.pyplot as plt
import meteostat as ms
import db_service
import meteostat
import pandas as pd

# Specify location and time range
POINT = ms.Point(50.1155, 8.6842, 113)  # Try with your location
START = date(2020, 1, 1)
END = date(2025, 12, 31)

# Get nearby weather stations
stations = ms.stations.nearby(POINT, limit=4)

# Get daily data & perform interpolation
ts = ms.daily(stations, START, END)
df = ms.interpolate(ts, POINT).fetch()

# Meteostat 欄位對應：tavg -> 均溫, tmax -> 高溫, tmin -> 低溫, rhum -> 濕度
df = df.reset_index()
 

weather_data = df[['time', 'temp', 'tmax', 'tmin', 'rhum']].copy()

# 只補數值欄位
weather_data[['temp', 'tmax', 'tmin', 'rhum']] = weather_data[['temp', 'tmax', 'tmin', 'rhum']].fillna(0)
 
# 時間
weather_data['time'] = weather_data['time']  # 先保持 pandas datetime

# 數值
weather_data['temp'] = weather_data['temp'].astype(float)
weather_data['tmax'] = weather_data['tmax'].astype(float)
weather_data['tmin'] = weather_data['tmin'].astype(float)
weather_data['rhum'] = weather_data['rhum'].astype(int)
 
weather_records = []

for row in weather_data.itertuples(index=False):
    weather_records.append((
        row.time.to_pydatetime(),  # ⭐ 轉 Python datetime
        float(row.temp),
        float(row.tmax),
        float(row.tmin),
        int(row.rhum)
    ))
 

db_service.insert_to_db(weather_records)
 


# Plot line chart including average, minimum and maximum temperature
# df.plot(y=[ms.Parameter.TEMP, ms.Parameter.TMIN, ms.Parameter.TMAX])
# plt.show()