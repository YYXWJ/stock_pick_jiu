# 获取 前 20 天数据 并存储
import mysql.connector
from datetime import timedelta
from get_data import DataSource
from datetime import datetime
import pandas as pd
from io import StringIO
'''
数据库结构

'''


def save60DaysData():
    # 获取数据，并存入数据库
    dataSource = DataSource()
    # 获取股票列表
    shareList = dataSource.getShareListLocal().split('\n')
    dataSource.setFields(['all'])
    dt01 = datetime.today()
    while dt01.isoweekday() > 5:
        dt01 = dt01 + timedelta(days=-1)
    # dataSource.setEndDate(str(dt01.date()))
    dataSource.setEndDate(dt01.strftime("%Y-%m-%d"))
    start_date = (datetime.today() + timedelta(days=-110)).strftime("%Y-%m-%d")  # 输出：2019-11-21
    dataSource.setStartDate(start_date)
    conn = mysql.connector.connect(user='root', password='bytedance')
    cursor = conn.cursor()
    i = 0
    for code in shareList:
        if i >= 3:
            break
        i = i + 1
        datas = dataSource.getDataByCode(code)
        datas = list(datas.split('\n'))
        datas = datas[2:]
        for item in datas:
            item = item.strip()
            if len(item) == 0:
                continue
            print("item: " + item)
            df = pd.read_csv(StringIO(item))
            print(df)


if __name__ == '__main__':
    save60DaysData()
    

    # analyzeShare = AnalyzeShare()
    # analyzeShare
    # analyzeShare.selectStockPriceNotRiseBytTradingVolumeIncreaseToday()


    # dataSource = DataSource()
    # analyzeShare = AnalyzeShare()
    # shareList = dataSource.getShareList().split('\n')
    # shareList = shareList[2:]
    # dataSource.setFields(['all'])
    # dt01 = datetime.today()
    # dataSource.setEndDate(str(dt01.date()))
    # start_date = (date.today() + timedelta(days=-110)).strftime("%Y-%m-%d")  # 输出：2019-11-21
    # dataSource.setStartDate(str(start_date))
    # i = 0
    # for code in shareList:
    #     i=i+1
    #     if i < 2:
    #         data = dataSource.getDataByCode('300579')
    #         dataSource.save(code, data)
    #         analyzeShare.selectStockPriceNotRiseBytTradingVolumeIncrease(code, data)
