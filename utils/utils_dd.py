# coding: utf8

import hmac
import hashlib
import base64
import requests_async as requests


# 签名校验方法
def check_sign(*args, **kwargs):
    # 从传入参数获取变量
    config = kwargs.get('config')
    headers = kwargs.get('headers')

    # 生成签名
    app_secret = config.get('APP_SECRET')
    timestamp = headers.get('Timestamp')
    sign = headers.get('Sign')
    app_secret_enc = config.get('APP_SECRET').encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign_made = base64.b64encode(hmac_code).decode('utf-8')

    # 比较签名，不一致则返回403
    if sign_made != sign:
        msg = '非法请求！原因:签名校验失败'
        return {'code': 403, 'msg': f'{msg}'}
    return {'code': 0, 'sign': f'{sign}'}


# 发送消息
class SendMessage(object):
    @staticmethod
    async def send_text(url, msg):
        data = {
            'msgtype': 'text',
            'text': {
                'content': msg
            }
        }
        await requests.post(url, json=data)
        print('text消息发送完成')

    @staticmethod
    async def send_md(url, msg):
        data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "命令执行结果通知",
                    "text": msg
                }
        }
        await requests.post(url, json=data)
        print('text消息发送完成')
