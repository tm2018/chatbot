from flask import Flask, request
from .funcs.say import *
from .funcs.utils import *
from .funcs.deploy import deploy
from .funcs.manager import create_app, config
# from flask_script import Manager
import logging
import hmac
import hashlib
import base64
import json
import os
import asyncio

# 根据环境变量读取配置
env = os.getenv('chatbot_env', 'dev')
config_file = '%s%s_%s.py' % ('config/', 'settings', env)

config_name = config[env]
# 这里通过一个函数创建了app的实例对象
app = create_app(env)
# app.logger.debug('sign check failed')

@app.route('/', methods=['POST'])
async def my_run():
    # 获取参数
    body = request.get_data()
    headers = request.headers

    timestamp = headers.get('Timestamp')
    sign = headers.get('Sign')
    app_secret = app.config['APP_SECRET']
    user_list = app.config['USERS_LIST']

    # 校验签名，失败则返回403
    check = check_sign(timestamp, app_secret, sign)
    if not check:
        msg = 'sign check failed'
        app.logger.debug(msg)
        return "{'code':403, 'msg':'%s'}" %(msg)

    # 转换body成dict
    data = json.loads(body)

    # senderId不在USERS_LIST中则提示非法用户
    if len(user_list) and data['senderId'] not in user_list:
        msg = "非法用户,请联系管理员授权！"
        data['text']['content'] = msg
        sender_nick = data.get('senderNick', 'none')
        app.logger.debug(sender_nick + '---' +msg)
        print(data)
        return data

    res = await asyncio.create_task(call_back(data))

    # 返回的结果为dict且状态码非零，则替换其中的content，否则删除content
    if isinstance(res, dict) and res.get('errCode'):
        data['text']['content'] = res.get('msg')
    else:
        del data['text']['content']

    return data


def check_sign(timestamp, app_secret, sign):
    # 计算签名
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign_made = base64.b64encode(hmac_code).decode('utf-8')

    # 算出的签名和获取的签名不一致则返回空
    if sign_made != sign:
        return ''
    return sign


# 处理数据，最终调用一个函数
async def call_back(data):
    tmp_webhook = data['sessionWebhook']
    content = data['text']['content']
    msg_list = content.split()

    # 根据content内容调用不同函数并传参
    func_name = msg_list[0]
    args = msg_list[1:]

    # 只允许部分方法
    funcs_allowed = app.config["FUNCS_ALLOWED"]
    if func_name not in funcs_allowed:
        msg = "方法使用错误，仅允许%s" %('|'.join(funcs_allowed))

        await SendMessage.send_text(tmp_webhook, msg)
        return msg
    log_info = '用户:%s，执行命令%s' %(data.get('senderNick', 'none'), msg_list)
    app.logger.info(log_info)
    res = await eval(func_name)(args, webhook=tmp_webhook)
    return res


if __name__ == "__main__":
    app.run()
