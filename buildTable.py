import json
from database.Mysql import *
from myBaostock.Baostock import *
from utils.dataTransform import *
with open("stock_pool.json", 'r',encoding='UTF-8') as load_f:
    index = json.load(load_f)

stock_index = index['股票'].values()
stock_key = index['股票'].keys()
stock_key_bs = []
pyMysql = MysqlConnector(host="1.15.90.134", user="gtrepublic", passwd="123", auth_plugin="mysql_native_password")

bao = BaostockRebuild()

# for index in stock_index:
#     stock_id = stockIDtusharToBaostock(index)
#     db_id = stockIDBaostockToDB(stock_id)
#     stock_key_bs.append(db_id)
#     pyMysql.createTable(db_id)
#     bao = BaostockRebuild()
#     stock_id_data = bao.k_data_query(code=stock_id, char="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg,isST",
#                  start_date="2010-03-1", end_date="2021-03-01", frequency="d", adjustflag="3")
#     pyMysql.uploadData(stock_id_data,db_id)


