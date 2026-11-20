import pandas as pd

data = pd.read_csv(
    'csv/인기대출도서_2024-01.csv',
    skiprows=12
)

print(data.head())
print(data.shape)
print(data.columns)
print(data.dtypes)

data.drop('Unnamed: 10', axis=1, inplace=True)
data['대출건수'] = data['대출건수'].str.replace(',','').astype(int)
data['ISBN'] = data['ISBN'].astype(str)

print(data.shape)
print(data.dtypes)
print(data.isnull().sum())
#------------------------------
print(data[data['KDC'].isnull()])
print(data[data['권'].isnull()][['서명', '권']])
# KDC 결측인 책과 ISBN 부가기호가 결측인 책이 완전히 같음 코딩으로 가능 할것도 같은데 어려움,, 이 두개는 연산이 필요한 컬럼은 아니라 NULL로 둬도 될듯 KDC통계에 좀 이상이 있을거같긴 함 0으로 대입 불가능
# 권 결측은 단권의 경우 NAN을 넣어둔거같아서 좀 고민해보고 0 아니면 1 을 넣으면 될듯 - 단권의 경우 1로 했음
data['권'] = data['권'].fillna(1)
