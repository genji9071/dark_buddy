from lib.chatbot import DingtalkChatbot


# 机器人注册dict，通过chatbotUserId检索
chatbots = {
    '$:LWCP_v1:$6iRUp4hKVVJEmAJ7eGz0Z2q8GValTmK1': DingtalkChatbot(
        webhook='https://oapi.dingtalk.com/robot/send?access_token=7564dc16675742466558f1f005770dfb8b831bce53849bc7af8583ce14fbef79'),
    '$:LWCP_v1:$cOvG5lU9DJwzki6nr0awqScNCVQUM1o4': DingtalkChatbot(
        webhook='https://oapi.dingtalk.com/robot/send?access_token=3cddb5405350c32a688c6a51d6151c11db8f8767410731c2bbdaee75dfaaa31a'),
    '$:LWCP_v1:$JS+tN5ZeAGnF/xrtw0wd5olE2WwhNQ1Y': DingtalkChatbot(
        webhook='https://oapi.dingtalk.com/robot/send?access_token=39039504f38252257c5755dbbd310546f89741277d4cf7d8251a89df02a0064e')
}

# 租户信息
tenant_base_info = {
    't1': {
        'chatbotUserId': '$:LWCP_v1:$cOvG5lU9DJwzki6nr0awqScNCVQUM1o4',
        'description': '最开始的租户，里面有很多人。',
        'tenant_group_name': '暗黑',
        'isExternal': False
    },
    't2': {
        'chatbotUserId': '$:LWCP_v1:$6iRUp4hKVVJEmAJ7eGz0Z2q8GValTmK1',
        'description': '湖畔大学外围粉丝团，包含核心开发，属于调试功能用租户。',
        'tenant_group_name': '湖畔大学外围粉丝团',
        'isExternal': False
    },
    't3': {
        'chatbotUserId': '$:LWCP_v1:$JS+tN5ZeAGnF/xrtw0wd5olE2WwhNQ1Y',
        'description': '钉钉更新的第一个外部租户。',
        'tenant_group_name': '暗黑小哥的一小步',
        'isExternal': True
    }
}