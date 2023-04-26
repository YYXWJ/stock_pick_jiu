import sql_connector
import pandas as pd
from datetime import datetime
import log
def get_mlil(code):
    conn = sql_connector.getConn()
    # 从数据库中读取股票数据
    cursor = conn.cursor()
    cursor.execute('select mlil from stock_' + code + ' where date=' + datetime.today().strftime("%Y%m%d") + ';')
    mlil = 0
    for row in cursor:
        mlil = row[0]
    log.info('mlil is ' +str(mlil))
    return mlil