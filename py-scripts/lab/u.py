# coding=utf8
import datetime

import repository

if __name__ == '__main__':
    start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('upsert start time: ' + start)
    print('--------------------------------------------------')
    print()
    repository.upsert_all()
    end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('--------------------------------------------------')
    print('upsert end time:' + end)
    print('{}~{}'.format(start, end))

