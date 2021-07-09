import os

from larksuiteoapi import Config, ACCESS_TOKEN_TYPE_TENANT, DOMAIN_LARK_SUITE, DefaultLogger, LEVEL_DEBUG
from larksuiteoapi.api import Request, set_timeout

from lib.BaseChatbot import BaseChatbot, ActionCard

feishu_app_id = os.environ.get("FEISHU_APP_ID")
feishu_app_secret = os.environ.get("FEISHU_APP_SECRET")
feishu_app_verification_token = os.environ.get("FEISHU_VERIFICATION_TOKEN")
feishu_app_encrypt_key = os.environ.get("FEISHU_APP_ENCRYPT_KEY")


class FeishuChatbot(BaseChatbot):

    def __init__(self, receive_id):
        self.receive_id = receive_id
        self.app_settings = Config.new_internal_app_settings(feishu_app_id, feishu_app_secret,
                                                             feishu_app_verification_token, feishu_app_encrypt_key)
        # Currently, you are visiting larksuite, which uses default storage and default log (debug level). More optional configurations are as follows: README.md->Advanced use->How to build overall configuration(Config)。
        self.conf = Config.new_config_with_memory_store(DOMAIN_LARK_SUITE, self.app_settings, DefaultLogger(),
                                                        LEVEL_DEBUG)

    def send_text(self, msg, is_at_all=False, at_mobiles=[], at_dingtalk_ids=[]):
        body = {
            'receive_id': self.receive_id,
            'content': {
                'text': msg
            },
            'msg_type': 'text'

        }
        req = Request('im/v1/messages', 'POST', ACCESS_TOKEN_TYPE_TENANT, body, request_opts=[set_timeout(3)])
        resp = req.do(self.conf)
        print('request id = %s' % resp.get_request_id())
        print(resp.code)
        if resp.code == 0:
            print(resp.data)
        else:
            print(resp.msg)
            print(resp.error)

    def send_image(self, pic_url):
        pass

    def send_markdown(self, title, text, is_at_all=False, at_mobiles=[], at_dingtalk_ids=[]):
        pass

    def send_action_card(self, action_card: ActionCard):
        pass

    def send_feed_card(self, links):
        pass
