# coding: utf8

async def hello(*args, **kwargs):
    print('hello,您可以在此函数定义要执行的操作')
    print('异步执行完成')
    return {'errCode': 0, 'msg': 'hello world!'}
