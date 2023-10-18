# coding=utf8
import json
import os


def replace_all_config_git_address(root_path, old_str, new_str):
    project_dirs = os.listdir(root_path)
    for project_dir in project_dirs:
        config_path = root_path + '\\' + project_dir + '\\.git\\config'
        if os.path.exists(config_path):
            string_replace_in_file(config_path, old_str, new_str)


def string_replace_in_file(file, old_str, new_str):
    with open(file, 'r', encoding='utf-8') as f1, open('%s.bak' % file, 'w', encoding='utf-8') as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
    os.remove(file)
    os.rename('%s.bak' % file, file)


def read_config():
    root = os.getcwd()
    path = root + '/config.json'
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    # 0. read config from json
    config = read_config()
    path = config.get('root_path', os.getcwd())
    original_address = config.get('original')
    target_address = config.get('target')

    replace_all_config_git_address(path, original_address, target_address)
