import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='love',
    database='miniproject',
    charset='utf8mb4'
)

print('DB 연결 성공')