# 获取 前 20 天数据 并存储
import mysql.connector
from datetime import timedelta
from get_data import DataSource
from datetime import datetime
import pandas as pd
from io import StringIO
import re,time
import save_data
import ma_sum
import celue1
if __name__ == '__main__':

    # 先保存 60 日数据
    # save_data.save60DaysData()
    # 获取每天的数据
    # save_data.saveTodayData()
    # print('保存数据成功')
    # time.sleep(3)
    ret = celue1.get_result()
    for code in ret:
        print('code is: ' + code)
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

