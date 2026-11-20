import csv
import numpy as np
import pandas as pd

data = pd.read_csv('인기대출도서_2024-01.csv', skiprows=12)
print(data)
print(data.head())
print(data.shape)
print(data.columns)

print(data.dtypes)
print(data['대출건수'])
data['대출건수'] = data['대출건수'].str.replace(',','')
data['대출건수'] = data['대출건수'].astype(int)
print(data.sort_values(by='대출건수', ascending=False).head(10))
over1000 = data[(data['대출건수']>1000)]

print(data.loc[data['대출건수'] > 1000, '대출건수'].mean())
print(data.loc[data['대출건수'] > 1000, '대출건수'].sum())

print(data['KDC'].value_counts())
print(data.groupby('KDC')['대출건수'].sum().sort_values(ascending=False))
print(data.groupby('KDC')['대출건수'].mean().sort_values(ascending=False))

print(data.groupby('KDC')['대출건수'].agg(['count','sum','mean']))

print(data.groupby('KDC')['대출건수'].agg(['count','sum','mean']).sort_values(by='mean', ascending=False).head(5))

result = data.groupby('KDC')['대출건수'].agg(['count', 'sum', 'mean'])
result['대출비중(%)'] = round(result['sum'] / data['대출건수'].sum() * 100, 2)
result = result.rename(columns={
    'count': '도서수',
    'sum': '총대출건수',
    'mean': '평균대출건수'
})
print(result.sort_values(by='평균대출건수', ascending=False).head(3))