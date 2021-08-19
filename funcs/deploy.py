# coding: utf8

from .utils import SendMessage, JenkinsOp, GitlabOp
# from .gitlab_ops import GitlabOp
from .get_project import projects
import os

# 根据环境变量读取配置
env = os.getenv('chatbot_env', 'dev')
if env == 'prod':
    from ..config.settings_prod import jenkins_url, jenkins_user, jenkins_password, project, git_url, git_private_token
else:
    from ..config.settings_dev import jenkins_url, jenkins_user, jenkins_password, project, git_url, git_private_token


# deploy命令时执行如下函数
async def deploy(*args, **kwargs):
    webhook = kwargs.get("webhook")

    # 支持输入多个
    alias_name_list = args[0]

    for alias_name in alias_name_list:
        # 参数help时，返回帮助并跳过本次循环
        if alias_name == 'help':
            msg_list = []
            project_info = await projects()
            for k, v in project_info.get('msg').items():
                tmp = '发布项目%s：deploy %s' % (v, k)
                msg_list.append(tmp)
            msg = '%s' % ('\n'.join(msg_list))
            # msg = {"errCode": 200, "msg": my_str}
            await SendMessage.send_text(webhook, msg)
            continue

        # 根据alias_name获取配置
        project_info = project.get(alias_name)

        # 未获取到配置则跳过本次循环
        if not project_info:
            msg = {"errCode": 404, "msg": "项目:%s不存在，请用deploy help获取命令!" % alias_name}
            await SendMessage.send_text(webhook, msg)
            continue

        depends = project_info.get('depends')
        project_name = project_info.get('project_name')
        jenkins_job_name = project_info.get('jenkins_job_name')
        params = project_info.get('params', '')
        namespace_name = project[alias_name]["namespace"]

        # 存在其他依赖项目，则递归发布
        if depends:
            await deploy([depends], webhook=webhook)

        # 合并请求
        if namespace_name:
            conn = GitlabOp.gitlab_conn(git_url, git_private_token)
            res = GitlabOp.merge_requests(conn, namespace_name, project_name, target_branch='master')
            msg = res.get("msg")
            await SendMessage.send_text(webhook, msg)

        # 调用jenkins发布代码
        if jenkins_job_name:
            res1 = await JenkinsOp.build_job(jenkins_url, jenkins_user, jenkins_password, jenkins_job_name, params)
            await SendMessage.send_text(webhook, res1.get('msg'))

    msg = {'errCode': 0, 'msg': '项目:%s调用操作完成，请等待！' % (','.join(alias_name_list))}
    await SendMessage.send_text(webhook, msg)
