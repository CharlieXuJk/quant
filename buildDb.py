stock_id_data = bao.k_data_query(code="sh.000001",
                                 char="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg,isST",
                                 start_date="2010-03-1", end_date="2021-03-01", frequency="d", adjustflag="3")
print(stock_id_data.head())
