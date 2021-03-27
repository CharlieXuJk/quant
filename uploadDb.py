from Mysql_operation import *
from BaoStock import *

if __name__ == "__main__":
    bao = BaostockRebuild()
    pyMysql = MysqlConnector(host="localhost", user="root", passwd="Your Password", auth_plugin="mysql_native_password")
    myCursor = pyMysql.createCursor()
    connection = pyMysql.getConnection()

    sh000001 = bao.k_data_query(code="000001.SH", char="date,code,open,high,low,close,volume,amount,adjustflag,"
                                                       "turn,pctChg",
                 start_date="2019-01-10", end_date="2020-01-01", frequency="d", adjustflag="3")
    myCursor.execute("USE TestDatabase")
    print(sh000001.keys())
    for item in sh000001.values:
        print(item)
        date = item[0]
        code = item[1]
        open = float(item[2])
        high = float(item[3])
        low = float(item[4])
        close =float(item[5])
        volume = float(item[6])
        amount = float(item[7])
        adjustflag = int(item[8])
        turn = float(item[9])
        pctChg = float(item[10])
        myCursor.execute("INSERT INTO %s "
                         "VALUES ('%s', '%s',%s,%s,%s,%s,%s,%s,%s,%s,%s)" % ('sh000001', item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]
        ,item[10]))
        connection.commit()
