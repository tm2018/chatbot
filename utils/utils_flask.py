# coding: utf8
# 和flask框架 相关的方法

from functools import wraps
from utils.utils_dd import SendMessage
import os
from cmds.say import hello
from cmds.deploy import deploy
from cmds.ali_firewall import add, revoke
from cmds.ali_ref import ref
from cmds.get_project import projects


# 装饰器，用于鉴权
def check(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        # 获取参数
        func_name = args[0]
        tmp_webhook = kwargs.get('tmp_webhook')
        senderId = kwargs.get('senderId')
        senderNick = kwargs.get('senderNick')

        # 非超管用户，只能运行普通命令

        if senderId not in kwargs.get('config').get('SUPERS') and func_name not in kwargs.get('config').get('COMMON_COMMAND'):
            msg = '用户:%s无权使用方法:%s，请联系管理员授权!' % (senderNick, func_name)
            await SendMessage.send_text(tmp_webhook, msg)
            return msg
        return f(*args, **kwargs)
    return decorated


# 调用实际方法
@check
async def call_back(*args, **kwargs):
    # 从传参中获取函数名 参数和webhook地址等
    func_name = args[0]
    args = args[1:]
    tmp_webhook = kwargs.get('tmp_webhook')
    sender_id = kwargs.get('senderId')

    # 仅允许如下方法，否则返回提示信息
    all_command = kwargs.get('config').get('ALL_COMMAND')
    if func_name not in all_command:
        msg = "方法使用错误，仅允许%s" % ('|'.join(all_command))
        await SendMessage.send_text(tmp_webhook, msg)
        return msg

    res = await eval(func_name)(*args, webhook=tmp_webhook, sender_id=sender_id)
    return res
