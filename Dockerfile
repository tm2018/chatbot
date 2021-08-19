FROM python:3.9.6-alpine3.14

WORKDIR /opt/

ADD . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["sh","/opt/entrypoint.sh"]
