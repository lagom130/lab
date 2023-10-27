import csv

filename = 'E:\\codeQC.csv'


def analysis(filename):
    code_dict = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] is not None and row[0] != '':
                code = row[0]
                if code in code_dict:
                    code_dict[code] = code_dict[code] + 1
                else:
                    code_dict[code] = 1
            if row[1] is not None and row[1] != '':
                code = row[1]
                if code in code_dict:
                    code_dict[code] = code_dict[code] + 1
                else:
                    code_dict[code] = 1
            if row[2] is not None and row[2] != '':
                code = row[2]
                if code in code_dict:
                    code_dict[code] = code_dict[code] + 1
                else:
                    code_dict[code] = 1

    for key in code_dict:
        if code_dict[key] > 1:
            print(key+ ": "+ str(code_dict[key]))


if __name__ == '__main__':
    analysis(filename)
    list = [
        '30701505813120010000000000/000016', 22
        '30701505813050250000000000/000003', 116
        '30701505813050160000000000/000050',181
    ]