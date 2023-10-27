import csv
import json
import os
import csv

# 提供部门-每个接口-申请部门 调用次数统计
# db.getCollection('screen_statistics').aggregate([
#     {
#         $match: {"sourceType" : "API","statisticsType" : "source"}
#     },
#     {$unwind :"$statisticsInfoDTOList"},
#     {$unwind :"$statisticsInfoDTOList.departUseSourceDTOList"},
#     {
#         $group:
#          {
#            _id: {"proDeptName":"$statisticsInfoDTOList.departName","apiName":"$statisticsInfoDTOList.sourceName","conDeptName":"$statisticsInfoDTOList.departUseSourceDTOList.departName"},
#            count: {$sum: "$statisticsInfoDTOList.departUseSourceDTOList.count"}
#          }
#     },
#     {
#         $project: {'proDeptName_apiName_conDeptName': '$_id', count: {$toInt: '$count'}, '_id': 0}
#     },
# 	{
#         $sort: {proDeptName_apiName_conDeptName: -1,count: -1}
# 	}
# ])


def psuct_analysis(path):
    provider_arr = []
    applicant_arr = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            provider_dept_name = row[0]
            source_name = row[1]
            applicant_dept_name = row[2]
            count = int(row[3])
            if provider_dept_name == '共享服务平台' or applicant_dept_name == '共享服务平台':
                continue
            psuct_analysis_item(provider_arr, 'providerDeptName', provider_dept_name, 'sourceName', source_name,
                                'applicantDeptName',
                                applicant_dept_name, count)

            psuct_analysis_item(applicant_arr, 'applicantDeptName', applicant_dept_name, 'sourceName', source_name,
                                'providerDeptName',
                                provider_dept_name, count)

        root = os.getcwd()
        write(root + '/{}.json'.format('provider'), provider_arr)
        provider_arr_top = cut(provider_arr, 5)
        write(root + '/{}_top.json'.format('provider'), provider_arr_top)
        write(root + '/{}.json'.format('applicant'), applicant_arr)
        applicant_arr_top = cut(applicant_arr, 5)
        write(root + '/{}_top.json'.format('applicant'), applicant_arr_top)


def cut(arr, num):
    for f in arr:
        s_arr = f['data']
        for s in s_arr:
            t_arr = s['data']
            s['data'] = t_arr[:num]
        f['data'] = s_arr[:num]
    arr = arr[:num]
    return arr


def write(path, info):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(info, ensure_ascii=False, indent=2))


def psuct_analysis_item(arr, one_k, one_v, two_k, two_v, three_k, three_v, count):
    change_one = None
    for one in arr:
        if one[one_k] == one_v:
            change_one = one
            break
    if change_one is None:
        change_one = {
            one_k: one_v,
            'totalCount': 0,
            'data': []
        }
        arr.append(change_one)
    change_two = None
    for two in change_one['data']:
        if two[two_k] == two_v:
            change_two = two
            break
    if change_two is None:
        change_two = {
            two_k: two_v,
            'totalCount': 0,
            'data': []
        }
        change_one['data'].append(change_two)
    change_two['data'].append({
        three_k: three_v,
        "count": count
    })
    change_two['data'].sort(key=lambda x: x['count'], reverse=True)
    change_two['totalCount'] = change_two['totalCount'] + count
    change_one['data'].sort(key=lambda x: x['totalCount'], reverse=True)
    change_one['totalCount'] = change_one['totalCount'] + count
    arr.sort(key=lambda x: x['totalCount'], reverse=True)


if __name__ == '__main__':
    psuct_analysis("E:\\psuc.csv")
