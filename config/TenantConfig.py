from config.ManuConfig import default_menu, live_chat_menu, feishu_menu

# 租户信息
tenant_base_info = {
    '$:LWCP_v1:$cOvG5lU9DJwzki6nr0awqScNCVQUM1o4': {
        'platformType': "dingding",
        'chatbotUserId': '$:LWCP_v1:$cOvG5lU9DJwzki6nr0awqScNCVQUM1o4',
        'description': '最开始的租户，里面有很多人。',
        'tenant_group_name': '暗黑',
        'isExternal': False,
        'menu': default_menu
    },
    '$:LWCP_v1:$6iRUp4hKVVJEmAJ7eGz0Z2q8GValTmK1': {
        'platformType': "dingding",
        'chatbotUserId': '$:LWCP_v1:$6iRUp4hKVVJEmAJ7eGz0Z2q8GValTmK1',
        'description': '湖畔大学外围粉丝团，包含核心开发，属于调试功能用租户。',
        'tenant_group_name': '湖畔大学外围粉丝团',
        'isExternal': False,
        'menu': default_menu
    },
    '$:LWCP_v1:$JS+tN5ZeAGnF/xrtw0wd5olE2WwhNQ1Y': {
        'platformType': "dingding",
        'chatbotUserId': '$:LWCP_v1:$JS+tN5ZeAGnF/xrtw0wd5olE2WwhNQ1Y',
        'description': '钉钉更新的第一个外部租户。',
        'tenant_group_name': '暗黑小哥的一小步',
        'isExternal': False,
        'menu': default_menu
    },
    'live_chat_chatbotUserId': {
        'platformType': "live_chat",
        'chatbotUserId': 'live_chat_chatbotUserId',
        'description': 'www.darkbuddy.cn',
        'tenant_group_name': 'www.darkbuddy.cn',
        'isExternal': True,
        'menu': live_chat_menu
    },
}
