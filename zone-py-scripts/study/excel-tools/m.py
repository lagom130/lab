import codecs
import json

import xlrd
import os
import shutil

import xlwt

INPUT_DIR = 'E:\\DataOpenFiles\\'
OUTPUT_DIR = 'E:\\DOFAnalysisResult\\'

keywords_str = '姓名,名字,姓氏, 出生年月日,出生日期,性别,民族,身份证号,手机号,国籍,婚姻状况,驾驶证编号,行驶证编号,微信账号,抖音账号,微博账号,邮箱,工作单位,证件生效日期,证件到期日期,家庭关系,照片,声音,指纹,指印,虹膜银行账号,支付宝账号,微信支付账号,登录密码,查询密码,支付密码,交易密码,收入,余额,消费支出,贷款额,不动产证号,不动产地址,纳税额,公积金缴存金额,个人社保缴存金额,医保存缴金额,家庭住址,通信地址,常驻地址,定位信息,工作单位地址,就诊医院,就医,疾病名称,病症,临床表现,症状,检查报告,检验报告,诊断结果,住院志,医嘱单,手术记录,麻醉记录,护理记录,用药记录,服药记录,药物食物,过敏信息,家族病史,以往病史,现病史,传染病史,吸烟史,饮酒史,宗教名称     '

row0 = ["部门", "文件ID", "文件名", "文件类型", "文件状态", "文件下载地址", "创建时间"]
JSON_DIR = 'E:\\DOFAnalysisResult\\'

# 设置表格样式
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

# 写Excel
def write_excel(book, sheet_name, json_file_name):
    sheet1 = book.add_sheet(sheet_name, cell_overwrite_ok=True)
    row0 = ["部门", "文件ID", "文件名", "文件类型", "文件状态", "文件下载地址", "创建时间"]
    # 写第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

    json_array = []
    with open(JSON_DIR+json_file_name, 'r', encoding='utf-8') as f:
        json_array = json.load(f)
    for i in range(0, len(json_array)):
        file_info = json_array[i]
        sheet1.write(i+1, 0, file_info['dept'])
        sheet1.write(i+1, 1, file_info['id'])
        sheet1.write(i+1, 2, file_info['fileName'])
        sheet1.write(i+1, 3, file_info['fileType'])
        sheet1.write(i+1, 4, file_info['fileStatus'])
        sheet1.write(i+1, 5, file_info['fileDownloadAddress'])
        sheet1.write(i+1, 6, file_info['createDate'])
    return book

def typeList():
    return {
        "3c68313ee689abe68f8f": 'html',
        "504b03040a0000000000": 'xlsx',
        '504b0304140008080800': 'docx',
        "d0cf11e0a1b11ae10000": 'doc',
        '2d2d204d7953514c2064': 'sql',
        'ffd8ffe000104a464946': 'jpg',
        '89504e470d0a1a0a0000': 'png',
        '47494638396126026f01': 'gif',
        '3c21444f435459504520': 'html',
        '3c21646f637479706520': 'htm',
        '48544d4c207b0d0a0942': 'css',
        '2f2a21206a5175657279': 'js',
        '255044462d312e350d0a': 'pdf',
    }


# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


# 获取文件类型
def filetype(filename):
    binfile = open(filename, 'rb')  # 必需二制字读取
    bins = binfile.read(20)  # 提取20个字符
    binfile.close()  # 关闭文件流
    bins = bytes2hex(bins)  # 转码
    bins = bins.lower()  # 小写
    # print(bins)
    tl = typeList()  # 文件类型
    ftype = 'unknown'
    for hcode in tl.keys():
        lens = len(hcode)  # 需要的长度
        if bins[0:lens] == hcode:
            ftype = tl[hcode]
            break
    if ftype == 'unknown':  # 全码未找到，优化处理，码表取5位验证
        bins = bins[0:5]
    for hcode in tl.keys():
        if len(hcode) > 5 and bins == hcode[0:5]:
            ftype = tl[hcode]
            break
    return ftype


def get_file_list(dir_path):
    return os.listdir(dir_path)


def get_keywords():
    return keywords_str.split(',')


def excel_file_has_keyword(dir, filename, keywords):
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
                for keyword in keywords:
                    if str(content).find(keyword) >= 0:
                        print(filename + ' has keyword ' + keyword)
                        return True
    print(filename + ' not find keyword')
    return False


