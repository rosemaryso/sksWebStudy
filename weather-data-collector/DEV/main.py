import requests
import pyodbc
import schedule
import time
import json
from config import DB_CONFIG

# 기상청 API 호출
def fetch_weather_data():
    # url = "http://marineweather.nmpnt.go.kr:8001/openWeatherNow.do"
    # params = {"lat": "35.0", "lon": "129.0"}
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        "serviceKey": "8Yh6GlgLBbIgZ1JYvRq7NeX5P2inMFyObpoWictXBvJHDVmC/Q9wwLEWtZ/buw05JnijZxETxlcNWB8TH0LddQ==",
        "numOfRows": 10,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": "20250331",  # 날짜
        "base_time": "1150",  # 시간
        "nx": 104,
        "ny": 83
    }

    # API URL 설정
    # url_sea_obs = "https://apihub.kma.go.kr/api/typ01/url/sea_obs.php?tm=20250330&stn=22189&help=0&authKey=CH8XAAZ1Qxq_FwAGdcMa8w"
    url_sea_obs = "https://apihub.kma.go.kr/api/typ01/url/sea_obs.php"
    params_sea_obs = {
        "tm": "20250330",       # 날짜
        "stn": "22189",         # 측정소 ID
        "help": "0",            # 도움말 비활성화
        "authKey": "CH8XAAZ1Qxq_FwAGdcMa8w"  # 인증키 (개인별 다름)
    }

    try:
        responseSeaObs = requests.get(url_sea_obs, params=params_sea_obs)
        # 응답 확인
        if responseSeaObs.status_code == 200:
            print("API 호출 성공")
            print(responseSeaObs.text)  # JSON 또는 XML 데이터 출력
        else:
            print(f"API 호출 실패: {responseSeaObs.status_code}")
        
        response = requests.get(url, params=params)
        response.raise_for_status()    
        return response.json()
    except requests.RequestException as e:
        print(f"API 요청 실패: {e}")
        response = requests.get(url, params=params)
        # 응답 확인
        if response.status_code == 200:
            print("API 호출 성공")
            print(response.text)  # JSON 또는 XML 데이터 출력
        else:
            print(f"API 호출 실패: {response.status_code}")
        return None

# MS-SQL에 데이터 저장
def save_to_mssql(data):
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']}"
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = "INSERT INTO TB_ULTRASRTNCST (baseDate, baseTime, category, nx, ny, obsrValue, INDATE, URL) VALUES (GETDATE(), ?, ?, ?, ?, ?, ?, GETDATE(), ?)"
        cursor.execute(query, data["baseDate"], data["baseTime"], data["category"], data["nx"], data["ny"], data["obsrValue"], data)
        conn.commit()
        cursor.close()
        conn.close()
        print("데이터 저장 성공")
    except Exception as e:
        print(f"MS-SQL 저장 실패: {e}")

# JSON 데이터를 SQL에 저장하는 함수
def save_to_mssql_TEST(data):
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']}"
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # 예제: JSON 데이터에서 필요한 값 추출
        wave_height = data.get("waveHeight", None)
        wind_speed = data.get("windSpeed", None)

        query = "INSERT INTO weather_data (timestamp, wave_height, wind_speed) VALUES (GETDATE(), ?, ?)"
        cursor.execute(query, wave_height, wind_speed)

        conn.commit()
        cursor.close()
        conn.close()
        print("데이터 저장 성공")
    except Exception as e:
        print(f"MS-SQL 저장 실패: {e}")

# # API 데이터 받아서 저장
# api_response = requests.get(url_sea_obs, params=params_sea_obs)
# if api_response.status_code == 200:
#     json_data = json.loads(api_response.text)
#     save_to_mssql_TEST(json_data)

# 5분마다 실행
def job():
    print("기상청 API 데이터 요청...")
    data = fetch_weather_data()
    if data:
        save_to_mssql(data)

# 5분마다 실행
schedule.every(1).minutes.do(job)

# 실행 루프
print("스케줄러 시작...")
while True:
    schedule.run_pending()
    time.sleep(1)
