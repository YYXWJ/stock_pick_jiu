import sql_connector
import pandas as pd
import datetime as dt
from datetime import datetime
import util

def calculate_ma_from_db(table, maList):
    """
    从数据库中读取股票数据，并计算均线
    :param host: 数据库主机名或IP地址
    :param user: 数据库用户名
    :param password: 数据库密码
    :param database: 数据库名
    :param table: 数据表名
    :param ma_list: 均线的天数列表
    :return: 包含均线的数据框
    """
    conn = sql_connector.getConn()
    # 从数据库中读取股票数据
    sql = "SELECT date, price FROM {}".format(table)
    data = pd.read_sql(sql, conn)

    # 计算均线
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    for i in maList:
        data['ma{}'.format(i)] = data['price'].rolling(window=i).mean()
    return data


def is_ma_60_up(code, date):
    conn = sql_connector.getConn()
    cursor = conn.cursor()
    cursor.execute('select price from stock_' + code + ' where date=' + date + ';')
    today_price = 0
    sixty_price = 0
    for row in cursor:
        today_price = row[0]
    cursor.execute('select price from stock_' + code + ' where date=' + util.get_nth_workday(date, 60) + ';')
    for row in cursor:
        sixty_price = row[0]
    cursor.close()
    conn.close()
    return today_price > sixty_price


def is_price_low_then_ma_60(code, date):
    conn = sql_connector.getConn()
    cursor = conn.cursor()
    ma_60 = calculate_ma_from_db('stock_' + code, [60])['ma60'][date]
    price = 0
    cursor.execute('select price from stock_' + code + ' where date=' + date + ';')
    for row in cursor:
        price = row[0]
    cursor.close()
    conn.close()
    return price < ma_60


def is_price_low_then_ma_60_this_week(code, date):
    # 今天一定要下穿60线
    if not is_price_low_then_ma_60(code, date):
        return False

    conn = sql_connector.getConn()
    cursor = conn.cursor()
    ma_60 = calculate_ma_from_db('stock_' + code, [60])['ma60']
    for i in range(1, 6):
        day = util.get_nth_workday(date, i)
        cursor.execute('select price from stock_' + code + ' where date=' + day + ';')
        price = 0
        for row in cursor:
            price = row[0]

        ma_price = ma_60[day]
        if ma_price < price:
            return True
    cursor.close()
    conn.close()
    return False
