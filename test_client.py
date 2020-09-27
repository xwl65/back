import  pytest
import pymysql
db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='jeesite',
    charset='utf8mb4',

)

def test_conn():
    #创建游标
    with db.cursor() as cursor:
        sql = "show tables;"
        cursor.execute(sql)
        print(sql)
        print(cursor.fetchall())
        print(type(cursor.fetchall()))


