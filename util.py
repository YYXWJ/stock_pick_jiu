from datetime import datetime
import datetime as dt
import sql_connector
import pandas as pd
import log
from get_data import DataSource

def get_price(code ,date):
    conn = sql_connector.getConn()
    # 从数据库中读取股票数据
    cursor = conn.cursor()
    cursor.execute('select price from stock_' + code + ' where date=' + date + ';')
    price = 0
    for row in cursor:
        price = row[0]
    cursor.close()
    conn.close()
    return price


def get_mlil(code, date):
    conn = sql_connector.getConn()
    # 从数据库中读取股票数据
    cursor = conn.cursor()
    cursor.execute('select mlil from stock_' + code + ' where date=' + date + ';')
    mlil = 0
    for row in cursor:
        mlil = row[0]
    cursor.close()
    conn.close()
    return mlil



def get_nth_workday(date, n):
    # 获取 A 股交易日历
    dataSource = DataSource()
    date_obj = datetime.strptime(date, "%Y%m%d")
    date_formatted = date_obj.strftime("%Y-%m-%d")
    trade_days = dataSource.getStockTradeDate('2022-01-01', date_formatted)
    # 获取交易日历中的所有开盘日

    # 将日期字符串转换为 datetime 对象
    current_date = datetime.strptime(date, "%Y%m%d").date()

    # 从给定日期开始往前计算开盘日
    while n > 0:
        # 计算前一天的日期
        current_date -= dt.timedelta(days=1)

        # 判断前一天是否为开盘日
        if current_date.strftime('%Y-%m-%d') in trade_days:
            n -= 1

    return current_date.strftime("%Y%m%d")

def get_bth_workday(date, n):
    # 获取 A 股交易日历
    dataSource = DataSource()
    date_obj = datetime.strptime(date, "%Y%m%d")
    date_formatted = date_obj.strftime("%Y-%m-%d")
    trade_days = dataSource.getStockTradeDate('2022-01-01', '2030-01-01')
    # 获取交易日历中的所有开盘日

    # 将日期字符串转换为 datetime 对象
    current_date = datetime.strptime(date, "%Y%m%d").date()

    # 从给定日期开始往前计算开盘日
    while n > 0:
        # 计算前一天的日期
        current_date += dt.timedelta(days=1)

        # 判断前一天是否为开盘日
        if current_date.strftime('%Y-%m-%d') in trade_days:
            n -= 1

    return current_date.strftime("%Y%m%d")


if __name__ == '__main__':
    date_str = '20230427'
    print(get_nth_workday(date_str, 50))