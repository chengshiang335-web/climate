from datetime import date
import matplotlib.pyplot as plt
import meteostat as ms

# Specify location and time range

"""
    ms.Point( lat , long )  緯度 , 經度
"""
POINT = ms.Point(24.160887904904108, 120.65667192896451)
START = date(2023, 1, 1)
END = date(2025, 12, 31)

# 先找可用的 偵測點
stations = ms.stations.nearby(POINT, limit=4)   # 給予 stations 座標 並尋找附近的偵測點 抓回前四台 進行資料的擷取

# 時間跟資料填入
ts = ms.daily(stations, START, END)    # 從這些機器取出指定時段內的 資料
df = ms.interpolate(ts, POINT).fetch()

df_reindex = df.reset_index()   # 重新設定索引
print(df_reindex)
#df.to_csv("./weather_tc.csv", index=False)
#df.to_csv("./weather_tc.csv", index=True)
# df --> sql server database 存放 ---> power bi
# df --> power bi 做分析 ( df to_csv  --> import power bi)
#print(df)
# Plot line chart including average, minimum and maximum temperature
#df.plot(y=[ms.Parameter.TEMP, ms.Parameter.TMIN, ms.Parameter.TMAX])
#plt.show()


