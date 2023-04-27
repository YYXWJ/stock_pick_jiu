# 获取 前 20 天数据 并存储
import celue1
import save_data
import util

if __name__ == '__main__':

    # 先保存 60 日数据
    # save_data.save60DaysData()
    # 获取每天的数据
    # save_data.saveTodayData()
    # print('保存数据成功')
    # time.sleep(3)
    ret = celue1.get_result(util.get_nth_workday('20230426', 60))
    for code in ret:
        print('code is: ' + code)
    if len(ret) == 0:
        print('没有找到符合策略的股票')
    else:
        celue1.backtesting(ret,util.get_nth_workday('20230426', 60), 60)