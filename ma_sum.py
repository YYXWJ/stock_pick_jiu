
import mysql.connector
import pandas as pd

def calculate_ma_from_db(table, ma_cycle):
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
    conn = mysql.connector.connect(user='root', password='bytedance', database='stocks', autocommit=True)
    # 从数据库中读取股票数据
    sql = "SELECT date, price FROM {}".format(table)
    data = pd.read_sql(sql, conn)

    # 计算均线
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data['ma{}'.format(ma_cycle)] = data['price'].rolling(window=ma_cycle).mean()
    print(data)
    return data