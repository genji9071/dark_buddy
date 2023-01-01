# coding=utf-8
import json
import os
import traceback
from functools import wraps
from io import BytesIO

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, request, make_response, send_from_directory
from flask.json import jsonify
from flask_cors import CORS

from config.ChatbotsConfig import chatbots
from config.ThreadLocalSource import dark_local
from dark_chat.DarkChat import dark_chat
from dark_chat.dark_jikipedia.DarkJiWordCloud import dark_ji_word_cloud
from dark_live_chat import socketio
from dark_live_chat.DarkLiveChat4Socket import init_dark_live_chat_event, capture_by_listener
from dark_maze.DarkMaze import get_maze_image
from dark_menu.DarkMenu import dark_menu
from dark_spy.DarkSpy import dark_spy
from dark_word_cloud.DarkWordCloud import dark_word_cloud
from lib.Logger import log, socketio_log
from lib.ResponseLib import response_lib
from mapper.DarkBuddyUser import select_by_name
from user.login.User_login import user_login

app = Flask(__name__, static_url_path="")
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['JSON_AS_ASCII'] = False


#
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
    founded_user = select_by_name(name.strip())
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


def convert_feishu_json_and_do_request(json_object):
    if 'event' in json_object:
        result = {
            "senderId": json_object.get('event').get("user_open_id"),
            "senderNick": "Unknown user",
            "chatbotUserId": json_object.get('event').get("app_id"),
            "text": {
                "content": json_object.get('event').get("text_without_at_bot", "")
            }
        }
        dark_local.receive_info = {
            'call_type': 'send',
            'receive_id_type': 'chat_id',
            'receive_id': json_object.get('event').get("open_chat_id")
        }
    else:
        result = {
            "senderId": json_object.get("open_id"),
            "senderNick": "Unknown user",
            "chatbotUserId": "cli_a06c6d4a3d799013",
            "text": {
                "content": json_object.get('action').get("option", "")
            }
        }
        dark_local.receive_info = {
            'call_type': 'reply',
            'receive_id_type': 'message_id',
            'receive_id': json_object.get("open_message_id")
        }
    return do_request(result)


@app.route('/feishu', methods=['POST', 'OPTIONS', 'GET'])
@control_allow
def feishu():
    try:
        if request.method == 'OPTIONS':
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'POST':
            json_object = request.json
            log.info(json.dumps(json_object, indent=4, ensure_ascii=False))
            # do verification
            if json_object.get('type') == "url_verification":
                return json_object
            socketio.start_background_task(target=convert_feishu_json_and_do_request, json_object=json_object)
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
        return response


@app.route('/wechat', methods=['GET'])
@control_allow
def wechat():
    try:
        if request.method == 'GET':
            params = request.values
            return params['echostr']
    except:
        log.error(traceback.format_exc())
        response = jsonify(response_lib.ERROR_CODE)
        return response


@app.route('/dark_buddy', methods=['POST', 'OPTIONS', 'GET'])
@control_allow
def dark_buddy():
    try:
        if request.method == 'OPTIONS':
            response = jsonify(response_lib.SUCCESS_CODE)
            return response
        if request.method == 'POST':
            json_object = request.json
            log.info(json.dumps(json_object, indent=4, ensure_ascii=False))
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
            log.info(json.dumps(json_object, indent=4, ensure_ascii=False))
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
        image = get_maze_image(chatbotUserId)
        image.save(f, 'png')
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
            log.info(json.dumps(json_object, indent=4, ensure_ascii=False))
            sender_id = json_object['sender_id']
            if user_login.check_lock(sender_id):
                return jsonify(response_lib.SUCCESS_CODE)
            else:
                return jsonify(response_lib.ERROR_CODE)

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
            log.info(json.dumps(json_object, indent=4, ensure_ascii=False))
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
    init_dark_live_chat_event()
    socketio.init_app(app, logger=socketio_log)
    socketio.run(app, "0.0.0.0", port=9000, debug=True)
