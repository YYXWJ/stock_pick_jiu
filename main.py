# 获取 前 20 天数据 并存储
import celue1
import save_data
import util
import sql_connector
from get_data import DataSource
from tqdm import tqdm
if __name__ == '__main__':

    # 先保存 60 日数据
    # save_data.save60DaysData()
    # 获取每天的数据
    # save_data.saveTodayData()
    # print('保存数据成功')
    # time.sleep(3)
    celue1.start()