# 基于钉钉企业内部机器人开发的聊天机器人
## 项目描述
```angular2html
基于flask开发的钉钉企业内部机器人，通过命令进行交互，后端执行预定义的操作。

目前项目用于自动化运维，具体功能如下所述，更多功能等待完善
```
## 功能说明
* 刷新cdn（阿里云）缓存
* 添加/删除云（阿里云）安全组规则
* 版本发布
* 
## 使用方式
#### 一、创建钉钉机器人
###### 1.登录钉钉开发者后台
```angular2html
访问网站 https://open-dev.dingtalk.com/#/，登录到钉钉后台
PS： 需要具备企业管理员权限
```
###### 2.创建机器人
```angular2html
点击"应用开发"-"企业内部开发"，进入页面后点击左侧菜单"机器人"，添加钉钉机器人

填好相关信息完成创建
```
###### 3.获取AppSecret
```angular2html
点击"基础信息"，获取到AppSecret
```
#### 二、启动项目
##### 2.1 修改配置

```angular2html
# cp -a env.example env
...
# 
FLASK_ENV=development
chatbot_env=dev
...

# vim config/settings.py 
修改APP_SECRET为1.3获取到的AppSecret
修改APP_SECRET为1.3获取到的AppSecret
```
#### 三、构建和启动
```
# docker-compose build
# docker-compose up -d
```
#### 四、配置机器人
```angular2html
按照步骤一登录机器人后台，进入机器人配置界面，点击"开发管理"，配置服务器

服务器出口IP：ip
消息接收地址：http://ip:9998
```

#### 五、测试
###### 5.1 添加机器人
```angular2html
在钉钉群中，添加”群设置“-”智能群助手“-”添加机器人“，找到企业机器人并添加到群中
```
###### 5.2 测试
```angular2html
在群里艾特机器人并输入指令
@机器人 help

```
