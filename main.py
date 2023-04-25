# 获取 前 20 天数据 并存储
import mysql.connector

from get_data import DataSource

'''
数据库结构

'''
if __name__ == '__main__':
    # 获取数据，并存入数据库
    dataSource = DataSource()
    # 获取股票列表
    shareList = dataSource.getShareListLocal().split('\n')
    dataSource.setFields(['all'])
    conn = mysql.connector.connect(user='root', password='Yy13693795561')

    cursor = conn.cursor()
    for code in shareList:
        dataSource.getDataByCode(code)


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

