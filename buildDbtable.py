'''
CREATE TABLE `testdatabase`.`new_table` (
  `date` DATE NOT NULL,
  `code` VARCHAR(45) NULL,
  `open` DECIMAL(10,5) NULL,
  `high` DECIMAL(10,5) NULL,
  `low` DECIMAL(10,5) NULL,
  `close` DECIMAL(10,5) NULL,
  `volume` DECIMAL(25,9) NULL,
  `amount` DECIMAL(25,9) NULL,
  `adjustflag` INT NULL,
  `turn` DECIMAL(15,10) NULL,
  `new_tablecol` DECIMAL(15,10) NULL,
  PRIMARY KEY (`date`));
'''


import mysql.connector

mydb = mysql.connector.connect(
    host="1.15.90.134",
    user="gtrepublic",
    passwd="123",
    database="stock-data")
c = mydb.cursor()


#%%

c.execute('''CREATE TABLE SZ000002
( ID      INT PRIMARAY KEY  NOT NULL,
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
  DESCRIPTION CHAR(50));''')
mydb.commit()
print(2)