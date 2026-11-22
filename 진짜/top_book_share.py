# 2. 상위 도서가 전체에서 차지하는 비율
# DB가져오기
import pandas as pd
from connDB import conn

sql = """
SELECT data_month, ranking, title, loan_count
FROM loan_ranking
"""

data = pd.read_sql(sql, conn)


# 대출 상위 10등 도서 선별, 월별 그룹화
top = data[data['ranking']<= 10]
top = top.groupby('data_month')['loan_count'].sum()
print(top)

# 월별 대출 도서 총합
total = data.groupby('data_month')['loan_count'].sum()
print(total)

# 월별 top 대출도서, 전체 대출도서 한 DB로 합치기
result = total.to_frame('total').join(top.to_frame('top'))
print(result)

# 점유율 = top/전체
result['ratio'] = round(result['top'] / result['total'] * 100, 2)

print(result)