# 获取 前 20 天数据 并存储
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
