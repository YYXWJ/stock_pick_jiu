import pandas as pd
import numpy as np
import show_data
from datetime import datetime
from get_data import DataSource
from datetime import timedelta
from io import StringIO


class AnalyzeShare(object):

    #选出股价不涨但是成交量涨的股票
    def selectStocksPriceNotRiseBytTradingVolumeIncrease(self, codes):
        pass

    def selectStockPriceNotRiseBytTradingVolumeIncrease(self, code, data):
        lines = data.split('\n')
        for line in lines:
            if len(line) == 0:
                lines.remove(line)
        labels = lines[0]
        datas = lines[2:]
        ll = []
        for d in datas:
            items = d.split(',')
            ll.append(items)
        datas = np.array(ll)
        # print(labels)
        # print(datas)
        show_data.showKGraph(data)

    def selectStockPriceNotRiseBytTradingVolumeIncreaseToday(self):
        dataSource = DataSource()
        shareList = dataSource.getShareList().split('\n')
        shareList = shareList[2:]
        dataSource.setFields(['all'])
        dt01 = datetime.today()
        while dt01.isoweekday() > 5:
            dt01 = dt01 + timedelta(days=-1)
        # dataSource.setEndDate(str(dt01.date()))
        dataSource.setEndDate(dt01.strftime("%Y-%m-%d"))
        # start_date = (date.today() + timedelta(days=-110)).strftime("%Y-%m-%d")  # 输出：2019-11-21
        dataSource.setStartDate(dt01.strftime("%Y-%m-%d"))

        for code in shareList:
            datas = dataSource.getDataByCode(code)
            datas = list(datas.split('\n'))
            if '股票' in datas[1]:
                del datas[1]
            df = pd.read_csv(StringIO('\n'.join(datas)))

            hslv = df['hslv']
            zdfd = abs(df['zdfd'])
            if hslv[0] > 10 and zdfd[0] < 2:
                print(code)

