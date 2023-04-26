import ma_sum
import mlil
from get_data import DataSource
from datetime import datetime

'''
60日均线向上，股价本周下穿60日均线，毛利率40%以上
'''


def get_result(date=datetime.today().strftime("%Y%m%d")):
    result = []
    data_source = DataSource()
    share_list = data_source.getShareListLocal().split('\n')
    # 60日均线是否向上
    for code in share_list:
        ret = ma_sum.is_ma_60_up(code, date)
        if not ret:
            continue
        code_mlil = mlil.get_mlil(code, date)
        if code_mlil < 40:
            continue
        if not ma_sum.is_price_low_then_ma_60_this_week(code, date):
            continue
        else:
            result.append(code)

    return result
