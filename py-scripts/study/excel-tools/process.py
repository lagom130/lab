import xlrd
import os
import shutil

INPUT_DIR = 'E:\\DataOpenFiles\\'
OUTPUT_DIR = 'E:\\CF\\'



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
    file_list = get_file_list(INPUT_DIR)

    for filename in file_list:
        if os.path.getsize(INPUT_DIR+filename) == 0:
            print(filename + ': os.path.getsize='+str(os.path.getsize(INPUT_DIR+filename)))
            continue
        try:
            excel_file_open_test(INPUT_DIR, filename)
            shutil.copy(INPUT_DIR + filename, OUTPUT_DIR + filename)
        except :
            print(filename + '需要人工处理！！！！！！！！！！！！！！！！！！')
            # shutil.copy(INPUT_DIR+filename, OUTPUT_DIR+filename)

    print('end')
