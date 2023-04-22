import requests
from datetime import datetime
from datetime import date, timedelta
import os
import pandas as pd


token = '7e7d6e8a7d96eec07a09bb1f6070d8c8'
url = 'http://api.waizaowang.com/doc/getStockHSADailyMarket'

class DataSource(object):



    # url 格式 'http://api.waizaowang.com/doc/getStockHSADailyMarket?code=000001,000002&startDate=2023-02-21&endDate=2100-01-01&fields=all&export=0&token=7e7d6e8a7d96eec07a09bb1f6070d8c8'
    # 参数详见：http://waizaowang.com/api/detail/202


    def __init__(self):
        self.startDate = None
        self.endDate = None
        self.export=4
        self.fields = []
        self.codes = []

    def getShareList(self):
        url = "http://api.waizaowang.com/doc/getBaseInfo?type=1&code=all&fields=code&export=4&token=7e7d6e8a7d96eec07a09bb1f6070d8c8"
        ret = requests.get(url)
        return ret.text

    def getShareListLocal(self):
        file = open('share_list.csv', 'r', encoding='utf-8')
        ret = file.read()
        file.close()
        return ret

    def getAndSaveSharelist(self):
        # 获取 A股 列表
        url = "http://api.waizaowang.com/doc/getBaseInfo?type=1&code=all&fields=code&export=4&token=7e7d6e8a7d96eec07a09bb1f6070d8c8"
        ret = requests.get(url)
        file = open('share_list.csv', 'w', encoding='utf-8')
        file.write(ret.text)
        file.close()

    def getData(self):
        realUrl = url + '?' + 'code=' + ','.join(self.codes) + '&startDate=' + self.startDate + '&endDate=' + self.endDate + '&fields=' +','.join(self.fields) +'&export=' + str(self.export) + '&token=' + token
        print(realUrl)
        ret = requests.get(realUrl)
        print(ret.text)
        file = open('testfile.csv', 'w', encoding='utf-8')
        file.write(ret.text)
        file.close()

    def getDataByCode(self, code):
        realUrl = url + '?' + 'code=' + code + '&startDate=' + self.startDate + '&endDate=' + self.endDate + '&fields=' + ','.join(
            self.fields) + '&export=' + str(self.export) + '&token=' + token
        ret = requests.get(realUrl)
        return ret.text

    def setCodes(self, codes):
        self.codes.extend(codes)

    def setStartDate(self, startDate):
        self.startDate = startDate

    def setEndDate(self, endDate):
        self.endDate = endDate

    def setFields(self, fields):
        self.fields.extend(fields)

    def save(self, code, data):
        if not os.path.exists('myTest1/datas'):
            os.mkdir('myTest1/datas')

        file = open('datas/' + code + '.csv', 'w', encoding='utf-8')
        file.write(data)
        file.close()

def date_add(date_str, days_count=1):
    date_list = datetime.strptime(date_str, "%Y-%m-%d")
    y, m, d = date_list[:3]
    delta = datetime(days=days_count)
    date_result = datetime(y, m, d) + delta
    date_result = date_result.strftime("%Y-%m-%d")
    return date_result

if __name__ == '__main__':
    # dataSource = DataSource()
    # dataSource.setFields(['all'])
    # dataSource.setCodes(['000001','000002'])
    # dt01 = datetime.today()
    # dataSource.setEndDate(str(dt01.date()))
    # start_date = (date.today() + timedelta(days=-10)).strftime("%Y-%m-%d")  # 输出：2019-11-21
    # dataSource.setStartDate(str(start_date))
    # dataSource.getData()
    # file= pd.read_csv('testfile.csv')
    # print(file.head(5))

    dataSource = DataSource()
    ret = dataSource.getAndSaveSharelist()

