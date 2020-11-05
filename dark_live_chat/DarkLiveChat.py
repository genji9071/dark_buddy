from config import redis


def exception_message(data):
    return {
        "msgtype": "exception",
        "message": data
    }


def get_live_chat_response(request_json):
    session_id = request_json['chatbotUserId']
    row_data = redis.get(get_dark_live_chat_session_name(session_id))
    if not row_data:
        return exception_message("结果没有找到，请联系作者。")
    data = eval(row_data.decode())
    redis.delete(get_dark_live_chat_session_name(session_id))
    return data


def put_live_chat_response(data, session_id):
    redis.setex(name=get_dark_live_chat_session_name(session_id), time=30,
                value=str(data))
    return


def get_dark_live_chat_session_name(session_id):
    return 'tianhao:dark_buddy:dark_live_chat:{0}'.format(session_id)
