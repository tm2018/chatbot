FROM python:3.9.7

WORKDIR /opt/


ADD ./sources.list /etc/apt/sources.list
ADD ./requirements.txt .


RUN echo "Asia/shanghai" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime \
    && apt update \
    && apt install gcc \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . .

ENTRYPOINT ["sh","/opt/entrypoint.sh"]

