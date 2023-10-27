import json
import os
import shutil
import time

import requests

COOKIE = ''
CAT_ID = ''
HOST = ''

CAT_URL_TEMPLATE = 'http://{host}/api/interface/list_cat?page=1&limit=100&catid={cat_id}'

API_DETAIL_URL_TEMPLATE = 'http://{host}/api/interface/get?id={id}'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'

input_param_desc = '\n     * @param {name}  {desc}'
controller_query_param = '@QueryParam("{name}") String {name}'
service_query_param = 'String {name}'

controller_methods = []
service_methods = []
local_host_rest_client_methods = []
actual_host_rest_client_methods = []
api_infos = []


def get_api_id_list(host, cookie, cat_id):
    url = CAT_URL_TEMPLATE.format(host=host, cat_id=cat_id)
    headers = {'user-agent': user_agent, 'cookie': cookie}
    r = requests.get(url, headers=headers)
    response_body = r.json()
    data = response_body.get('data')
    api_list = data.get('list')
    api_id_arr = []
    for api in api_list:
        api_id_arr.append(api.get('_id'))
    return api_id_arr


def get_api_info(host, cookie, id):
    url = API_DETAIL_URL_TEMPLATE.format(host=host, id=id)
    headers = {'user-agent': user_agent, 'cookie': cookie}
    r = requests.get(url=url, headers=headers)
    response_body = r.json()
    data = response_body.get('data')
    return data


def read_config():
    root = os.getcwd()
    path = root + '/config.json'
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def method_convert(api_info, config):
    root_path = config.get('root_path')
    rest_client_method_template = open('template/rest_client_method.txt').read()
    controller_method_template = open('template/controller_method.txt').read()
    service_method_template = open('template/service_method.txt').read()
    input_check_template = open('template/input_check.txt').read()
    path = api_info.get('path')[len(root_path):]
    method_type = api_info.get('method')
    name_words = path.split('/')
    method_name = method_type.lower()
    for word in name_words:
        if len(word) > 0:
            method_name = method_name + ''.join(w[0].upper() + w[1:] for w in word.split())
    method_desc = api_info.get('title')
    req_query = api_info.get('req_query')
    controller_query_params = []
    service_query_params = []
    method_input_desc_arr = []
    service_input_arr = []
    param_check_arr = []
    rest_client_query_params = []
    for item in req_query:
        param_name = item.get('name')
        param_desc = item.get('desc')
        param_required = item.get('required')
        param_example = item.get('example', None)
        method_input_desc_arr.append(input_param_desc.format(name=param_name, desc=param_desc))
        controller_query_params.append(controller_query_param.format(name=param_name))
        service_query_params.append(service_query_param.format(name=param_name))
        service_input_arr.append(param_name)
        if param_required == '1':
            if param_example is not None:
                rest_client_query_params.append(param_name + '=' + param_example)
            param_check_arr.append(input_check_template.format(param=param_name))
    controller_method = controller_method_template.format(method_type=method_type.upper(), path=path,
                                                          method_name=method_name,
                                                          method_desc=method_desc,
                                                          input_desc=''.join(method_input_desc_arr),
                                                          controller_input=', '.join(controller_query_params),
                                                          input_check='\n'.join(param_check_arr),
                                                          service_input=', '.join(service_input_arr))
    service_method = service_method_template.format(method_name=method_name,
                                                    method_desc=method_desc,
                                                    input_desc=''.join(method_input_desc_arr),
                                                    service_input=', '.join(service_query_params))
    local_host_rest_client_method_url = rest_client_method_template.format(method_name=method_name,
                                                                           method_desc=method_desc,
                                                                           method_type=method_type.upper(),
                                                                           test_host=config.get('local_host'),
                                                                           root_path=root_path,
                                                                           path=path)
    actual_host_rest_client_method_url = rest_client_method_template.format(method_name=method_name,
                                                                            method_desc=method_desc,
                                                                            method_type=method_type.upper(),
                                                                            test_host=config.get('actual_host'),
                                                                            root_path=root_path,
                                                                            path=path)

    rest_client_method_query_params = '&'.join(rest_client_query_params)

    if len(rest_client_method_query_params) > 0:
        local_host_rest_client_method_url = '?'.join(
            [local_host_rest_client_method_url, rest_client_method_query_params])
        actual_host_rest_client_method_url = '?'.join(
            [actual_host_rest_client_method_url, rest_client_method_query_params])

    controller_methods.append(controller_method)
    service_methods.append(service_method)
    local_host_rest_client_methods.append(local_host_rest_client_method_url)
    actual_host_rest_client_methods.append(actual_host_rest_client_method_url)
    if config.get('visualization', False):
        api_info_url = 'http://' + config.get('actual_host') + root_path + path
        if len(rest_client_method_query_params) > 0:
            api_info_url = '?'.join([api_info_url, rest_client_method_query_params])
        api_infos.append({
            'api_name': method_desc,
            'api_url': api_info_url,
        })


if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.mkdir('output')

    config = read_config()
    host = config.get("api_center_host")
    cookie = config.get("api_center_cookie")
    cat_id = config.get("cat_id")
    api_id_arr = get_api_id_list(host, cookie, cat_id)
    if len(api_id_arr) == 0:
        print("no api")
    else:
        for api_id in api_id_arr:
            api_info = get_api_info(host, cookie, str(api_id))
            method_convert(api_info, config)
    if len(controller_methods) > 0:
        package = config.get('package')
        class_name = config.get('class')
        class_desc = config.get('class_desc')
        root_path = config.get('root_path')
        date = time.strftime('%Y/%m/%d', time.localtime())
        controller_temp = open('template/controller.txt').read()
        controller_str = controller_temp.format(package=package, class_name=class_name, class_desc=class_desc,
                                                root_path=root_path, date=date,
                                                method_arr='\n'.join(controller_methods))
        with open('output\\' + class_name + 'Controller.java', 'w', encoding='utf-8') as cf:
            cf.write(controller_str)
            cf.close()
    if len(service_methods) > 0:
        service_temp = open('template/service.txt').read()
        service_str = service_temp.format(package=package, class_name=class_name, class_desc=class_desc, date=date,
                                          method_arr='\n'.join(service_methods))
        with open('output\\' + class_name + 'Service.java', 'w', encoding='utf-8') as sf:
            sf.write(service_str)
            sf.close()
    if len(local_host_rest_client_methods) > 0:
        local_host_rest_client_str = '\n'.join(local_host_rest_client_methods)
        with open('output\\Local' + class_name + '.rest', 'w', encoding='utf-8') as rf:
            rf.write(local_host_rest_client_str)
            rf.close()
    if len(actual_host_rest_client_methods) > 0:
        actual_host_rest_client_str = '\n'.join(actual_host_rest_client_methods)
        with open('output\\Actual' + class_name + '.rest', 'w', encoding='utf-8') as rf:
            rf.write(actual_host_rest_client_str)
            rf.close()
    if config.get('visualization', False) and len(api_infos) > 0:
        with open('output\\visualization_apis.json', 'w', encoding='utf-8') as af:
            af.write(json.dumps(api_infos, ensure_ascii=False, indent=2))
            af.close()
