# coding: utf8

from utils.utils_dd import SendMessage
from utils.utils_jks import JksOp
from utils.utils import get_deploy_info
from utils.utils import MysqlToDo
from .get_project import projects

from utils.utils import parse_config
from cmds.ali_ref import ref
import datetime
config = parse_config()


# deploy命令时执行如下函数
async def deploy(*args, **kwargs):
    webhook = kwargs.get("webhook")

    # 支持输入多个并去重
    project_list = list(set(args))
    msg_list = []
    for project_origin in project_list:
        # 以-分割传入的参数project_origin
        alias_name, tag_or_branch, deploy_env = get_deploy_info(project_origin)
        # 获取时间
        deploy_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # alias_name==help时，返回帮助并跳过本次循环
        if alias_name == 'help':
            project_info = await projects()
            for k, v in project_info.get('msg').items():
                tmp = '发布项目%s：deploy %s-tag-env\n' % (v, k)
                msg_list.append(tmp)
            continue

        # tag为空或tag不符合则跳出循环
        if not tag_or_branch or deploy_env not in ['pre', 'prod']:
            msg = {"errCode": 404, "msg": "未获取到项目:%s的tag或tag不正确，当前project_tag_env=%s!\n" % (alias_name, project_origin)}
            msg_list.append(msg.get('msg'))
            continue

        # 根据alias_name获取配置
        project_info = config.project.get(alias_name)

        # 未获取到配置则跳过本次循环
        if not project_info:
            msg = {"errCode": 404, "msg": "项目:%s不存在，请用deploy help获取命令!\n" % alias_name}
            msg_list.append(msg.get('msg'))
            continue

        depends = project_info.get('depends')
        jks_job_name = project_info.get(deploy_env).get('jks_job_name')
        jks_params = project_info.get(deploy_env).get('jks_params', '')
        project_info[deploy_env]['jks_params']['TAG_OR_BRANCH'] = tag_or_branch
        domain = project_info.get(deploy_env).get('domain')

        # 存在其他依赖项目，则递归发布
        if depends:
            await deploy([depends], webhook=webhook)

        # 调用jks发布代码
        if jks_job_name:
            res1 = await JksOp.build_job(config.jks_url, config.jks_user, config.jks_password, jks_job_name, jks_params)
            msg_list.append(res1.get('msg'))

        # domain存在则刷新cdn缓存
        if domain:
            await ref(alias_name, deploy_env, webhook=webhook, domain=domain)
        try:
            # 写入数据库
            conn = MysqlToDo.conn(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_passwd, config.mysql_db)
            sql = f"INSERT INTO `version_info`(`alias_name`,`deploy_env`,`tag_or_branch`,`deploy_time`) VALUES ('{alias_name}','{deploy_env}','{tag_or_branch}', '{deploy_time}');"
            MysqlToDo.sql_exec(conn, sql)
        except Exception as e:
            msg = f'项目:{alias_name}发布信息入库失败，原因:{e}'
            msg_list.append(msg)
    msg_md = "\n".join(msg_list)
    msgs = "# 反馈信息   \n  ---  \n ## 详情  \n%s" % msg_md
    await SendMessage.send_md(webhook, msgs)
