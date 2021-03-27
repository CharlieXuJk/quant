# %%

import json

with open("stock_pool.json", 'r', encoding='UTF-8') as load_f:
    index = json.load(load_f)

# %%

stock_index = index['股票'].values()
stock_key = index['股票'].keys()


# %%

def tushareToBaostock(str):
    return str.split('.')[1].lower() + '.' + str.split('.')[0]


# %%

temp = "ww.com"
print(tushareToBaostock(temp))

# %%

baostock_index = list(map(tushareToBaostock, stock_index))
c = dict(zip(stock_key, stock_index))

# %%

import pandas as pd
import Baostock as bs

code = list(c.values())[0]
lg = bs.login()
rs = bs.query_history_k_data_plus(code,
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                  start_date='2012-06-01', end_date='2021-3-16',
                                  frequency="d", adjustflag="1")  # frequency="d"取日k线，adjustflag="3"默认不复权
print('query_history_k_data_plus respond error_code:' + rs.error_code)
print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

# %%

print(rs)


def baostockToDataframe(rs):
    li = []
    while (rs.error_code == '0') & rs.next():
        li.append(rs.get_row_data())
    print(li)

    result = pd.DataFrame(li, columns=rs.fields)
    result.close = result.close.astype('float64')
    result.open = result.close.astype('float64')
    result.low = result.low.astype('float64')
    result.high = result.high.astype('float64')
    result.volume = result.volume.astype('int')  # astype转换数组类型
    result.date = pd.to_datetime(result.date)
    result.index = pd.to_datetime(result.date)

    return result


# %%

import mysql.connector

mydb = mysql.connector.connect(
    host="1.15.90.134",
    user="gtrepublic",
    passwd="123",
    database="stock_data_day")
c = mydb.cursor()

# %%

data = baostockToDataframe(rs)
# data.to_sql(code, mydb, index=False, if_exists='append')
print(data.head())

# %%

command = "CREATE TABLE %d" \
    (ID)
c.execute('''
CREATE TABLE '''


