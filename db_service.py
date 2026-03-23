import os
import json
import pymssql

def load_env():
    if not os.getenv("DB_USER"):
        try:
            with open("local.settings.json") as f:
                data = json.load(f)
                for k, v in data["Values"].items():
                    os.environ[k] = v
        except:
            pass

load_env()

def insert_to_db(weather_records):
    """
    寫回 SQL
    """
    #print(f"準備寫入 {len(records)} 筆資料...")

    load_env()  # 確保環境變數已經被載入

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

 

    print(f"從環境變數讀取資料庫連線資訊: server={server}, database={database}, user={user}, password={'*' * len(password) if password else None}") 

    if not all([server, database, user, password]):
        return "錯誤: 環境變數未設置"
    
    INS_SQL = """
        INSERT into dbo.WeatherData(time, temp, tmin, tmax, rhum) 
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """
    try:
        connect = pymssql.connect(server, user, password, database)
        cursor = connect.cursor()

        print("資料庫連線成功")

     # 優化點：executemany 會自動遍歷 records 中的所有 tuple 並執行 INSERT
        cursor.executemany(INS_SQL, weather_records)
 #       cursor.execute(INS_SQL, (time, temp, tmin, tmax, rhum))
        # pymssql 預設設定 autocommit = false
        connect.commit()

        print("資料寫入完畢")
        cursor.close()
        connect.close()
        return "成功"

    except Exception as e: 
        print(f'連線失敗: 原因{e}')
        return f"失敗: {e}"
