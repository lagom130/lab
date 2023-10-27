import base


env = 'DEV'
receivers = None
mongo_client = None
cursor = None

if __name__ == '__main__':
    mongo_client, cursor, receivers, mysql_conn = base.init_envs(env)
    # 创建一个字典,key是business_handling_code,value是实体
    item_id_dict = {}
    print("0/5 开始解析历史数据")
    # 读取原表数据,记录所有task_guid和id的映射关系
    task_list = base.get_mysql_res(cursor, "SELECT * FROM cmp_catalog.task order by update_time")
    for task in task_list:
        item_id_dict[task['business_handling_code']] = task


    # 遍历字典,将唯一的task_guid对应的id查找出来插入新表
    print("1/5 创建事项新表")
    cursor.execute("CREATE TABLE cmp_catalog.`task_new` ( `id` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL, `task_guid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '事项guid', `task_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '事项类型', `task_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '事项名称', `basic_catalog_code` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '基本目录编码', `business_handling_code` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '业务办理项编码', `implement_list_code` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '实时清单编码', `dept_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '本平台部门ID', `ou_code` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '行政审批局部门编码', `ou_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '行政审批局部门名称', `area_code` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '区划编码', `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间', `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间', PRIMARY KEY (`id`) USING BTREE, INDEX `idx_dept_id_task_type`(`dept_id`, `task_type`) USING BTREE ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '事项' ROW_FORMAT = Dynamic;")
    mysql_conn.commit()
    print("2/5 处理后事项数据插入新表")
    for task in item_id_dict.values():
        cursor.execute("INSERT INTO cmp_catalog.task_new(id, task_guid, task_type, task_name, basic_catalog_code, business_handling_code, implement_list_code, dept_id, ou_code, ou_name, area_code, update_time, create_time) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" ,(task['id'], task['business_handling_code'], task['task_type'], task['task_name'], task['basic_catalog_code'], task['business_handling_code'], task['implement_list_code'], task['dept_id'], task['ou_code'], task['ou_name'], task['area_code'], task['update_time'], task['create_time']))
    mysql_conn.commit()
    print("3/5 重命名事项旧表用于备份")
    cursor.execute("RENAME TABLE cmp_catalog.task TO cmp_catalog.task_old_backup;")
    mysql_conn.commit()
    print("4/5 重命名事项新表,事项数据处理完成")
    cursor.execute("RENAME TABLE cmp_catalog.task_new TO cmp_catalog.task;")
    mysql_conn.commit()
    print("5/5 处理目录历史数据")
    cursor.execute("UPDATE cmp_catalog.info_resource_platform SET task_guid = business_handling_code WHERE task_guid IS NOT NULL OR task_guid != '' AND ( business_handling_code IS NULL OR business_handling_code = '')")
    mysql_conn.commit()
    print("全部完成，遗留guid本身不存在的数据，无法处理")
    mysql_conn.close()