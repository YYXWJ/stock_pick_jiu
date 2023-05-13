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
    sql = "SELECT date, price FROM {} order by date asc".format(table)
    data = pd.read_sql(sql, conn)

    # 计算均线
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    for i in maList:
        data['ma{}'.format(i)] = data['price'].rolling(window=i).mean()
    return data


def is_ma_60_up(data_dict, date):
    try:
        today_price = data_dict[date].price
        sixty_price = data_dict[util.get_nth_workday(date, 60)].price
        return today_price > sixty_price
    except Exception as e:
        return False


def is_price_low_then_ma_60(data_dict, ma_60, date):
    price = 0
    try:
        price = data_dict[date].price
    except Exception:
        return False
    return price < ma_60[date]


def is_price_low_then_ma_60_this_week(data_dict, ma_60, date):
    try:
        # 今天一定要下穿60线
        if not is_price_low_then_ma_60(data_dict, ma_60, date):
            return False
        ret = False
        for i in range(1, 6):
            day = util.get_nth_workday(date, i)
            price = 0
            try:
                price = data_dict[day].price
            except Exception:
                price = 0
            if ma_60.__contains__(key=day):
                ma_price = ma_60[day]
                if ma_price < price:
                    ret = True
                    break
            else:
                ret = False
    except Exception:
        print('is_price_low_then_ma_60_this_week 异常')
    return ret


def is_price_high_then_ma_60_ten_day(data_dict, ma_60, date):
    try:
        ret = False
        for i in range(1, 10):
            day = util.get_nth_workday(date, i)
            price = 0
            try:
                price = data_dict[day].price
            except Exception:
                price = 0
            if ma_60.__contains__(key=day):
                ma_price = ma_60[day]
                if ma_price < price:
                    ret = True
                    break
            else:
                ret = False
    except Exception:
        print('is_price_low_then_ma_60_this_week 异常')
    return ret
