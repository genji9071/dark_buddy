from flask import g, request
from flask_socketio import join_room

from dark_chat.DarkChat import dark_chat
from dark_listener.DarkListener import dark_listeners
from dark_live_chat import socketio, namespace
from dark_menu.DarkMenu import dark_menu

rooms = {}


def init_dark_live_chat_event():
    @socketio.on('join room', namespace=namespace)
    def on_join():
        print("on_join, session_id: {0}".format(request.sid))
        join_room(request.sid)

    @socketio.on('connect', namespace=namespace)
    def on_connect():
        print('Client connected')

    @socketio.on('disconnect', namespace=namespace)
    def on_disconnect():
        print('Client disconnected')

    @socketio.on('message', namespace=namespace)
    def on_say_a_word(data):
        do_live_chat_request(data)


def do_live_chat_request(request_json):
    g.session_id = request.sid
    bibi = False
    bibi = dark_menu.call_api(request_json) or bibi
    if not bibi and not dark_listeners.listen(request_json):
        # 进入自动逼逼环节
        dark_chat.do_dark_chat(request_json)
