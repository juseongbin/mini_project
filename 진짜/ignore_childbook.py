# 아동도서 제외
# https://nl.go.kr/seoji/contents/S20101050000.do 참고하여서 isbn 부가기호를 참고
# 부가기호의 첫 자리가 4,5,6,7인 경우 아동도서로 분류
# 부가기호의 자릿수가 총 4자리인 경우 맨 앞자리를 0으로 간주
import pandas as pd
from connDB import conn
# isbn 부가기호와 그 갯수
sql = """
SELECT isbn_add_code, COUNT(*) AS count
FROM loan_ranking
GROUP BY isbn_add_code
ORDER BY count DESC
"""

data = pd.read_sql(sql, conn)

# 5자리가 될때까지 맨 앞자리를 0으로 채움
data['isbn_add_code'] = data['isbn_add_code'].str.zfill(5)
# 맨 앞자리 확인
data['first'] = data['isbn_add_code'].str[0]

result = data.groupby('first')['count'].sum()

print(result)
print(result.sum())
#결측치 164건
# 아동책만 선정
ignore = ['4','5','6','7']
# 전체 데이터 호출
sql = """
SELECT data_month, title, isbn, isbn_add_code, loan_count
FROM loan_ranking
"""

books = pd.read_sql(sql, conn)

#데이터 위와 같게 만들기
books['isbn_add_code'] = books['isbn_add_code'].str.zfill(5)

#어른책만 선정
kid_books = books[books['isbn_add_code'].str[0].isin(ignore)]
adult_books = books[~books['isbn_add_code'].str[0].isin(ignore)]

print('전체:', books.shape)
print('아동:', kid_books.shape)
print('제외 후:', adult_books.shape)