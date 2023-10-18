# 项目克隆工具

## 简介
 用于快速将一个项目复制出来，并替换其中部分文字

## 环境依赖
 windows、python3
 
## 配置文件说明

### config.json

* #### replace_file_types 需要替换文本的文件类型 

* #### original_project 原始项目信息
  + root_path: 项目根目录绝对路径
  + block_list: 黑名单 不复制
* #### target_projects 目标项目信息列表
  + root_path: 项目根目录绝对路径
  * allow_list: 白名单 不参与文件字符串替换
  * replace_dir_list: 参与替换文件夹列表，会递归
  * replace_dict: 替换字典， key为原始字段，value为目标字段
  * replace_file_list: 参与替换文件列表
    + path: 文件路径
    + replace_dict: 文件替换字典
