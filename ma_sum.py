import sql_connector
import pandas as pd
import pandas as pd
import datetime as dt
from datetime import datetime
def get_nth_workday(n):
    '''
     计算今天往前数第 n 个工作日
    '''
    today = dt.date.today()
    workdays = pd.offsets.BDay(n)
    result = (today - workdays).strftime('%Y%m%d')
    return result
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

def is_ma_60_up(code):
    conn = sql_connector.getConn()
    cursor = conn.cursor()
    cursor.execute('select price from stock_' + code+ ' where date=' +datetime.today().strftime("%Y%m%d") +';')
    today_price= 0
    sixty_price = 0
    for row in cursor:
        today_price = row[0]
    cursor.execute('select price from stock_' + code + ' where date=' + get_nth_workday(60) + ';')
    for row in cursor:
        sixty_price = row[0]
    return today_price > sixty_price

def is_price_low_then_ma_60(code):
    conn = sql_connector.getConn()
    cursor = conn.cursor()
    ma_60= calculate_ma_from_db('stock_' +code ,[60])['ma60'][-1]
    price = 0
    cursor.execute('select price from stock_' + code + ' where date=' + datetime.today().strftime("%Y%m%d") + ';')
    for row in cursor:
        price = row[0]

    return price < ma_60

if __name__ == '__main__':
    print(is_ma_60_up('000665'))