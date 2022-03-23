# coding: utf8

import os
from utils.utils_dd import SendMessage
from utils.utils_ali import RefreshDcdn
from utils.utils import parse_config

config = parse_config()


# ref命令时执行如下函数
async def ref(*args, **kwargs):
    '''
    刷新cdn缓存，cdn地址在settings_prod.py中
    :param args:
    :param kwargs:
    :return:
    '''

    webhook = kwargs.get("webhook")
    domain = kwargs.get('domain')
    # 从输入参数中项目名，支持多个

    project_list = args
    msg_list = []
    msg = f'debug:项目信息{args}'
    await SendMessage.send_text(webhook, msg)

    # domain存在则直接调用阿里api刷新缓存
    if domain:
        try:
            RefreshDcdn.refresh_dcdn(config.access_key_id, config.access_key_secret, domain)
            msg = '已刷新项目别名:%s的cdn缓存，请验证--' % (args[0])
            msg_list.append(msg)
        except Exception as e:
            msg = '刷新项目别名:%s的cdn缓存失败，请检查，原因:%s--' % (args[0], e)
            msg_list.append(msg)
    else:
        for project_env in project_list:
            # 以-分割传入的参数，取项目名和环境,分割后长度为1则取pre环境
            project_info = project_env.split('-')
            if len(project_info) > 1:
                alias_name, env = project_info[0:2]
            else:
                alias_name = project_env
                env = "pre"

            # 参数help时，返回帮助并跳过本次循环
            if alias_name == 'help':
                msg = '刷新阿里云cdn缓存，用法: ref project1-env1 project2-env2 project3-env3 ...'
                msg_list.append(msg)
                continue

            project_config = config.project.get(alias_name)

            # 根据alias_name查询配置，未获取到将跳过
            if not project_config:
                msg = '获取项目别名:%s配置失败，请检查项目是否存在' % ( alias_name )
                msg_list.append(msg)
                continue
            # 根据环境取domain，未获取到则跳过
            if project_config.get(env) and project_config.get(env).get('domain'):
                domain = project_config.get(env).get('domain')
            else:
                msg = '获取项目别名:%s的环境:%s或域名失败,请检查' % (alias_name, env)
                msg_list.append(msg)
                continue

            # 捕获异常，有异常则发送钉钉消息
            try:
                RefreshDcdn.refresh_dcdn(config.access_key_id, config.access_key_secret, domain)
                msg = '已刷新项目别名:%s的cdn缓存，请验证--' % (alias_name)
                msg_list.append(msg)
            except Exception as e:
                msg = '刷新项目别名:%s的cdn缓存失败，请检查，原因:%s--' % (alias_name, e)
                msg_list.append(msg)

    messages = '\n'.join(msg_list)
    await SendMessage.send_text(webhook, messages)
