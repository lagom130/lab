# coding=utf8
import json
import shutil
import os


def copy_dir(original_path, target_path, no_copy_path_arr):
    file_list = os.listdir(original_path)
    for item in file_list:
        original_item_path = original_path + '\\' + item
        target_item_path = target_path + '\\' + item
        if original_item_path in no_copy_path_arr:
            continue
        if os.path.exists(original_item_path):
            if os.path.isdir(original_item_path):
                if not os.path.exists(target_item_path):
                    os.makedirs(target_item_path)
                copy_dir(original_item_path, target_item_path, no_copy_path_arr)
            else:
                copy_file(original_item_path, target_item_path)


def copy_file(original_path, target_path):
    # print('****[file copy]: ' + original_path + ' -> ' + target_path)
    shutil.copyfile(original_path, target_path)


def replace_all_files(root_path, replace_dict, no_replace_path_arr, file_types):
    file_list = os.listdir(root_path)
    for item in file_list:
        item_path = root_path + '\\' + item
        if os.path.exists(item_path):
            if item_path in no_replace_path_arr:
                continue
            if os.path.isdir(item_path):
                replace_all_files(item_path, replace_dict, no_replace_path_arr, file_types)
            else:
                string_replace_in_file(item_path, replace_dict, file_types)


def string_replace_in_file(file, replace_dict, file_types):
    # 只匹配下面的文件类型
    if not file.split('.')[-1] in file_types:
        return
    with open(file, 'r', encoding='utf-8') as f1, open('%s.bak' % file, 'w', encoding='utf-8') as f2:
        replaced_logs = []
        for index, line in enumerate(f1):
            for key in replace_dict:
                old_str = key
                new_str = replace_dict[key]
                if old_str in line:
                    line = line.replace(old_str, new_str)
                    replaced_logs.append('    line' + str(index+1) + ': ' + old_str + ' -> ' + new_str)
            f2.write(line)
        if len(replaced_logs) > 0:
            print('====[text replace]: ' + file)
            for replaced_log in replaced_logs:
                print(replaced_log)
    os.remove(file)
    os.rename('%s.bak' % file, file)


def read_config():
    root = os.getcwd()
    path = root + '/config.json'
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def clone(config):
    file_types = config.get('replace_file_types')
    original_project = config.get('original_project', {})
    original_project_root_path = original_project.get('root_path')
    # 0.1 处理复制黑名单，跳过不需要复制的文件
    relative_no_copy_path_list = original_project.get('block_list', [])
    no_copy_path_list = []
    for relative_path in relative_no_copy_path_list:
        no_copy_path_list.append(original_project_root_path + relative_path)
    target_projects = config.get('target_projects', [])

    # 开始复制并替换
    for target_project in target_projects:
        target_project_root_path = target_project.get('root_path')
        print('****[project copy]-[start]: ' + original_project_root_path + ' -> ' + target_project_root_path)
        # 1. 复制项目
        if os.path.exists(target_project_root_path):
            print('****[project copy]-[target address exist]-[start remove tree]: ' + target_project_root_path)
            shutil.rmtree(target_project_root_path)
            print('****[project copy]-[target address exist]-[old remove complete]: ' + target_project_root_path)

        print('****[project copy]-[complete]: ' + target_project_root_path)
        os.makedirs(target_project_root_path)
        copy_dir(original_project_root_path, target_project_root_path, no_copy_path_list)
        print('****[project copy]-[complete]: ' + target_project_root_path)
        # 2. 替换文本
        # 2.0 处理替换白名单，跳过不需要替换的文件
        relative_no_replace_path_list = target_project.get('allow_list', [])
        no_replace_path_list = []
        for relative_path in relative_no_replace_path_list:
            no_replace_path_list.append(target_project_root_path + relative_path)

        replace_dict = target_project.get('replace_dict')
        # 2.1 文件夹递归处理替换文本
        replace_dir_list = target_project.get('replace_dir_list', [])
        for replace_dir in replace_dir_list:
            target_root_path = target_project_root_path + replace_dir
            replace_all_files(target_root_path, replace_dict, no_replace_path_list, file_types)
        # 2.2 文件处理替换文本
        replace_file_list = target_project.get('replace_file_list', [])
        for replace_file_obj in replace_file_list:
            replace_file_path = replace_file_obj.get('path')
            file_replace_dict = replace_file_obj.get('replace_dict')
            target_root_path = target_project_root_path + replace_file_path
            string_replace_in_file(target_root_path, file_replace_dict, file_types)


if __name__ == '__main__':
    # 0. 读取配置
    config = read_config()
    clone(config)
