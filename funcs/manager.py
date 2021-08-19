from flask import Flask
from logging import StreamHandler, Formatter, handlers

config = {
    "dev": "../config/settings_dev.py",
    "prod": "../config/settings_prod.py",
    "test": "../config/settings_test.py",
}


def create_app(env):
    """

    :param config_name: info bug error
    :return:
    """
    # 创建app实例对象
    app = Flask(__name__)
    # 日志格式化
    fmt = '[%(asctime)s] [%(filename)s:%(lineno)d\t] [%(levelname)s] ' \
          '[ %(message)s ]'
    fmt = Formatter(fmt)
    file_handler = handlers.RotatingFileHandler('logs/flask.log', maxBytes=104857600, backupCount=20)
    file_handler.setFormatter(fmt)
    app.logger.addHandler(file_handler)

    # 实例对象从配置文件中加载配置
    app.config.from_pyfile(config[env])
    return app
