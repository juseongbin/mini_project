import csv
f = open('인기대출도서_2024-01.csv', 'r', encoding='utf-8-sig')
lines = csv.reader(f)
for i in range(12):
    next(lines)

header = next(lines)

count = 0
total = 0
max_loan = 0
max_title = ''
min_loan = 9999
min_title = ''
overavgloan = 0
loan_list = []

for i in range(200):
    data = next(lines)
    count += 1
    loan = int(data[9].replace(',', ''))
    total += loan
    loan_list.append(loan)
    if loan > max_loan:
        max_loan = loan
        max_title = data[1]
    if loan <= min_loan:
        min_loan = loan
        min_title = data[1]

    
avg = (total/count)
for loan in loan_list:
    if loan > avg:
        overavgloan += 1

print(f' 200등 책 : {min_title}, {min_loan}권')
print(f' 최다대출책 : {max_title}, {max_loan}권')
print(f'24년 1월 상위 200등 건수 : {total}')
print(f'총 건수 : {count}')
print(f'평균 대출 건수 : {round(avg,2)}')
print(f'평균이상 대출건수 : {overavgloan}')
print(f'평균미만 대출건수 : {200-overavgloan}')


f.close()