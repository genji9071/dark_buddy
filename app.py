# coding=utf-8
import os
import traceback
from functools import wraps
from io import BytesIO
from multiprocessing import Process

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, request, make_response, send_from_directory
from flask.json import jsonify, _json
from flask_cors import CORS

import mapper
from config.ChatbotsConfig import chatbots
from dark_chat.DarkChat import dark_chat
from dark_chat.dark_jikipedia.DarkJiWordCloud import dark_ji_word_cloud
from dark_listener.DarkListener import dark_listeners
from dark_maze.DarkMaze import dark_maze
from dark_menu.DarkMenu import dark_menu
from dark_spy.DarkSpy import dark_spy
from dark_word_cloud.DarkWordCloud import dark_word_cloud
from lib.ImageFactory import image_factory
from lib.Logger import log
from lib.ResponseLib import response_lib
from lib.chatbot import ActionCard, CardItem
from user.login.User_login import user_login

app = Flask(__name__, static_url_path="")
cors = CORS(app, resources={r"*": {"origins": "*"}})
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


def image_control_allow(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        response = make_response(fun(*args, **kwargs))
        response.headers['Content-Type'] = 'image/png'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = 86400
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'service-name, api-name, X-User-Id, X-Token, X-Top-User-Id, X-Top-Token, X-Requested-With, Access-Control-Allow-Origin, X-HTTP-Method-Override, Content-Type, Authorization, Accept'
        return response

    return wrapper_fun


def capture_by_listener(request_json):
    return dark_listeners.listen(request_json)


def do_request(request_json):
    founded_user = user_login.login(request_json)
    if founded_user:
        bibi = False
        bibi = do_dark_debug(request_json) or bibi
        if not bibi and not capture_by_listener(request_json):
            # 进入自动逼逼环节
            user_login.record_words(request_json['text']['content'], founded_user.get('id'))
            dark_chat.do_dark_chat(request_json)

def do_listener(json_object):
    name = json_object['name']
    message = json_object['message']
    founded_user = mapper.mapper_user.select_by_name(name.strip())
    if founded_user is None:
        pass
    user_login.record_words(message, founded_user.id)
    pass


def run_schedule_task():
    timez = pytz.timezone('Asia/Shanghai')
    scheduler = BlockingScheduler(timezone=timez)
    if hasattr(os, 'getppid'):  # only available on Unix
        print('parent process:', os.getppid())
    print('process id:', os.getpid())
    scheduler.start()


@app.route('/dark_buddy', methods=['POST', 'OPTIONS', 'GET'])
@control_allow
def dark_buddy():
    try:
        if request.method == 'OPTIONS':
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'POST':
            json_object = request.json
            log.info(_json.dumps(json_object, indent=4))
            do_request(json_object)
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'GET':
            log.error('Why you got GET method?')
            log.info(request)
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        chatbots.get(request.json['chatbotUserId']
                     ).send_text(traceback.format_exc())
        return response


@app.route('/dark_buddy/listener', methods=['POST', 'OPTIONS'])
@control_allow
def dark_buddy_listener():
    try:
        if request.method == 'OPTIONS':
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'POST':
            json_object = request.json
            log.info(_json.dumps(json_object, indent=4))
            do_listener(json_object)
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response


@app.route('/dark_buddy/dark_maze/image/get', methods=['GET'])
@image_control_allow
def dark_maze_image_get():
    try:
        f = BytesIO()
        chatbotUserId = request.values.get('session_id')
        image = dark_maze.get_maze_image(chatbotUserId)
        image.save(f, 'png')
        return f.getvalue()
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response


@app.route('/dark_buddy/image/get', methods=['GET'])
@image_control_allow
def image_get():
    try:
        f = BytesIO()
        chatbotUserId = request.values.get('session_id')
        uuid = request.values.get('uuid')
        file_suffix = request.values.get('file_suffix', 'png')
        image = image_factory.get_image_by_uuid(uuid)
        if image is None:
            return None
        image.save(f, file_suffix)
        return f.getvalue()
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response


@app.route('/dark_buddy/dark_word_cloud/image/get', methods=['GET'])
@image_control_allow
def dark_word_cloud_image_get():
    try:
        f = BytesIO()
        file_suffix = request.values.get('file_suffix', 'png')
        image = dark_word_cloud.get_image()
        image.save(f, file_suffix)
        return f.getvalue()
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response


@app.route('/dark_buddy/dark_ji_word_cloud/image/get', methods=['GET'])
@image_control_allow
def dark_ji_word_cloud_image_get():
    try:
        f = BytesIO()
        file_suffix = request.values.get('file_suffix', 'png')
        image = dark_ji_word_cloud.get_image()
        image.save(f, file_suffix)
        return f.getvalue()
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response


@app.route('/dark_buddy/sign_in/check_lock', methods=['POST', 'OPTIONS'])
@control_allow
def sign_in():
    try:
        if request.method == 'OPTIONS':
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'POST':
            json_object = request.json
            log.info(_json.dumps(json_object, indent=4))
            sender_id = json_object['sender_id']
            if user_login.check_lock(sender_id):
                return jsonify(response_lib.SUCCESS_CODE)
            else:
                return jsonify(response_lib.ERROR_CODE)

    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response

@app.route('/dark_buddy/sign_in/get_signature_by_url', methods=['POST', 'OPTIONS'])
@control_allow
def get_signature_by_url():
    try:
        if request.method == 'OPTIONS':
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'POST':
            json_object = request.json
            log.info(_json.dumps(json_object, indent=4))
            url = json_object['url']
            return get_url_signature(url)
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response

@app.route('/dark_buddy/darkSpy/getWord', methods=['POST', 'OPTIONS'])
@control_allow
def darkSpyGetWord():
    try:
        if request.method == 'OPTIONS':
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'POST':
            json_object = request.json
            log.info(_json.dumps(json_object, indent=4))
            return dark_spy.show_gamer_info(json_object)
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response


@app.route("/dark_buddy/static/<path:path>")
def static_get(path):
    web_root = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "web/build/static"
    )
    return send_from_directory(web_root, path)


@app.route("/dark_buddy/web", defaults={'path': ''})
@app.route("/dark_buddy/web/<path:path>")
def web_get(path):
    web_root = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "web/build"
    )
    response = send_from_directory(web_root, "index.html")
    response.headers["Cache-Control"] = "no-cache"
    return response


def do_dark_debug(json):
    return dark_menu.call_api(json)

if __name__ == '__main__':
    p = Process(target=run_schedule_task)
    p.start()
    for chatbot in chatbots.values():
        chatbot.send_action_card(ActionCard(
            title="最近更新",
            text="### 最近更新\n- 暗黑梭哈内测版（不花钱）\n- 暗黑日报优化显示格式，新增入职日期/工号/部门/职位，可重复召唤",
            btns=[CardItem(
                title="点击开始体验", url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑梭哈")]
        ))
    app.run("0.0.0.0", port=9000, debug=False, threaded=True)
