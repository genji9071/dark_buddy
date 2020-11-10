from flask import session

from dark_live_chat import socketio


def init_dark_live_chat_event():
    @socketio.on('join')
    def on_join(data):
        username = session['username']
        room = data['room']
        socketio.join_room(room)
        socketio.send(username + ' has entered the room.', room=room)

    @socketio.on('leave')
    def on_leave(data):
        username = session['username']
        room = data['room']
        socketio.leave_room(room)
        socketio.send(username + ' has left the room.', room=room)
