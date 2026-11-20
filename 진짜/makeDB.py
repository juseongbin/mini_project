import pandas as pd

files = ['csv/인기대출도서_2024-01.csv', 'csv/인기대출도서_2024-02.csv',
         'csv/인기대출도서_2024-03.csv','csv/인기대출도서_2024-04.csv'
         ,'csv/인기대출도서_2024-05.csv','csv/인기대출도서_2024-06.csv'
         ,'csv/인기대출도서_2024-07.csv','csv/인기대출도서_2024-08.csv'
         ,'csv/인기대출도서_2024-09.csv','csv/인기대출도서_2024-10.csv'
         ,'csv/인기대출도서_2024-11.csv','csv/인기대출도서_2024-12.csv'
         ,'csv/인기대출도서_2025-01.csv','csv/인기대출도서_2025-02.csv'
         ,'csv/인기대출도서_2025-03.csv','csv/인기대출도서_2025-04.csv'
         ,'csv/인기대출도서_2025-05.csv','csv/인기대출도서_2025-06.csv'
         ,'csv/인기대출도서_2025-07.csv','csv/인기대출도서_2025-08.csv'
         ,'csv/인기대출도서_2025-09.csv','csv/인기대출도서_2025-10.csv'
         ,'csv/인기대출도서_2025-11.csv','csv/인기대출도서_2025-12.csv']

data_list = []

for file in files:
    data = pd.read_csv(file,skiprows=12)
    data_list.append(data)

data = pd.concat(data_list, ignore_index=True)
data.drop('Unnamed: 10', axis=1, inplace=True)
data['대출건수'] = data['대출건수'].str.replace(',','').astype(int)
data['ISBN'] = data['ISBN'].astype(str)

# print(data.shape)
# print(data.dtypes)
# print(data.isnull().sum())
# #------------------------------
# print(data[data['KDC'].isnull()])
# print(data[data['권'].isnull()][['서명', '권']])
## KDC 결측인 책과 ISBN 부가기호가 결측인 책이 완전히 같음 코딩으로 가능 할것도 같은데 어려움,, 이 두개는 연산이 필요한 컬럼은 아니라 NULL로 둬도 될듯 KDC통계에 좀 이상이 있을거같긴 함 0으로 대입 불가능
## 권 결측은 단권의 경우 NAN을 넣어둔거같아서 좀 고민해보고 0 아니면 1 을 넣으면 될듯 - 단권의 경우 1로 했음
data['권'] = data['권'].fillna(1)

print('파일 개수:', len(files))
print('통합 데이터 크기:', data.shape)
print('컬럼 개수:', len(data.columns))
print('결측치 확인:')
print(data.isnull().sum())

data.rename(columns={
    '순위': 'ranking',
    '서명': 'title',
    '저자': 'author',
    '출판사': 'publisher',
    '출판년도': 'publish_year',
    '권': 'volume',
    'ISBN': 'isbn',
    'ISBN부가기호': 'isbn_add_code',
    'KDC': 'kdc',
    '대출건수': 'loan_count'
}, inplace=True)

print(data.columns)
rows = list(data.itertuples(index=False, name = None))
sql = """
INSERT INTO loan_ranking (
    ranking, title, author, publisher, publish_year,
    volume, isbn, isbn_add_code, kdc, loan_count
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
from connDB import conn
data = data.astype(object).where(pd.notna(data), None)

rows = list(data.itertuples(index=False, name=None))

cursor = conn.cursor()

cursor.executemany(sql, rows)

conn.commit()

print('데이터 입력 완료')
print('입력 행 수:', cursor.rowcount)

cursor.close()
conn.close()