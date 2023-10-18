import xlrd
import os

INPUT_DIR = 'E:\\CF\\'
OUTPUT_DIR = 'E:\\'

keywords = ['fuck']
keywords_str = '姓名,名字,姓氏, 出生年月日,出生日期,性别,民族,身份证号,手机号,国籍,婚姻状况,驾驶证编号,行驶证编号,微信账号,抖音账号,微博账号,邮箱,工作单位,证件生效日期,证件到期日期,家庭关系,照片,声音,指纹,指印,虹膜银行账号,支付宝账号,微信支付账号,登录密码,查询密码,支付密码,交易密码,收入,余额,消费支出,贷款额,不动产证号,不动产地址,纳税额,公积金缴存金额,个人社保缴存金额,医保存缴金额,家庭住址,通信地址,常驻地址,定位信息,工作单位地址,就诊医院,就医,疾病名称,病症,临床表现,症状,检查报告,检验报告,诊断结果,住院志,医嘱单,手术记录,麻醉记录,护理记录,用药记录,服药记录,药物食物,过敏信息,家族病史,以往病史,现病史,传染病史,吸烟史,饮酒史,宗教名称     '


def get_file_list(dir_path):
    return os.listdir(dir_path)


def excel_file_has_keyword(dir, filename):
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
            for content in row_contents:
                for keyword in keywords_str.split(','):
                    if str(content).find(keyword) >= 0:
                        return True
    return False


if __name__ == '__main__':
    file_list = get_file_list(INPUT_DIR)

    for filename in file_list:
        if os.path.getsize(INPUT_DIR+filename) == 0:
            continue
        try:
            if excel_file_has_keyword(INPUT_DIR, filename):
                print(filename)
        except :
            print(filename+"无法读取")

    print('end')
