import csv
import json
import os


def no_title_csv_analysis(title, path):
    data_list = []

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            data = {}
            for index, i in enumerate(row):
                if index < len(title):
                    data[title[index]] = i
                else:
                    data[index] = i

            data_list.append(data)

    return data_list


def csv_analysis(path):
    title = []
    data_list = []

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            if row_index is 0:
                title = row

            else:
                data = {}
                for index, i in enumerate(row):
                    data[title[index]] = i
                data_list.append(data)
    return data_list


def sub_step(status):
    if status == 'unSend' :
        return 1
    elif status == 'finished':
        return 1
    else:
        return 0

def write_csv(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())


def write_txt(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        for item in data_list:
            cf.writelines(item)

def get_id_and_name(data_list, code, parent_id):
    if parent_id is None:
        for item in data_list:
            if item['mapCatalogCode'] == code:
                return item['_id'], item['mapCatalogName']
    else:
        for item in data_list:
            if item['mapCatalogCode'] == code and item['mapCatalogParentId'] == parent_id:
                return item['_id'], item['mapCatalogName']
    return '', ''

def share_res_cataloginfo_relation_update_sql(srcr_dict):
    return "update share_res_cataloginfo_relation set region_id='{region_id}',region_code='{region_code}',region_name='{region_name}',category_id='{category_id}',category_code='{category_code}',category_name='{category_name}',term_id='{term_id}',term_code='{term_code}',term_name='{term_name}',catalogue_id='{catalogue_id}',catalogue_code='{catalogue_code}',catalogue_name='{catalogue_name}' where id='{id}';".format(srcr_dict)

if __name__ == '__main__':
    update_sql = []
    map_catalog_list = csv_analysis("E:\\io816\\map_catalog_simple.csv")
    province_c_list = []
    region_c_list = []
    category_c_list = []
    term_c_list = []
    catalogue_c_list = []
    for mc in map_catalog_list:
        if mc['mapCatalogType'] == 'province':
            province_c_list.append(mc)
        elif mc['mapCatalogType'] == 'region':
            region_c_list.append(mc)
        elif mc['mapCatalogType'] == 'category':
            category_c_list.append(mc)
        elif mc['mapCatalogType'] == 'term':
            term_c_list.append(mc)
        elif mc['mapCatalogType'] == 'catalogue':
            catalogue_c_list.append(mc)

    ir_list = no_title_csv_analysis(['id', 'info_resource_name', 'dept_info_resource_code'],
                                                    "E:\\io816\\irdeptcode816.csv")
    sr_list = no_title_csv_analysis(['id', 'resource_id', 'resource_name', 'resource_type', '', '','', '', '','','','info_resource_id'],
                                    "E:\\io816\\sdr816.csv")
    # srcr_list = no_title_csv_analysis(['id', 'info_resource_name', 'dept_info_resource_code'],
    #                                 "E:\\io816\\info_resource_816_dept_code.csv")

    for ir in ir_list:
        dept_code = ir['dept_info_resource_code']
        province_code = dept_code[0:6]
        province_id, province_name = get_id_and_name(province_c_list, province_code, None)
        region_code = dept_code[6:10]
        region_id, region_name = get_id_and_name(region_c_list, region_code, province_id)
        category_code = dept_code[10:11]
        category_id, category_name = get_id_and_name(category_c_list, category_code, region_id)
        term_code = dept_code[11:13]
        term_id, term_name = get_id_and_name(term_c_list, term_code, category_id)
        catalogue_code = dept_code[13:16]
        catalogue_id, catalogue_name = get_id_and_name(catalogue_c_list, catalogue_code, term_id)
        for sr in sr_list:
            if sr['info_resource_id'] == ir['id']:
                sql = "update share_res_cataloginfo_relation set "
                sql = sql + "region_id='"+region_id+"',"
                sql = sql + "region_code='"+region_code+"',"
                sql = sql + "region_name='"+region_name+"',"
                sql = sql + "category_id='"+category_id+"',"
                sql = sql + "category_code='"+category_code+"',"
                sql = sql + "category_name='"+category_name+"',"
                sql = sql + "term_id='"+term_id+"',"
                sql = sql + "term_code='"+term_code+"',"
                sql = sql + "term_name='"+term_name+"',"
                sql = sql + "catalogue_id='"+catalogue_id+"',"
                sql = sql + "catalogue_code='"+catalogue_code+"',"
                sql = sql + "catalogue_name='"+catalogue_name+"',"
                sql = sql + "detail_id is null,"
                sql = sql + "detail_name is null,"
                sql = sql + "detail_code is null,"
                sql = sql + " where id='"+sr['id']+"';"
                update_sql.append(sql)



    write_txt(update_sql, "E:\\io816\\srupdate.txt")
    print('over')

