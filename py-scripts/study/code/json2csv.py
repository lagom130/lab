import json
import csv
import os


def csv_json(path):
    json_fp = open(path+'.json', "r", encoding='utf-8')
    csv_fp = open(path+'.csv', "w", encoding='utf-8')

    data_list = json.load(json_fp)


    sheet_data = []
    for data in data_list:

        sheet_data.append(data.values())

    writer = csv.writer(csv_fp)

    writer.writerows(sheet_data)

    json_fp.close()
    csv_fp.close()

if __name__ == "__main__":
    root = os.getcwd()

    csv_json(root + '/{}_top'.format('provider'))
    csv_json(root + '/{}_top'.format('applicant'))