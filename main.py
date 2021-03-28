from myBaostock import Baostock
from database import Mysql

if __name__ == "__main__":
    bao = Baostock.BaostockRebuild()
    sh000001 = bao.k_data_query(code="000001.SH", char="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
                 start_date="2019-01-10", end_date="2020-01-01", frequency="d", adjustflag="3")
    #sh000001.to_csv("Test.csv")

    #div_info_test = bao.div_info_query(code="sh.600000", year="2015", yearType="report")

    #profitability_info = bao.profitability_info_query(code="sh.600000", year=2017, quarter=2)
    #print(profitability_info)

    db = Mysql.MysqlConnector(host="1.15.90.134", user="gtrepublic", passwd="123", auth_plugin="mysql_native_password")
    db.createTable("sh000001")
