from lib.DingtalkChatbot import DingtalkChatbot

# 机器人注册dict，通过chatbotUserId检索
from lib.FeishuChatbot import FeishuChatbot


class ChatbotsConfig():
    def __init__(self):
        self.chatbot_map = {
            'dingding': {
                '$:LWCP_v1:$6iRUp4hKVVJEmAJ7eGz0Z2q8GValTmK1': DingtalkChatbot(
                    webhook='https://oapi.dingtalk.com/robot/send?access_token=7564dc16675742466558f1f005770dfb8b831bce53849bc7af8583ce14fbef79'),
                '$:LWCP_v1:$cOvG5lU9DJwzki6nr0awqScNCVQUM1o4': DingtalkChatbot(
                    webhook='https://oapi.dingtalk.com/robot/send?access_token=3cddb5405350c32a688c6a51d6151c11db8f8767410731c2bbdaee75dfaaa31a'),
                '$:LWCP_v1:$JS+tN5ZeAGnF/xrtw0wd5olE2WwhNQ1Y': DingtalkChatbot(
                    webhook='https://oapi.dingtalk.com/robot/send?access_token=39039504f38252257c5755dbbd310546f89741277d4cf7d8251a89df02a0064e'),
            },
            'live_chat': {
                'live_chat_chatbotUserId': DingtalkChatbot(webhook='live_chat', is_live_chat=True),
            },
            'feishu': {
                'cli_a06c6d4a3d799013': FeishuChatbot()
            },
        }

    def get(self, key):
        from config.TenantConfig import tenant_base_info
        tenant_info = tenant_base_info.get(key)
        platform_type = tenant_info.get('platformType')
        if platform_type == 'feishu':
            return self.chatbot_map.get(platform_type)['cli_a06c6d4a3d799013']
        else:
            return self.chatbot_map.get(platform_type)[key]


chatbots = ChatbotsConfig()
