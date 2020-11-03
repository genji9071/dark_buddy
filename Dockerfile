FROM python:3.7

WORKDIR /DarkDing/

MAINTAINER zhangtianhao@tezign.com

USER root

COPY requirements.txt /DarkDing/
#RUN pip3 install pip3 -U -i https://mirrors.huaweicloud.com/repository/pypi/simple/
RUN pip3 config set global.index-url https://mirrors.huaweicloud.com/repository/pypi/simple/
#RUN pip3 install --upgrade ndg-httpsclient -i https://mirrors.huaweicloud.com/repository/pypi/simple/
#RUN pip3 install -r requirements.txt -i https://mirrors.huaweicloud.com/repository/pypi/simple/
#RUN pip3 install --upgrade ndg-httpsclient
RUN pip3 install -r requirements.txt

COPY . /DarkDing/

EXPOSE 9000

ENTRYPOINT python app.py

#docker run -ti -d --name darkrobot -p 9000:9000 darkrobot:0.0.3

#ssh root@202.182.127.23

#docker run -p 8080:8080 -p 50000:50000 -v /home/docker/jenkins:/var/jenkins_home -d --restart=always  jenkinsci/jenkins