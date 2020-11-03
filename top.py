# coding=utf-8
import os
import traceback
from functools import wraps

from flask import Flask, make_response, request, jsonify

from config.ChatbotsConfig import chatbots
from lib.Logger import log
from lib.ResponseLib import response_lib

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def control_allow(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        response = make_response(fun(*args, **kwargs))
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = 86400
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'service-name, api-name, X-User-Id, X-Token, X-Top-User-Id, X-Top-Token, X-Requested-With, Access-Control-Allow-Origin, X-HTTP-Method-Override, Content-Type, Authorization, Accept'
        return response

    return wrapper_fun


def do_fetch():
    for chatbot in chatbots.values():
        chatbot.send_text("我要开始裂开了，期间请不要和我说话 ")
    os.chdir("/data/User/tianhao/Dark_buddy")
    log.info("Dark buddy helper starts to set the config...")
    os.system("git config --global credential.helper.store --file /data/User/tianhao/git-credentials/global.gitcredentials")
    # os.system("yum install -y lsof")
    # os.system("yum install -y net-tools")
    # os.system("yum install tk-devel")
    log.info("Dark buddy helper starts to pull codes...")
    os.system("git pull")
    log.info("Dark buddy helper starts to shut down the service...")
    try:
        # os.system("ps -ef | grep `netstat -nlp | grep :9000 | awk '{print $7}' | awk -F / '{ print $1 }'` | awk '{print $2}' | xargs kill -9")
        os.system(
            "ps -ef | grep 'python -u app.py' | awk '{print $2}' | xargs kill -9")
    except:
        log.info("Dark buddy helper doesn't find the old service...")
    log.info("Dark buddy helper starts to install the pip...")
    # os.system("pip config set install.trusted-host mirrors.aliyun.com")
    # os.system("pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/")
    # os.system("pip install -r requirements.txt")
    log.info("Dark buddy helper starts to up the service...")
    os.system("nohup python -u app.py > app.log 2>&1 &")
    log.info("Dark buddy helper makes everything well done!")
    pass


@app.route('/webhook', methods=['POST', 'OPTIONS'])
@control_allow
def parse_request():
    try:
        if request.method == 'OPTIONS':
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'POST':
            do_fetch()
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response

if __name__ == '__main__':
    app.run("0.0.0.0", port=32021, debug=False, threaded=True)