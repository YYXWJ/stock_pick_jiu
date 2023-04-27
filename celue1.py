import ma_sum
import util
from get_data import DataSource
from datetime import datetime
import math
'''
60日均线向上，股价本周下穿60日均线，毛利率40%以上
'''

def backtesting(list, date, during):
    for code in list:
        price = util.get_price(code, date)
        price_end = util.get_price(code, util.get_bth_workday(date, 60))
        rise = (price_end - price) / price
        print("开始日期 is %s, 结束日期 is %s, code: %s ;rise: %.2f" % (str(date),str(util.get_bth_workday(date, 60)), code, rise))



def get_result(date=datetime.today().strftime("%Y%m%d")):
    result = []
    data_source = DataSource()
    share_list = data_source.getShareListLocal().split('\n')
    # 60日均线是否向上
    for code in share_list:
        if len(code.strip()) == 0:
            continue
        ret = ma_sum.is_ma_60_up(code, date)
        if not ret:
            continue
        code_mlil = util.get_mlil(code, date)
        if code_mlil < 40:
            continue
        if not ma_sum.is_price_low_then_ma_60_this_week(code, date):
            continue
        else:
            result.append(code)
    return result
