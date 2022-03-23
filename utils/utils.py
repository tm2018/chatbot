# coding: utf8
import os
import pymysql
my_env = os.getenv('chatbot_env', 'dev')


# 基础方法
def get_deploy_info(project_origin):
    # 以-分割传入的参数project_origin
    project_tag_env = project_origin.split('-')
    # 长度大于等于3则取alias_name tag env
    if len(project_tag_env) >= 3:
        alias_name = project_tag_env[0]
        tag_or_branch = project_tag_env[1]
        deploy_env = project_tag_env[2]
    elif len(project_tag_env) == 2:
        alias_name = project_tag_env[0]
        tag_or_branch = project_tag_env[1]
        deploy_env = 'pre'
    else:
        alias_name = project_tag_env[0]
        tag_or_branch = ''
        deploy_env = ''
    return alias_name, tag_or_branch, deploy_env


def parse_config():
    # 根据环境变量读取配置
    from config.settings import DevelopmentConfig as config
    if my_env == 'prod':
        from config.settings import ProductionConfig as config

    return config


class MysqlToDo(object):
    def __init__(self):
        pass

    @staticmethod
    def conn(host, port, user, passwd, db):
        conn = pymysql.connect(host=host, port=port, user=user, password=passwd, database=db)
        return conn

    @staticmethod
    def sql_exec(conn, sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchone()
        print(data)

# conn = MysqlToDo.conn('127.0.0.1','3306','root','123456','test')
# sql = "INSERT INTO `11`(`name`) VALUES ('1111');"
# MysqlToDo.sql_exec(conn,sql)