def write_result(arr, result_name):
    if os.path.exists(OUTPUT_DIR + result_name):
        os.remove(OUTPUT_DIR + result_name)
    with codecs.open(OUTPUT_DIR + result_name, 'wb', encoding='utf-8') as fp:
        fp.write(u'{arr}\n'.format(arr='\n'.join(arr)))


def loadJson():
    with open('resources_meta.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_dept_dict():
    with open('org_department.json', 'r', encoding='utf-8') as f:
        dept_arr = json.load(f)
        dept_dict = {}
        for d in dept_arr:
            dept_dict[d['dept_id']] = d['dept_name']
    return dept_dict


def match(arr, dept_dict, resource_metas):
    file_info_arr = []
    for resource_meta in resource_metas:
        if 'technicalInfo' not in resource_meta:
            continue
        if 'fileList' not in resource_meta['technicalInfo']:
            continue
        dept = 'unknown'
        if 'basicInfo' in resource_meta and 'deptId' in resource_meta['basicInfo']:
            dept = dept_dict.get(resource_meta['basicInfo']['deptId'], 'unknown')
        rm_files = resource_meta['technicalInfo']['fileList']
        for rm_file in rm_files:
            if rm_file['id'] in arr:
                rm_file['dept'] = dept
                file_info_arr.append(rm_file)
    return file_info_arr


def dump_file_info(arr, dept_dict, resource_metas, json_file_name, files_dir):
    file_info_list = match(arr, dept_dict, resource_metas)
    for file_info in file_info_list:
        save_path = OUTPUT_DIR+files_dir
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        shutil.copy(INPUT_DIR+file_info['id'], save_path + '\\' + file_info['id'] + '.' + file_info['fileType'])
    with open(OUTPUT_DIR + json_file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(file_info_list, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    dept_dict = get_dept_dict()
    resource_metas = loadJson()
    keywords = get_keywords()
    file_list = get_file_list(INPUT_DIR)
    zero_size_list = []
    has_keywords_list = []
    cannot_analysis_dict = {}
    for filename in file_list:
        if os.path.getsize(INPUT_DIR + filename) == 0:
            zero_size_list.append(filename)
            print(filename + " is empty, now zero_size_list size is " + str(len(zero_size_list)))
            continue
        try:
            if excel_file_has_keyword(INPUT_DIR, filename, keywords):
                has_keywords_list.append(filename)
                print(filename + " has keyword, now has_keywords_list size is " + str(len(has_keywords_list)))
        except:
            type = filetype(INPUT_DIR + filename)
            if type not in cannot_analysis_dict:
                cannot_analysis_dict[type] = [filename]
            else:
                cannot_analysis_dict[type].append(filename)
            print(filename + " cannot analysis, now cannot analysis " + type + " size is " + str(len(cannot_analysis_dict[type])))
    print('analysis complete')
    if len(zero_size_list) > 0:
        print('zero_size_list write result')
        write_result(zero_size_list, 'empty_files.txt')
        dump_file_info(zero_size_list, dept_dict, resource_metas, "empty_files.json", 'empty')
    if len(has_keywords_list) > 0:
        print('has_keywords_list write result')
        write_result(has_keywords_list, 'hasKeyword.txt')
        dump_file_info(has_keywords_list, dept_dict, resource_metas, "has_keywords_files.json", 'hasKeyword')
    for type in cannot_analysis_dict.keys():
        if len(cannot_analysis_dict[type]) > 0:
            print('cannotAnalysis-' + type + '_list write result')
            write_result(cannot_analysis_dict[type], 'cannotAnalysis-' + type + '.txt')
            dump_file_info(cannot_analysis_dict[type], dept_dict, resource_metas, "cannot_analysis_"+type+".json", 'cannotAnalysis('+type+')')

    book = xlwt.Workbook()
    book = write_excel(book, '包含关键词', 'has_keywords_files.json')
    book = write_excel(book, '无法分析XLSX文件', 'cannot_analysis_xlsx.json')
    book = write_excel(book, '无法分析DOC文件', 'cannot_analysis_doc.json')
    book = write_excel(book, '无法分析PDF文件', 'cannot_analysis_pdf.json')
    book = write_excel(book, '无法分析JPG文件', 'cannot_analysis_jpg.json')
    book = write_excel(book, '无法分析其他文件', 'cannot_analysis_unknown.json')
    book = write_excel(book, '空文件', 'empty_files.json')
    book.save(JSON_DIR + '分析结果.xls')

    print('end')
