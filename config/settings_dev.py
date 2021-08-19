import logging
# 是否开启debug
DEBUG = True
LOG_LEVEL = logging.DEBUG

# 钉钉app_secret，以以企业管理员进入钉钉开发者中心可获取
APP_SECRET = ''

# 鉴权配置，只有senderId在配置中，才能进行某些敏感操作
USERS_LIST = {'bb', 'aaaaaaaaa'}

# 限制方法，其他方法返回提示信息
FUNCS_ALLOWED = ["hello", "help", "test", "deploy", "projects"]

# gitlab配置
git_url = ''
git_private_token = ""

# jenkins地址
jenkins_url = ""
jenkins_user = ""
jenkins_password = ""

# 项目配置
project = {
    "tt": {
        "project_name": "test-api",
        "namespace": "devops/test",
        "jenkins_job_name": "PROD-test-api",
        # "depends": "smc",
        "params": {
            "deploy_env": "prod"
        }
    }
}
