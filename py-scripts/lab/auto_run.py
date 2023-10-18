# coding=utf8

import leek_analysis
import repository

if __name__ == '__main__':
    leek_analysis.SPIDER_SLEEP = 0
    leek_analysis.NEED_ANALYSIS = True
    leek_analysis.COLOR_FLAG = False
    repository.upsert_all()
    leek_analysis.main()
