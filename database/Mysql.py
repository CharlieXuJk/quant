import mysql.connector
import pandas as pd
from database.sql import *

class MysqlConnector:
    def __init__(self, host, user, passwd, auth_plugin):
        self.__myConnection = mysql.connector.connect(
            host=host,  # 数据库主机地址
            user=user,  # 数据库用户名
            passwd=passwd,  # 数据库密码
            auth_plugin=auth_plugin # 解决MYSQL 8.0默认加密模式不匹配问题
        )
        self.__myCursor = self.__myConnection.cursor()

    def __del__(self):
        self.__myConnection.close()

    def getCursor(self):
        return self.__myCursor

    def getConnection(self):
        return self.__myConnection

    def createTable(self, new_table, db="stock_data_day",):
        #todo:try-except
        self.__myCursor.execute(create_sql(new_table, db))

    def uploadData(self, dic, table, db="stock_data_day"):
        self.__myCursor.execute("USE %s;"%db)
        for value in dic.values:
            self.__myCursor.execute(upload_sql(table, value))
            self.__myConnection.commit()

    def downloadData(self, table, db="stock_data_day"):
        self.__myCursor.execute("USE %s;"%db)
        self.__myCursor.execute(download_sql(table))  # 执行SQL语句
        """
        使用fetchall函数以元组形式返回所有查询结果并打印出来
        fetchone()返回第一行，fetchmany(n)返回前n行
        游标执行一次后则定位在当前操作行，下一次操作从当前操作行开始
        """
        data = self.__myCursor.fetchall()

        # 下面为将获取的数据转化为dataframe格式
        columnDes = self.__myCursor.description  # 获取连接对象的描述信息
        columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
        result = pd.DataFrame([list(i) for i in data], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df
        result = result.apply(pd.to_numeric, axis=0, errors='ignore')
        result['date'] = pd.to_datetime(result['date'])
        return result

#
# sql = "SELECT * FROM score" # SQL语句
# dff=get_df_from_db(sql)
# dff
if __name__ == "__main__":
    pyMysql = MysqlConnector(host="1.15.90.134", user="gtrepublic", passwd="123", auth_plugin="mysql_native_password")
    myCursor = pyMysql.createCursor()
    # myCursor.execute("CREATE DATABASE TestDatabase")
    myCursor.execute("SHOW DATABASES")
    for x in myCursor:
        print(x)
    myCursor.execute("USE TestDatabase")
    # myCursor.execute("CREATE TABLE Test (name VARCHAR(255), url VARCHAR(255))")
    myCursor.execute("SHOW TABLES")
    for x in myCursor:
        print(x)
