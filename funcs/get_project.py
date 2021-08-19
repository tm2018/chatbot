# coding: utf8

import os
# 根据环境变量读取配置
env = os.getenv('chatbot_env', 'dev')
if env == 'prod':
    from ..config.settings_prod import project
else:
    from ..config.settings_dev import project

# 获取项目别名和项目名并返回
async def projects(*args, **kwargs):
    msg = {}
    for alias_name, project_info in project.items():
        msg[alias_name] = project_info.get('project_name')
    return {'errCode': 200, 'msg': msg}
