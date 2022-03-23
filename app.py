from flask import Flask,request
from logging import Formatter, handlers
from utils.utils_flask import call_back
from utils.utils_dd import check_sign
import json
import os
import asyncio

# 根据环境变量读取配置
if os.getenv('chatbot_env', 'dev') == 'prod':
    setting_class = 'ProductionConfig'
else:
    setting_class = 'DevelopmentConfig'


# 创建app实例对象
app = Flask(__name__)
# 日志格式化
fmt = '[%(asctime)s] [%(filename)s:%(lineno)d\t] [%(levelname)s] ' \
      '[ %(message)s ]'
fmt = Formatter(fmt)
file_handler = handlers.RotatingFileHandler('logs/flask.log', maxBytes=104857600, backupCount=20)
file_handler.setFormatter(fmt)
app.logger.addHandler(file_handler)

# 加载配置
app.config.from_object(f'config.settings.{setting_class}')
config = app.config


@app.route('/', methods=['POST'])
async def index():
    # 获取参数
    body = request.get_data()
    headers = request.headers

    # 校验签名，失败则直接return
    sign_check = check_sign(headers=headers, config=config)
    if sign_check.get('code'):
        return sign_check

    # 转换body成dict
    data = json.loads(body)

    # 从data中获取数据
    tmp_webhook = data['sessionWebhook']
    sender_nick = data.get('senderNick', 'unknown')
    sender_id = data.get('senderId', 'unknown')

    # 分割数据，第一个字段做函数名，剩余字段做参数
    msg_list = data['text']['content'].split()

    # 记录日志
    log_info = '用户:%s【%s】，执行操作:%s' % (sender_nick, sender_id, msg_list)
    app.logger.info(log_info)

    # 调用call_back
    res = await asyncio.create_task(await call_back(*msg_list, tmp_webhook=tmp_webhook, senderId=sender_id, senderNick=sender_nick, config=config))

    # 返回的结果为dict且状态码非零，则替换其中的content，否则删除content
    if isinstance(res, dict) and res.get('errCode'):
        data['text']['content'] = res.get('msg')
    else:
        del data['text']['content']

    return data


if __name__ == "__main__":
    app.debug = True
    app.run()
