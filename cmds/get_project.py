# coding: utf8

from utils.utils import parse_config

config = parse_config()


# 获取项目别名和项目名并返回
async def projects(*args, **kwargs):
    msg = {}
    for alias_name, project_info in config.project.items():
        msg[alias_name] = project_info.get('project_name')
    return {'errCode': 200, 'msg': msg}
