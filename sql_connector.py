import mysql.connector


def getConn():
    return mysql.connector.connect(user='root', password='bytedance', database='stocks', autocommit=True)
