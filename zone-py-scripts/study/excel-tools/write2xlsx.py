import xlwt
import json

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


if __name__ == '__main__':
    book = xlwt.Workbook()
    book = write_excel(book, '包含关键词', 'has_keywords_files.json')
    book = write_excel(book, '无法分析XLSX文件', 'cannot_analysis_xlsx.json')
    book = write_excel(book, '无法分析DOC文件', 'cannot_analysis_doc.json')
    book = write_excel(book, '无法分析PDF文件', 'cannot_analysis_pdf.json')
    book = write_excel(book, '无法分析JPG文件', 'cannot_analysis_jpg.json')
    book = write_excel(book, '无法分析其他文件', 'cannot_analysis_unknown.json')
    book = write_excel(book, '空文件', 'empty_files.json')
    book.save(JSON_DIR+'分析结果.xls')
