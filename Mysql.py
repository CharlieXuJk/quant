import mysql.connector

class MysqlConnector():
    def __init__(self, host, user, passwd, auth_plugin):

        self.host = host
        self.user = user
        self.passwd = passwd
        self.auth_plugin = auth_plugin
        self.connection = mysql.connector.connect(
            host=self.host,  # 数据库主机地址
            user=self.user,  # 数据库用户名
            passwd=self.passwd,  # 数据库密码
            auth_plugin=self.auth_plugin # 解决MYSQL 8.0默认加密模式不匹配问题
        )

    def __del__(self):


    def createCursor(self):
        myCursor = self.connection.cursor()
        return myCursor

    def get_connection(self):
        return self.connection

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
