import json
import os
import shutil

origin_dir = 'E:\\dopdata\\DataOpenFiles\\'
target_dir = 'E:\\dopdata\\target\\'
trans_target_dir = 'E:\\dopdata\\trans_target\\'
postfix_target_dir = 'E:\\dopdata\\postfix_target\\'

if __name__ == '__main__':
    file_id_dept_name_map = json.load(open("E:\\dopdata\\file_id_dept_name_map.json", "r", encoding='utf-8'))
    file_id_filename_map = json.load(open("E:\\dopdata\\file_id_filename_map.json", "r", encoding='utf-8'))
    files = os.listdir(origin_dir)
    file_dict = {}
    for file in files:
        dept_name = file_id_dept_name_map.get(file, '部门未找到')
        trans_filename = file_id_filename_map.get(file, file)
        ts = trans_filename.split("\\")
        ts2 = trans_filename.split(".")
        trans_filename = ts[len(ts)-1]
        file_type = ts2[len(ts2)-1]
        target_dept_dir = target_dir+dept_name+"\\"
        trans_target_dept_dir = trans_target_dir+dept_name+"\\"
        postfix_target_dept_dir = postfix_target_dir+dept_name+"\\"
        if not os.path.exists(target_dept_dir):
            os.mkdir(target_dept_dir)
            os.mkdir(trans_target_dept_dir)
            os.mkdir(postfix_target_dept_dir)
        shutil.copy(origin_dir+file, target_dept_dir)
        shutil.copy(origin_dir+file, trans_target_dept_dir+trans_filename)
        shutil.copy(origin_dir+file, postfix_target_dept_dir+file+'.'+file_type)
