import ma_sum
import mlil
from get_data import DataSource
def get_result():
    result = []
    dataSource = DataSource()
    shareList = dataSource.getShareListLocal().split('\n')
    # 60日均线是否向上
    for code in shareList:
        ret = ma_sum.is_ma_60_up(code)
        if not ret:
            continue
        code_mlil = mlil.get_mlil(code)
        if code_mlil < 40:
            continue
        if not ma_sum.is_price_low_then_ma_60_this_week(code):
            continue
        else:
            result.append(code)

    return result
