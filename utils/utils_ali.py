# coding: utf8

from Tea.core import TeaCore
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_dcdn20180115.client import Client as dcdn20180115Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dcdn20180115 import models as dcdn_20180115_models

import json
# ecs安全组规则添加
class EcsRulesOp(object):
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Ecs20140526Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'ecs.cn-shanghai.aliyuncs.com'
        return Ecs20140526Client(config)

    # 获取安全组规则
    @staticmethod
    def get_rules_in(
            client,
            **data
    ):
        # print(data)
        # client = EcsRulesOp.create_client(access_key_id, access_key_secret)
        describe_security_group_attribute_request = ecs_20140526_models.DescribeSecurityGroupAttributeRequest(
            security_group_id=data.get('security_group_id'),
            region_id=data.get('region_id')
        )
        # 复制代码运行请自行打印 API 的返回值
        res = client.describe_security_group_attribute(describe_security_group_attribute_request).body.to_map()
        # print(res)
        return res['Permissions'].get('Permission')

    # 增加安全组规则
    @staticmethod
    def add_rules_in(
            client,
            **data
    ) -> None:
        # client = EcsRulesOp.create_client(access_key_id, access_key_secret)
        region_id = data.get('region_id')
        security_group_id = data.get('security_group_id')
        ip_protocol = data.get('ip_protocol', 'tcp')
        port_range = data.get('port_range')
        source_cidr_ip = data.get('source_cidr_ip')
        description = data.get('description', 'devops自动添加')

        authorize_security_group_request = ecs_20140526_models.AuthorizeSecurityGroupRequest(
            region_id=region_id,
            security_group_id=security_group_id,
            ip_protocol=ip_protocol,
            port_range=port_range,
            source_cidr_ip=source_cidr_ip,
            description=description
        )
        resp = client.authorize_security_group(authorize_security_group_request)
        ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))

    # 撤销安全组规则
    @staticmethod
    def revoke_rules_in(
            client,
            **data
    ):
        # 定义撤销规则的数据，格式为dict
        # 其中region_id和security_group_id和查询的完全一致
        revoke_data = {}
        revoke_data['region_id'] = data.get('region_id')
        revoke_data['security_group_id'] = data.get('security_group_id')
        res_rules_in = EcsRulesOp.get_rules_in(client, **data)
        print(res_rules_in)

        # 循环删除规则，注意，会删除安全组下所有规则
        for rule in res_rules_in:
            revoke_data['port_range'] = rule.get('PortRange')
            revoke_data['ip_protocol'] = rule.get('IpProtocol')
            revoke_data['source_cidr_ip'] = rule.get('SourceCidrIp')
            revoke_security_group_request = ecs_20140526_models.RevokeSecurityGroupRequest(
                **revoke_data
            )

            # 执行删除动作
            client.revoke_security_group(revoke_security_group_request)

# 刷新cdn缓存
class RefreshDcdn:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> dcdn20180115Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'dcdn.aliyuncs.com'
        return dcdn20180115Client(config)

    @staticmethod
    def refresh_dcdn(
        access_key_id: str,
        access_key_secret: str,
        object_path: str,
        object_type='file'
    ) -> None:

        client = RefreshDcdn.create_client(access_key_id, access_key_secret)
        refresh_dcdn_object_caches_request = dcdn_20180115_models.RefreshDcdnObjectCachesRequest(
            object_path=object_path,
            object_type=object_type
        )
        # 复制代码运行请自行打印 API 的返回值
        client.refresh_dcdn_object_caches(refresh_dcdn_object_caches_request)
