def create_sql(db, new_table):
    sql = '''
        CREATE TABLE %s.%s (
        date DATE NOT NULL,
        code VARCHAR(45) NULL,
        open DECIMAL(10,5) NULL,
        high DECIMAL(10,5) NULL,
        low DECIMAL(10,5) NULL,
        close DECIMAL(10,5) NULL,
        volume DECIMAL(25,9) NULL, 
        amount DECIMAL(25,9) NULL,
        adjustflag INT NULL,
        turn DECIMAL(15,10) NULL,
        new_tablecol DECIMAL(15,10) NULL,
        PRIMARY KEY (date)) ENGINE = InnoDB DEFAULT CHARSET=utf8;
        ''' % (db, new_table)
    return sql


def upload_sql(table, value):
    sql = '''
        INSERT INTO %s 
        VALUES ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE code = '%s', 
                                open = %s,
                                high = %s,
                                low = %s,
                                close = %s,
                                volume = %s,
                                amount = %s,
                                adjustflag = %s,
                                turn = %s,
                                new_tablecol = %s;
        ''' % (table, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7],
                             value[8], value[9], value[10], value[1], value[2], value[3], value[4], value[5], value[6], value[7],
                             value[8], value[9], value[10])
    return sql

def download_sql(table):
    sql = '''
        SELECT *
        FROM %s as u 
        WHERE u.date>'2019-03-01' AND u.date<'2019-04-01';
        '''%table
    return sql
