import pandas as pd
import baostock as bs

class BaostockRebuild():
    def __init__(self):
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        if lg.error_msg == "success":
            print("登录成功")
            print('login respond error_code:' + lg.error_code)
            print('login respond  error_msg:' + lg.error_msg)
        else:
            print("登录错误")
            print('login respond error_code:' + lg.error_code)
            print('login respond  error_msg:' + lg.error_msg)

    def __del__(self):
        bs.logout()

    def baostock_logout(self):
        bs.logout()

    def k_data_query(self,code, char, start_date, end_date, frequency, adjustflag):
        """
        获取某只标的的K线数据
        :param code: 标的代码 eg；"000001.SH"
        :param char: 需要下载的数据特征 eg 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
                                        周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        :param start_date:  开始日期
        :param end_date:  结束日期
        :param frequency:  频率 数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，
                            不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
        :param adjustflag:  复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权
        :return: result
        """
        rs = bs.query_history_k_data_plus(code,
                                          char,
                                          start_date=start_date, end_date=end_date,
                                          frequency=frequency, adjustflag=adjustflag)
        result = rs.get_data()
        # 将字符串数值列的类型转成数值型
        result = result.apply(pd.to_numeric, axis=0, errors='ignore')

        # 删除股票停牌的行记录
        #result = result[result.tradestatus == 1]  # tradestatus 1 正常交易， 0 停牌
        # 日期列的类型
        result['date'] = pd.to_datetime(result['date'])
        return result

    def div_info_query(self, code, year, yearType):
        """
        通过API接口获取除权除息信息数据（预披露、预案、正式都已通过）
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param year: 年份，如：2017。此参数不可为空；
        :param yearType: 年份类别，默认为"report":预案公告年份，可选项"operate":除权除息年份。此参数不可为空。
        :return: rs_list
        """
        rs_list = []
        rs_dividend_2015 = bs.query_dividend_data(code=code, year=year, yearType=yearType)
        while (rs_dividend_2015.error_code == '0') & rs_dividend_2015.next():
            rs_list.append(rs_dividend_2015.get_row_data())
        return rs_list

    def profitability_info_query(self, code, year, quarter):
        """
        通过API接口获取季频盈利能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param year: 统计年份，为空时默认当前年；
        :param quarter:统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        :return: result_profit
        """
        profit_list = []
        rs_profit = bs.query_profit_data(code=code, year=year, quarter=quarter)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        return result_profit

    def opeation_info_query(self, code, year, quarter):
        """
        通过API接口获取季频营运能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param year: 统计年份，为空时默认当前年；
        :param quarter:统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        :return: result_profit
        """
        profit_list = []
        rs_profit = bs.query_operation_data(code=code, year=year, quarter=quarter)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        return result_profit

    def growth_info_query(self, code, year, quarter):
        """
        通过API接口获取季频成长能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param year: 统计年份，为空时默认当前年；
        :param quarter:统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        :return: result_profit
        """
        profit_list = []
        rs_profit = bs.query_growth_data(code=code, year=year, quarter=quarter)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        return result_profit

    def balance_info_query(self, code, year, quarter):
        """
        通过API接口获取季频偿债能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param year: 统计年份，为空时默认当前年；
        :param quarter:统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        :return: result_profit
        """
        profit_list = []
        rs_profit = bs.query_balance_data(code=code, year=year, quarter=quarter)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        return result_profit

    def cashflow_info_query(self, code, year, quarter):
        """
        通过API接口获取季频现金流量信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param year: 统计年份，为空时默认当前年；
        :param quarter:统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        :return: result_profit
        """
        profit_list = []
        rs_profit = bs.query_cash_flow_data(code=code, year=year, quarter=quarter)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        return result_profit

    def query_dupont_data(self, code, year, quarter):
        """
        通过API接口获取季频杜邦指数信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param year: 统计年份，为空时默认当前年；
        :param quarter:统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        :return: result_profit
        """
        profit_list = []
        rs_profit = bs.query_cash_flow_data(code=code, year=year, quarter=quarter)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        return result_profit

    def performance_express_report_query(self, code, start_date, end_date):
        """
        通过API接口获取季频公司业绩快报信息，可以通过参数设置获取起止年份数据，提供2006年至今数据。除几种特殊情况外，交易所未要求必须发布。
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param start_date: 开始日期，发布日期或更新日期在这个范围内；
        :param end_date: 结束日期，发布日期或更新日期在这个范围内。
        :return: result
        """
        rs = bs.query_performance_express_report(code=code, start_date=start_date, end_date=end_date)
        print('query_performance_express_report respond error_code:' + rs.error_code)
        print('query_performance_express_report respond  error_msg:' + rs.error_msg)

        result_list = []
        while (rs.error_code == '0') & rs.next():
            result_list.append(rs.get_row_data())
            # 获取一条记录，将记录合并在一起
        result = pd.DataFrame(result_list, columns=rs.fields)
        return result

    def forcast_report_query(self, code, start_date, end_date):
        """
        通过API接口获取季频公司业绩预告信息，可以通过参数设置获取起止年份数据，提供2003年至今数据。除几种特殊情况外，交易所未要求必须发布。
        :param code: 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param start_date: 开始日期，发布日期或更新日期在这个范围内；
        :param end_date: 结束日期，发布日期或更新日期在这个范围内。
        :return: result
        """
        #### 获取公司业绩预告 ####
        rs_forecast = bs.query_forecast_report(code=code, start_date=start_date, end_date=end_date)
        print('query_forecast_reprot respond error_code:' + rs_forecast.error_code)
        print('query_forecast_reprot respond  error_msg:' + rs_forecast.error_msg)
        rs_forecast_list = []
        while (rs_forecast.error_code == '0') & rs_forecast.next():
            # 分页查询，将每页信息合并在一起
            rs_forecast_list.append(rs_forecast.get_row_data())
        result_forecast = pd.DataFrame(rs_forecast_list, columns=rs_forecast.fields)
        #### 结果集输出到csv文件 ####
        return result_forecast

"下一个方式是证券基本资料  http://baostock.com/baostock/index.php/%E8%AF%81%E5%88%B8%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99"

if __name__ == "__main__":
    bao = BaostockRebuild()
    sh000001 = bao.k_data_query(code="000001.SH", char="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
                 start_date="2019-01-10", end_date="2020-01-01", frequency="d", adjustflag="3")
    sh000001.to_csv("Test.csv")

    div_info_test = bao.div_info_query(code="sh.600000", year="2015", yearType="report")
    print()

    profitability_info = bao.profitability_info_query(code="sh.600000", year=2017, quarter=2)
    print(profitability_info)

    bao.baostock_logout()
