import xlrd
import os

INPUT_DIR = 'E:\\DataOpenFiles\\'
OUTPUT_DIR = 'E:\\rggy\\'

keywords = ['fuck']


def get_file_list(dir_path):
    return os.listdir(dir_path)


def excel_file_open_test(dir, filename):
    full_filename = dir + filename
    # 打开文件
    xl_file = xlrd.open_workbook(filename=full_filename)

    # 获取sheet的个数，一个整数
    nsheets = xl_file.nsheets
    for i in range(nsheets):
        sheet = xl_file.sheet_by_index(i)
        # 获取sheet中行数
        nrows = sheet.nrows
        for j in range(nrows):
            row_contents = sheet.row_values(rowx=j, start_colx=0, end_colx=None)
    return False


if __name__ == '__main__':
    # 打开文件
    xl_file = xlrd.open_workbook(filename='E:\\821499989353103531.xls')

    # 获取sheet的个数，一个整数
    nsheets = xl_file.nsheets
    for i in range(nsheets):
        sheet = xl_file.sheet_by_index(i)
        # 获取sheet中行数
        nrows = sheet.nrows
        for j in range(nrows):
            row_contents = sheet.row_values(rowx=j, start_colx=0, end_colx=None)
            for content in row_contents:
                print(content)


