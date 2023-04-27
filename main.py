# 获取 前 20 天数据 并存储
import celue1
import save_data
import util
import sql_connector
from get_data import DataSource
if __name__ == '__main__':

    # 先保存 60 日数据
    # save_data.save60DaysData()
    # 获取每天的数据
    # save_data.saveTodayData()
    # print('保存数据成功')
    # time.sleep(3)
    dataSource = DataSource()
    # 获取股票列表
    shareList = dataSource.getShareListLocal().split('\n')
    for code in shareList:
        beginDate = util.get_begin_date(code)
        endDate = util.get_end_date(code)
        dates_Between = util.dates_Between(beginDate, endDate)
        if dates_Between < 120:
            print('数据小于 120 天，不进行计算')
            continue

        startDate = util.get_bth_workday(beginDate, 60)
        finishDate = util.get_nth_workday(endDate, 60)
        sumNum = util.dates_Between(startDate, finishDate)
        hahah = []
        for i in range(0, sumNum):
            realDate = util.get_bth_workday(startDate, i)
            ret = celue1.get_celue_result(code, realDate)
            if ret:
                hahah.append(celue1.backtesting(ret, realDate))


