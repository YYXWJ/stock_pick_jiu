# 获取 前 20 天数据 并存储
import mysql.connector
from datetime import timedelta
from get_data import DataSource
from datetime import datetime
import pandas as pd
from io import StringIO
import re,time


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
    conn = mysql.connector.connect(user='root', password='bytedance', database='stocks', autocommit=True)
    cursor = conn.cursor()
    for code in shareList:
        cursor.execute('create table if not exists stock_' + code + ' (date varchar(32),price FLOAT, zdfd FLOAT, zded FLOAT,cjl FLOAT,zhfu FLOAT, hslv FLOAT, lbi FLOAT, zgj FLOAT, zdj FLOAT, zgb FLOAT, jzc FLOAT, jlr FLOAT, mlil FLOAT, jlil FLOAT, fzl FLOAT, unique(date))')
        datas = dataSource.getDataByCode(code)
        datas = list(datas.split('\n'))
        if '股票' in datas[1]:
            del datas[1]
        df = pd.read_csv(StringIO('\n'.join(datas)))
        for i in range(0,len(df)):
            times = time.strptime(df.tdate[i],'%Y-%m-%d')
            times = time.strftime('%Y%m%d',times)
            cursor.execute("insert into stock_" + code + '(date, price,zdfd,zded,cjl,zhfu,hslv,lbi,zgj,zdj,zgb,jzc,jlr,mlil,jlil,fzl) values (%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)' % (times, df.price[i], df.zdfd[i], df.zded[i],df.cjl[i],df.zhfu[i],df.hslv[i],df.lbi[i],df.zgj[i],df.zdj[i], df.zgb[i],df.jzc[i],df.jlr[i],df.mlil[i],df.jlil[i],df.fzl[i]))
    conn.close()
    cursor.close()
'''
    数据库结构

    需要的关键字段
    price   float   最新价（元）
    zdfd    float   涨跌幅度（%）
    zded    float   涨跌额度（元）
    cjl float   成交量（手）
    zhfu    float   振幅（%）
    hslv    float   换手率（%)
    lbi float   量比
    zgj float   最高价（元）
    zdj float   最低价（元）
    zgb float   总股本（股）
    jzc float   净资产
    jlr float   净利润
    mlil    float   毛利率
    jlil    float   净利率
    fzl float   负债率
    '''
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

