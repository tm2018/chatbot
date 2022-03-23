# coding: utf8


import datetime
from utils.utils_dd import SendMessage
from utils.utils_ali import EcsRulesOp
from utils.utils import parse_config

config = parse_config()
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

client = EcsRulesOp.create_client(config.access_key_id, config.access_key_secret)


# 执行add命令时，会调用如下方法
async def add(*args, **kwargs):
    '''
    修改阿里云安全组
    :param args:
    :param kwargs:
    :return:
    '''

    webhook = kwargs.get("webhook")
    sender_id = kwargs.get("sender_id")
    # 从输入参数中获取ip地址，支持输入多个ip
    ip_list = args

    # 超管会开放所有端口，否则开放指定端口
    port_list = config.ports if sender_id not in config.SUPERS else ["1/65535"]

    for ip in ip_list:
        # 参数help时，返回帮助并跳过本次循环
        if ip == 'help':
            msg = '添加安全组规则，用法: op ip 或op ip1 ip2 ip3 ip4'
            await SendMessage.send_text(webhook, msg)
            continue

        for security_group in config.security_group_ids:
            for port_range in port_list:
                data = {
                    "region_id": "cn-shanghai",
                    "security_group_id": security_group,
                    "ip_protocol": "tcp",
                    "port_range": port_range,
                    "source_cidr_ip": ip,
                    "description": "devops自动化添加 by devops at %s" % (time)
                }

                EcsRulesOp.add_rules_in(client, **data)
            msg = '已添加ip:%s, 端口:%s,到安全组:%s' % (ip, '|'.join(port_list), security_group)
            await SendMessage.send_text(webhook, msg)


# 执行revoke时执行如下函数
async def revoke(*args, **kwargs):
    security_region_id = config.security_region_id
    # 循环清理
    for security_group_id in config.security_group_ids:
        # 组合参数
        revoke_data = {
            'security_group_id': security_group_id,
            'region_id': security_region_id
        }
        msg = "清理区域:%s， 安全组:%s中的所有规则，请关注!" % (security_region_id, security_group_id)
        webhook = kwargs.get("webhook")
        await SendMessage.send_text(webhook, msg)
        EcsRulesOp.revoke_rules_in(client, **revoke_data)
