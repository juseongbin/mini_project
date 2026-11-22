#1. 신간 비율 계산
# DB에서 파이썬으로 데이터 불러오기
import pandas as pd
from connDB import conn

sql = """
SELECT data_month, title, publish_year, loan_count
FROM loan_ranking
"""

data = pd.read_sql(sql, conn)

# 1-1 신간 여부 판별
# 발행년도 정수 전환, publish_year 앞 4자리가 발행년도, 최근 2년 출판된 도서가 신간
# data_month.str(4)가 publish_year+2 보다 작으면 신간
data['publish_year'] = data['publish_year'].astype(int)
data['year'] = data['data_month'].str[:4].astype(int)
data['is_new'] = data['publish_year'] >= (data['year'] - 2)
print(data[['data_month', 'title', 'publish_year', 'year', 'is_new']].head(10))
# is_new가 True 면 신간, False 면 3년 이상 된 도서
# 이제 월별로 몇권이 신간인지 확인
monthly = data.groupby('data_month').agg(
    total=('title', 'count'),
    new_book=('is_new', 'sum'))

print(monthly)
# 신간 비율 계산
monthly['ratio'] = round(monthly['new_book'] / monthly['total'] * 100, 2)
print(monthly)
# 12월에서 1월로 넘어갈때 신간이 24개월분에서 12개월분으로 줄어서 비율이 줄어든 모양
# 월까지 계산해서 신간으로 계산하면(24개월) 더 좋을듯
# 아마 그렇다면 각 12월의 비율처럼 30퍼센트 후반정도를 유지할거같음
