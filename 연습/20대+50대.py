import os
import pymysql
conn = pymysql.connect(host='localhost', user='student',
password=os.environ.get('DB_PASSWORD', ''),
database='프로젝트_연습', charset='utf8mb4')
cur = conn.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())
cur.execute("SHOW TABLES")
print(cur.fetchall())
conn.close()