import json
import time
from database.Mysql import *
from myBaostock.Baostock import *
from utils.dataTransform import *
with open("../stock_pool.json", 'r', encoding='UTF-8') as load_f:
    index = json.load(load_f)

bao = BaostockRebuild()
pyMysql = MysqlConnector(host="1.15.90.134", user="gtrepublic", passwd="123", auth_plugin="mysql_native_password")

stock_index = index['股票'].values()
stock_key = index['股票'].keys()
stock_key_bs = []


for index in stock_index:
    stock_id = stockIDtusharToBaostock(index)
    stock_id_data = bao.k_data_query(code=stock_id,
                                     char="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg,isST",
                                     start_date="2010-03-01", end_date="2021-03-01", frequency="d", adjustflag="3")
    print(stock_id_data.head())
    db_id = stockIDBaostockToDB(stock_id)
    pyMysql.uploadData(stock_id_data, db_id)
    time.sleep(1)