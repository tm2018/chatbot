# coding: utf8

import jenkins


# 调用jenkins
class JksOp(object):
    @staticmethod
    async def build_job(url, username, password, jenkins_job_name, data):
        try:
            server = jenkins.Jenkins(url, username=username, password=password)
            server.build_job(jenkins_job_name, parameters=data)
            return {'errCode': 0, 'msg': '项目:%s调用jenkins任务成功，请等待。\n' % jenkins_job_name}
        except Exception as e:
            return {'errCode': 503, 'msg': '项目:%s调用jenkins失败，原因:%s。\n' % (jenkins_job_name, e)}
