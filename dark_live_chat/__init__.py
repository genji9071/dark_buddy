from flask_socketio import SocketIO

socketio = SocketIO(async_mode="eventlet", cors_allowed_origins=[])

namespace = '/dark_live_chat'
message_event_name = 'message'
connect_event_name = 'connect'
disconnect_event_name = 'disconnect'
