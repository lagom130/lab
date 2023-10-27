import datetime
import zipfile

from workshop import base

env = "DEV"


def get_info_resource_op_dict(mongo_client):
    pipeline = [
        {
            "$match": {
                "operation": {
                    "$in": ["发布", "申请发布", "申请撤销", "撤销退回", "发布退回", "撤销"]
                }
            }
        },
        {
            "$group": {
                "_id": "$infoResourceId",
                "audit_time": {
                    "$max": {
                        "$cond": [
                            {
                                "$in": [
                                    "$operation",
                                    ["发布", "撤销退回", "发布退回", "撤销"]
                                ]
                            },
                            "$createTime",
                            None
                        ]
                    }
                },
                "apply_time": {
                    "$max": {
                        "$cond": [
                            {
                                "$in": [
                                    "$operation",
                                    ["申请撤销", "申请发布"]
                                ]
                            },
                            "$createTime",
                            None
                        ]
                    }
                }
            }
        }
    ]
    result = mongo_client['infoResOPLogEntity'].aggregate(pipeline)
    dict_result = {}
    for doc in result:
        resource_id = doc["_id"]
        audit_time = doc["audit_time"]
        apply_time = doc["apply_time"]

        dict_result[resource_id] = {
            "audit_time": audit_time,
            "apply_time": apply_time
        }
    return dict_result

if __name__ == '__main__':
    mongo_client, cursor, receivers = base.init_envs(env)
    print('env='+env+', will send to'+str(receivers))
    print('statistical task started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 1 目录发布审核统计
    # 1.1 TODO：目录操作日志，用于获取申请发布时间和平台审核时间
    info_res_log_dict = get_info_resource_op_dict(mongo_client)
    # 1.2 TODO:目录发布审核（区县）
    # 运营要的：目录名称、目录发布状态、提供方、申请发布时间、平台管理员审核时间
    # 扩充内容： 目录ID、提供方属地
    # 1.3. TODO:目录发布审核（市级）
    # 运营要的：目录名称、目录发布状态、提供方、申请发布时间、平台管理员审核时间
    # 扩充内容： 目录ID、提供方属地
    # 2 资源发布审核统计
    # 2.1 TODO：资源操作日志，用于获取申请发布时间和平台审核时间(只查询资源的，不查询申请的，减少数据量)
    # 2.2 TODO:共享资源发布审核（区县）
    # 运营要的：共享资源名称、共享资源类型、共享资源发布状态、提供方、申请发布时间、平台管理员审核时间
    # 扩充内容： 目录ID、目录名称、resourceId、shareResourceId、共享类型、提供方属地
    # 2.3 TODO:共享资源发布审核（区县）
    # 运营要的：共享资源名称、共享资源类型、共享资源发布状态、提供方、申请发布时间、平台管理员审核时间
    # 扩充内容： 目录ID、目录名称、resourceId、shareResourceId、共享类型、提供方属地
    # 3 申请审核统计
    # 不需要查询操作日志，申请实体中有申请和审核时间
    # 3.1 TODO:共享资源申请审核（所有状态的）
    # 运营要的：申请方、共享资源名称、提供方、申请状态、发起申请时间、平台管理员审核时间
    # 扩充内容： 目录ID、目录名称、resourceId、shareResourceId、提供方审核时间

    # 6. 组装xlsx
    print('statistical task complete at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
