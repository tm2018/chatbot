# coding: utf8
import requests_async as requests
import jenkins
import gitlab


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


# 调用jenkins
class JenkinsOp(object):
    @staticmethod
    async def build_job(url, username, password, jenkins_job_name, data):
        try:
            server = jenkins.Jenkins(url, username=username, password=password)
            server.build_job(jenkins_job_name, parameters=data)
            return {'errCode': 0, 'msg': '项目:%s调用jenkins任务成功，请等待。' % jenkins_job_name}
        except Exception as e:
            return {'errCode': 503, 'msg': '项目:%s调用jenkins失败，原因:%s。' % (jenkins_job_name, e)}


# gitlab相关操作
class GitlabOp(object):
    @classmethod
    def gitlab_conn(cls, url,private_token):
        # 连接gitlab
        gl = gitlab.Gitlab(url, private_token=private_token)
        return gl

    @classmethod
    def get_project_info(cls, conn):
        # 获取项目路径和id，返回dict
        res = {}
        infos = conn.projects.list(all=True, as_list=False)
        for p in infos:
            res[p.path_with_namespace] = p.id
        return res

    # 合并请求
    @classmethod
    def merge_requests(cls, conn, name_space, project_name, target_branch):
        if name_space:
            path_with_namespace = '%s/%s' %(name_space, project_name)
        else:
            path_with_namespace = project_name

        # 获取项目id，不存在则返回404
        project_info = cls.get_project_info(conn)
        project_id = project_info.get(path_with_namespace, '')
        if not project_id:
            return {"errCode": 404, "msg": "获取project_id失败，请检查项目:%s是否存在!" % (project_name)}

        project_id = project_info.get(path_with_namespace)
        project = conn.projects.get(project_id)
        mrs = project.mergerequests.list(state='opened', order_by='created_at', sort='desc')
        if not len(mrs):
            return {"errCode": 404, "msg": "项目:%s无合并请求，请关注!" %(project_name)}

        merge_infos = mrs[0]
        # 只合并目标分支为target_branch的请求
        if merge_infos.target_branch != target_branch:
            return {"errCode": 403, "msg": "非授权分支:%s，放弃合并！" %(merge_infos.target_branch)}

        # 根据iid合并
        mr = project.mergerequests.get(merge_infos.iid)
        mr.merge()
        return {"errCode": 0, "msg": "项目：%s,分支:%s合并完成，准备发布中" %(project_name, merge_infos.target_branch)}
