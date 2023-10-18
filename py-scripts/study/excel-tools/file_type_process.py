import os


# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少半2字符，长则8字符
import shutil


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
    print(bins)
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


# 文件扫描，如果是目录，就将遍历文件，是文件就判断文件类型
def filescanner(path):
    if type(path) != type('a'):  # 判断是否为字符串
        print('抱歉，你输入的不是一个字符串路径！')
    elif path.strip() == '':  # 将两头的空格移除
        print('输入的路径为空！')
    elif not os.path.exists(path):
        print('输入的路径不存在！')
    elif os.path.isfile(path):
        if path.rfind('.') > 0:
            print('文件名:', os.path.split(path)[1])
        else:
            print('文件名中没有找到格式')
        path = filetype(path)
        print('解析文件判断格式：' + path)
    elif os.path.isdir(path):
        print('输入的路径指向的是目录，开始遍历文件')
        for p, d, fs in os.walk(path):
            print(os.path.split(p))
            for n in fs:
                n = n.split('.')
                print('\t' + n[0] + '\t' + n[1])


if __name__ == '__main__':
    file_list = os.listdir('E:\\RGP\\')
    for fn in file_list:
        print(fn)
        path = filetype('E:\\RGP\\'+fn)
        new_file_name = fn + '.' + path
        print(new_file_name)
        if path == 'unknown':

            shutil.copy('E:\\RGP\\'+fn, 'E:\\FTUN\\'+fn+'.txt')
        else:
            shutil.copy('E:\\RGP\\' + fn, 'E:\\FT\\' + new_file_name)
        # filescanner('E:\\RGP\\'+fn)
    print('end')