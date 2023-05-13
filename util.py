from datetime import datetime
import datetime as dt
import sql_connector
import pandas as pd
import log
from get_data import DataSource
import csv
import requests
import get_data

def get_share_list():
    url = "http://api.waizaowang.com/doc/getBaseInfo?type=1&code=all&fields=code&export=4&token=" + get_data.token
    ret = requests.get(url)
    return ret.text

def get_price(code ,date):
    conn = sql_connector.getConn()
    # 从数据库中读取股票数据
    cursor = conn.cursor()
    cursor.execute('select price from stock_' + code + ' where date=' + date + ';')
    price = 0
    for row in cursor:
        price = row[0]
    cursor.close()
    return price


def get_mlil(data_dict, date):
    try:
        mlil = data_dict[date].mlil
    except Exception:
        return 0
    return mlil


def get_begin_date(code):
    conn = sql_connector.getConn()
    cursor = conn.cursor()
    cursor.execute('select date from stock_' + code + ' order by date ASC;')
    result = cursor.fetchall()

    for row in result:
        return row[0]
    while cursor.nextset():
        pass
    cursor.close()


def get_end_date(code):
    conn = sql_connector.getConn()
    cursor = conn.cursor()
    cursor.execute('select date from stock_' + code + ' order by date DESC;')
    result = cursor.fetchall()
    for row in result:
        return row[0]
    while cursor.nextset():
        pass
    cursor.close()


def dates_Between(startDate, endDate):
    date1 = datetime.strptime(startDate, '%Y%m%d')
    date2 = datetime.strptime(endDate, '%Y%m%d')
    # Calculate the difference between the two dates
    delta = date2 - date1
    # Extract the number of days from the timedelta object
    days_between = delta.days
    return days_between


def get_nth_workday(date, n):
    # 获取 A 股交易日历
    trade_days = getStockTradeDate('trade_date_a_gu.csv')
    # 获取交易日历中的所有开盘日

    # 将日期字符串转换为 datetime 对象
    current_date = datetime.strptime(date, "%Y%m%d").date()
    try:
    # 从给定日期开始往前计算开盘日
        while n > 0:
            # 计算前一天的日期
            current_date -= dt.timedelta(days=1)

            # 判断前一天是否为开盘日
            if current_date.strftime('%Y-%m-%d') in trade_days:
                n -= 1
    except Exception:
        print('oadkofoaf')
    return current_date.strftime("%Y%m%d")


def get_bth_workday(date, n):
    # 获取 A 股交易日历
    trade_days = getStockTradeDate('trade_date_a_gu.csv')
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

def getStockTradeDate(file_name):
    tdates = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # 跳过CSV文件的标题行
        next(reader)
        for row in reader:
            # 如果isopen列的值为1，则将tdate列的值添加到tdates列表中
            if row[2] == '1':
                tdates.append(row[0])
    return tdates


if __name__ == '__main__':
    date_str = '20230427'
