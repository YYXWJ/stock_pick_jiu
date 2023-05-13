import logging

import ma_sum
import celue1
import util
from get_data import DataSource
from tqdm import tqdm
from datetime import datetime, timedelta
import sql_connector
import time
import ma_sum
import concurrent.futures

'''
60日均线向上，股价本周下穿60日均线，毛利率40%以上
'''


def backtesting(code, data_dict, startDate):
    # 计算 60 天内最高涨幅
    init_date = datetime.strptime(startDate, "%Y%m%d")
    price = data_dict[startDate].price
    max = -10000
    for i in range(60):
        end_date = init_date + timedelta(days=i)
        end_date = end_date.strftime("%Y%m%d")
        price_end = 0
        if data_dict.__contains__(end_date):
            price_end = data_dict[end_date].price
        else:
            continue
        rise = (price_end - price) / price
        if rise > max:
            max = rise

    if max > -10000:
        return "股票 %s ,从 %s 开始往后 60 天, 最高涨幅为 %s" % (str(code), str(startDate), str('%.2f' % max))
    else:
        return None

def get_real_result():
    import os
    import glob

    folder_path = "output"  # 修改为实际的文件夹路径

    # 获取文件夹中所有的 txt 文件
    file_list = glob.glob(os.path.join(folder_path, "*.txt"))

    print("文件个数： " + str(len(file_list)))
    # 定义分组的边界
    boundaries = [0, 0.1, 0.2, 0.3]

    # 定义分组的名称
    groups = ["<0", "0", "0-0.1", "0.1-0.2", "0.2-0.3", ">0.3"]

    # 初始化字典，用于存储各个分组的数据
    data = {group: [] for group in groups}
    lines = []
    data_count = 0
    # 遍历所有文件并处理每个文件中的行
    for file_path in file_list:
        with open(file_path, "r", encoding="gbk") as f:
            for line in f:
                data_count +=1
                # 判断行是否符合要求
                if len(line.split(",")) == 3:
                    # 提取最高涨幅
                    value = float(line.split(" ")[-1].strip())
                    group = None
                    if value < 0:
                        group = "<0"
                    elif value == 0:
                        group = "0"
                    elif value >= 0 and value < 0.1:
                        group = "0-0.1"
                    elif value >= 0.1 and value < 0.2:
                        group = "0.1-0.2"
                    elif value >= 0.2 and value < 0.3:
                        group = "0.2-0.3"
                    elif value >= 0.3:
                        group = ">0.3"
                        lines.append(line)
                    # 将数据添加到对应的分组中
                    if group:
                        data[group].append(value)
    print("数据条数：" + str(data_count))
    for group in groups:
        values = data[group]
        print(f"{group}: {len(values)}")

    for line in lines:
        print(line)
def get_celue_result(data_dict, date, ma_60):
    code_mlil = util.get_mlil(data_dict, date)
    if code_mlil < 40:
        return False
    ret = ma_sum.is_ma_60_up(data_dict, date)
    if not ret:
        return False

    if not ma_sum.is_price_low_then_ma_60(data_dict, ma_60, date):
        return False

    if not ma_sum.is_price_high_then_ma_60_ten_day(data_dict, ma_60, date):
        return False
    return True


def start():
    dataSource = DataSource()
    # 获取股票列表
    shareList = dataSource.getShareListLocal().split('\n')[::-1]
    # shareList = ['688018']
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        for code in shareList:
            executor.submit(handle_one_row, code)


def handle_one_row(code):
    beginDate = util.get_begin_date(code)
    endDate = util.get_end_date(code)
    dates_Between = util.dates_Between(beginDate, endDate)
    if dates_Between < 120:
        print(code + '的数据小于 120 天，不进行计算')
        return
    hahah = []
    startDate = util.get_bth_workday(beginDate, 60)
    finishDate = util.get_nth_workday(endDate, 60)
    # 读出 所有 数据
    data_dict = getShareDataByCode(code)
    # 获取 60日均线数据
    ma_60 = ma_sum.calculate_ma_from_db('stock_' + code, [60])['ma60']
    sumNum = util.dates_Between(startDate, finishDate)
    try:
        i = 0
        while i < sumNum:
            realDate = util.get_bth_workday(startDate, i)
            ret = celue1.get_celue_result(data_dict, realDate, ma_60)
            if ret:
                i = i + 60
                result = None
                try:
                    result = celue1.backtesting(code, data_dict, realDate)
                except Exception as e:
                    print(e)
                if result is not None:
                    hahah.append(result)
            # 根据某个条件增加i的值
                i += 60
            else:
                i += 1

        if len(hahah) > 0:
            with open('./output/output_' + code + '.txt', 'a') as f:
                # Write each element of the list to the file
                for item in hahah:
                    f.write(item + '\n')
    except Exception as e:
        logging.exception(e)
    print('finish: ' + code)


def getShareDataByCode(code):
    conn = sql_connector.getConn()
    cursor = conn.cursor()
    cursor.execute('select date,price,mlil from stock_' + code + ' order by date ASC;')
    data_dict = {row[0]: Unit(row[1], row[2]) for row in cursor.fetchall()}
    return data_dict


class Unit:
    def __init__(self, price, mlil):
        self.price = price
        self.mlil = mlil

if __name__ == '__main__':
    get_real_result()