import mysql.connector

mydb = mysql.connector.connect(
    host="1.15.90.134",
    user="gtrepublic",
    passwd="123",
    database="stock-data")
c = mydb.cursor()

c.execute('''CREATE TABLE SZ000002
( ID      INT   NOT NULL AUTO_INCREMENT,
  TIME    TEXT              NOT NULL,
  CODE    TEXT              NOT NULL,
  HIGH    REAL                      ,
  LOW     REAL                      ,
  CLOSE   REAL                      ,
  OPEN    REAL                      ,
  PRECLOSE REAL                     ,
  VOLUME  REAL                      ,
  AMOUNT  REAL                      ,
  ADJUSTFLAG INT                    ,
  TURN    REAL                      ,
  TRADESTATUS INT                   ,
  PCTCHG  REAL                      ,
  PRTTM   REAL                      ,
  PSTTM   REAL                      ,
  PCFNCFTTM REAL                    ,
  PBMRQ   REAL                      ,
  ISST    INT                       ,
  DESCRIPTION CHAR(50)              ,
  PRIMARY KEY(ID))ENGING = MySQL DEFAULT CHARSET=utf8;''')
mydb.commit()



#%%



