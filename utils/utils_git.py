# coding: utf8

import gitlab


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
        try:
            if name_space:
                path_with_namespace = '%s/%s' %(name_space, project_name)
            else:
                path_with_namespace = project_name

            # 获取项目id，不存在则返回404
            project_info = cls.get_project_info(conn)
            project_id = project_info.get(path_with_namespace, '')
            if not project_id:
                return {"errCode": 404, "msg": "获取project_id失败，请检查项目:%s是否存在!\n" % (project_name)}

            project_id = project_info.get(path_with_namespace)
            project = conn.projects.get(project_id)
            mrs = project.mergerequests.list(state='opened', order_by='created_at', sort='desc')
            if not len(mrs):
                return {"errCode": 404, "msg": "项目:%s无合并请求，请关注!\n" %(project_name)}

            merge_infos = mrs[0]
            # 只合并目标分支为target_branch的请求
            if merge_infos.target_branch != target_branch:
                return {"errCode": 403, "msg": "非授权分支:%s，放弃合并！\n" %(merge_infos.target_branch)}

            # 根据iid合并
            mr = project.mergerequests.get(merge_infos.iid)
            mr.merge()
            return {"errCode": 200, "msg": "项目：%s,分支:%s合并完成，继续发布...\n" % (project_name, merge_infos.target_branch)}
        except Exception as e:
            return {"errCode": 500, "msg": "项目：%s,目标分支:%s合并出错，原因:%s\n" % (project_name, target_branch, e)}
