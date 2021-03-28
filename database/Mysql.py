import mysql.connector

class MysqlConnector:
    def __init__(self, host, user, passwd, auth_plugin):
        self.__myConnection = mysql.connector.connect(
            host=self.host,  # 数据库主机地址
            user=self.user,  # 数据库用户名
            passwd=self.passwd,  # 数据库密码
            auth_plugin=self.auth_plugin # 解决MYSQL 8.0默认加密模式不匹配问题
        )
        self.__myCursor = self.connection.cursor()

    def __del__(self):
        __myConnection.close()

    def getCursor(self):
        return self.__myCursor

    def getConnection(self):
        return self.__myConnection

    def createTable(self, new_table, db="stock_data_day",):
        #todo:try-except
        __myCursor.execute('''
            CREATE TABLE '%s'.'%s' (
            'date' DATE NOT NULL,
            'code' VARCHAR(45) NULL,
            'open' DECIMAL(10,5) NULL,
            'high' DECIMAL(10,5) NULL,
            'low' DECIMAL(10,5) NULL,
            'close' DECIMAL(10,5) NULL,
            'volume' DECIMAL(25,9) NULL, 
            'amount' DECIMAL(25,9) NULL,
            'adjustflag' INT NULL,
            'turn' DECIMAL(15,10) NULL,
            'new_tablecol' DECIMAL(15,10) NULL,
            PRIMARY KEY ('date')); 
            '''%(db, newtable)
        )

    def uploadData(self, dic, table, db="stock_data_day"):
        __myCursor.execute("USE %s;"%db)
        for value in dic.values:
            myCursor.execute("INSERT INTO %s "
                             "VALUES ('%s', '%s',%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
                             table, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7],
                             value[8], value[9]
                             , value[10]))
            __connection.commit()

    def downloadData(self, db):
        cursor = db.cursor()  # 使用cursor()方法获取用于执行SQL语句的游标
        cursor.execute(sql)  # 执行SQL语句
        """
        使用fetchall函数以元组形式返回所有查询结果并打印出来
        fetchone()返回第一行，fetchmany(n)返回前n行
        游标执行一次后则定位在当前操作行，下一次操作从当前操作行开始
        """
        data = cursor.fetchall()

        # 下面为将获取的数据转化为dataframe格式
        columnDes = cursor.description  # 获取连接对象的描述信息
        columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
        df = pd.DataFrame([list(i) for i in data], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df

        """
        使用完成之后需关闭游标和数据库连接，减少资源占用,cursor.close(),db.close()
        db.commit()若对数据库进行了修改，需进行提交之后再关闭
        """
        cursor.close()
        db.close()

        print("cursor.description中的内容：", columnDes)
        return df


sql = "SELECT * FROM score" # SQL语句
dff=get_df_from_db(sql)
dff
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
