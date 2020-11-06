from flask import g

from config import redis


def exception_message(data):
    return {
        "msgtype": "exception",
        "message": data
    }


def get_live_chat_response():
    session_id = g.session_id
    row_data = redis.get(get_dark_live_chat_session_name(session_id))
    if not row_data:
        return {"result": [exception_message("结果没有找到，请联系作者。")]}
    data = eval(row_data.decode())
    redis.delete(get_dark_live_chat_session_name(session_id))
    result = []
    for message in data:
        result.append(eval(message))
    return {"result": result}


def put_live_chat_response(data):
    session_id = g.session_id
    row_data = redis.get(get_dark_live_chat_session_name(session_id))
    if not row_data:
        redis.setex(name=get_dark_live_chat_session_name(session_id), time=60,
                    value=str([data]))
    else:
        existed_data = eval(row_data.decode())
        existed_data.append(data)
        redis.setex(name=get_dark_live_chat_session_name(session_id), time=60,
                    value=str(existed_data))
    return


def get_dark_live_chat_session_name(session_id):
    return 'tianhao:dark_buddy:dark_live_chat:{0}'.format(session_id)
