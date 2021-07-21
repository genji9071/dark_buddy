from config.ManuConfig import default_menu, live_chat_menu, feishu_menu

# 租户信息
tenant_base_info = {
    '$:LWCP_v1:$cOvG5lU9DJwzki6nr0awqScNCVQUM1o4': {
        'chatbotUserId': '$:LWCP_v1:$cOvG5lU9DJwzki6nr0awqScNCVQUM1o4',
        'description': '最开始的租户，里面有很多人。',
        'tenant_group_name': '暗黑',
        'isExternal': False,
        'menu': default_menu
    },
    '$:LWCP_v1:$6iRUp4hKVVJEmAJ7eGz0Z2q8GValTmK1': {
        'chatbotUserId': '$:LWCP_v1:$6iRUp4hKVVJEmAJ7eGz0Z2q8GValTmK1',
        'description': '湖畔大学外围粉丝团，包含核心开发，属于调试功能用租户。',
        'tenant_group_name': '湖畔大学外围粉丝团',
        'isExternal': False,
        'menu': default_menu
    },
    '$:LWCP_v1:$JS+tN5ZeAGnF/xrtw0wd5olE2WwhNQ1Y': {
        'chatbotUserId': '$:LWCP_v1:$JS+tN5ZeAGnF/xrtw0wd5olE2WwhNQ1Y',
        'description': '钉钉更新的第一个外部租户。',
        'tenant_group_name': '暗黑小哥的一小步',
        'isExternal': False,
        'menu': default_menu
    },
    'live_chat_chatbotUserId': {
        'chatbotUserId': 'live_chat_chatbotUserId',
        'description': 'www.darkbuddy.cn',
        'tenant_group_name': 'www.darkbuddy.cn',
        'isExternal': True,
        'menu': live_chat_menu
    },

    'cli_a06c6d4a3d799013': {
        'chatbotUserId': 'cli_a06c6d4a3d799013',
        'description': '飞书的内容应用群机器人',
        'tenant_group_name': 'Tezign内容应用',
        'isExternal': False,
        'menu': feishu_menu
    }

}
