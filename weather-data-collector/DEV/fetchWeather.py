import requests
import pyodbc
import time
from datetime import datetime

# MS SQL Server 연결
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=10.14.5.63,1433;'  # 서버 주소
            'DATABASE=kh16;'  # 데이터베이스 이름
            'UID=kh16;'  # 사용자 이름
            'PWD=waff!23;'  # 비밀번호
        )
        return conn
    except pyodbc.Error as e:
        print(f"Error while connecting to database: {e}")
        return None

# API 호출 함수
def fetch_weather_data():
    # 현재 날짜와 시간 가져오기
    now = datetime.now()
    # curr_date (yyyyMMdd 형식)
    curr_date = now.strftime("%Y%m%d")
    # curr_time (HHmm 형식)
    curr_time = now.strftime("%H%M")
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        "serviceKey": "8Yh6GlgLBbIgZ1JYvRq7NeX5P2inMFyObpoWictXBvJHDVmC/Q9wwLEWtZ/buw05JnijZxETxlcNWB8TH0LddQ==",
        "numOfRows": 10,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": curr_date,  # 현재 날짜 "20250331",  # 날짜
        "base_time": curr_time,  # 현재 시간 "1150",  # 시간
        "nx": 104,
        "ny": 83
    }
    try:
        print("params:", params)
        print("url:", url)
        response = requests.get(url, params=params)
        print("response.url:", response.url)
        response.raise_for_status()  # HTTP 에러가 있을 경우 예외 발생
        # print("API 호출")
        # print(response.text)  # JSON 또는 XML 데이터 출력
        # print(f"API 호출 결과: {response.status_code}")
        # print("API 호출 성공")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching weather data: {e}")
        return None
    

# 데이터 삽입 함수
def insert_data_to_db(weather_data, conn):
    cursor = conn.cursor()
    print("데이터 삽입 함수")
    try:
        for data in weather_data['response']['body']['items']['item']:
            base_date = data['baseDate']
            base_time = data['baseTime']
            category = data['category']
            value = data['obsrValue']
            
            # SQL 쿼리 작성 (테이블 예시: weather_data 테이블)
            query = """
            INSERT INTO weather_data (base_date, base_time, category, value, exec_date)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (base_date, base_time, category, value, datetime.now()))
        
        conn.commit()
        print(f"Data inserted at {datetime.now()}")
    except pyodbc.Error as e:
        print(f"Error while inserting data into the database: {e}")
        conn.rollback()  # 오류 발생 시 롤백
    except Exception as e:
        print(f"insert_data_to_db expected error occurred: {e}")
    finally:
        cursor.close()

# 메인 로직
def main():
    print("DB 연결")
    conn = None
    try:
        conn = get_db_connection()
        print(conn)
        if conn is None:
            print("Failed to connect to the database. Exiting...")
            return
        
        while True:
            # API에서 날씨 데이터 가져오기
            weather_data = fetch_weather_data()
            print("API에서 날씨 데이터 가져오기")
            print(weather_data)
            # 데이터를 데이터베이스에 삽입
            print("데이터를 데이터베이스에 삽입")
            insert_data_to_db(weather_data, conn)
            
            # 10분 대기
            print(f"Data inserted at {datetime.now()}")
            time.sleep(600)  # 10분 간격
    except KeyboardInterrupt:
            print("Process interrupted by user.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()  # 연결 종료

if __name__ == "__main__":
    main()
