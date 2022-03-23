import logging


class BaseConfig(object):
    # 鉴权配置，只有senderId在配置中，才能进行某些敏感操作；senderId可通过查看docker获取
    SUPERS = ['']

    # 仅允许如下命令，其他命令返回提示信息
    ALL_COMMAND = ["hello", "test", "deploy", "projects", "add", "ref", "revoke"]

    # 公共方法，允许所有人执行
    COMMON_COMMAND = ['add']

    # 普通用户只开放如下端口，超管开放所有端口
    ports = ["80/80", "443/443", "8080/8080"]

    git_url = ""
    git_private_token = ""

    # 数据库配置,db需提前创建
    mysql_host = '10.1.1.1'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_passwd = '123456'
    mysql_db = 'devops'

    # jenkins地址
    jks_url = ""
    jks_user = ""
    jks_password = ""
    project = {}


class DevelopmentConfig(BaseConfig):
    # 是否开启debug
    DEBUG = True
    LOG_LEVEL = logging.WARNING

    # 钉钉app_secret
    APP_SECRET = ''

    # 阿里云配置
    access_key_id = ""
    access_key_secret = ""
    security_group_ids = []
    security_region_id = ""


class ProductionConfig(BaseConfig):
    # 是否开启debug
    DEBUG = False
    LOG_LEVEL = logging.INFO
    # 钉钉app_secret
    APP_SECRET = ''

    # 阿里云配置
    # access_key_id： 阿里云access_key_id，需给api调用权限
    # access_key_secret：阿里云access_key_secret
    # security_group_ids： 阿里云安全组id，支持多个
    # security_region_id：安全组所在区域
    access_key_id = ""
    access_key_secret = ""
    security_group_ids = [""]
    security_region_id = ""

    # 项目配置, 如下
    # test: 项目别名
    # project_name: 项目名称
    # prod: 项目环境
    # jks_job_name： jenkins任务名，需和实际严格一致
    # jks_params： jenkins参数，根据实际填写
    project = {
        "test": {
            "project_name": "",
            "prod": {
                "jks_job_name": "",
                "jks_params": {
                    "deploy_env": "",
                    "git_path": "",
                    "TAG_OR_BRANCH": "",
                    "repo_sub_path": "",
                    "dingtalk_id": ""
                }
            }
        },
    }
