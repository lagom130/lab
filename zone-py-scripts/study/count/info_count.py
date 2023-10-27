import datetime
import time

import pymongo
import pymysql


def test():
    # mysql_conn = pymysql.connect(host='2.46.2.102', port=3306, user='bigdata', password='123@abcd')
    mysql_conn = pymysql.connect(host='mysql-master', port=3306, user='bigdata', password='123@abcd')
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute('SELECT count(*) from cmp_catalog.info_resource_platform')
    result = mysql_cursor.fetchall()
    for x in result:
        for y in x:
            print(y)
    print(result)


if __name__ == '__main__':
    try:
        print(1)
        # mysql_conn = pymysql.connect(host='2.46.2.102', port=3306, user='bigdata', password='123@abcd')
        # mysql_conn = pymysql.connect(host='mysql-master', port=3306, user='bigdata', password='123@abcd')
        # mysql_cursor = mysql_conn.cursor()
        # mysql_cursor.execute('SELECT count(*) from cmp_catalog.info_resource_platform')
        # result = mysql_cursor.fetchall()
        # for x in result:
        #     for y in x:
        #         print(y)
        # print(result)
    except Exception as e:
        print('except:', e)
    finally:
        while True:
            print('query is completed, please close the window!')
            time.sleep(60)



