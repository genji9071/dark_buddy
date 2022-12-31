FROM python:3.8

WORKDIR /DarkBuddy/

MAINTAINER 615882479@qq.com

USER root

COPY requirements.txt /DarkBuddy/
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install -r requirements.txt

COPY . /DarkBuddy/

EXPOSE 8080

ENTRYPOINT python app.py
