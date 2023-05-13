import mysql.connector

connector = None


def getConn():
    return mysql.connector.connect(user='root', password='Yy13693795561', database='stocks', autocommit=True)
