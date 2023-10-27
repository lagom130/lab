import csv
import json


def analysis(path, key):
    dict_arr = []
    tc = 0
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] is not None and row[0] != '':
                dict_arr.append({
                    key: row[0],
                    "totalCount": int(row[1]),
                    "data": []
                })
            tc = tc + int(row[1])


def suc_analysis(path):
    provider_arr = []
    applicant_arr = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            provider_dept_name = row[0]
            applicant_dept_name = row[1]
            count = int(row[2])
            suc_analysis_item(provider_arr, 'providerDeptName', provider_dept_name, 'applicantDeptName',
                              applicant_dept_name, count)
            for item in provider_arr:
                item['data'].sort(key=lambda x: x['count'], reverse=True)
            suc_analysis_item(applicant_arr, 'applicantDeptName', applicant_dept_name, 'providerDeptName',
                              provider_dept_name, count)
            for item in applicant_arr:
                item['data'].sort(key=lambda x: x['count'], reverse=True)
        print(provider_arr)
        print(applicant_arr)
        for p in applicant_arr:
            print('\"' + p['applicantDeptName'] +' \",')
        for p in applicant_arr:
            print('\"'+ str(p['totalCount'])+'\",')


def suc_analysis_item(arr, item_key, item_value, child_key, child_name, count):
    change_item = None
    for item in arr:
        if item[item_key] == item_value:
            change_item = item
            break
    if change_item is None:
        change_item = {
            item_key: item_value,
            'totalCount': 0,
            'data': []
        }
        arr.append(change_item)
    change_item['data'].append({
        child_key: child_name,
        "count": count
    })
    if change_item is not None and len(change_item['data']) > 0 :
        change_item['totalCount'] = change_item['totalCount'] + count
    arr.sort(key= lambda x:x['totalCount'], reverse=True)


if __name__ == '__main__':
    suc_analysis("E:\\suc.csv")
