import os

from flask.json import _json
from larksuiteoapi import Config, ACCESS_TOKEN_TYPE_TENANT, DOMAIN_LARK_SUITE, DefaultLogger, LEVEL_DEBUG
from larksuiteoapi.api import Request, set_timeout

from config.EnvConfig import env_config
from config.ThreadLocalSource import dark_local
from lib.BaseChatbot import BaseChatbot, ActionCard
from lib.Logger import log

feishu_app_id = os.environ.get("FEISHU_APP_ID")
feishu_app_secret = os.environ.get("FEISHU_APP_SECRET")
feishu_app_verification_token = os.environ.get("FEISHU_VERIFICATION_TOKEN")
feishu_app_encrypt_key = os.environ.get("FEISHU_APP_ENCRYPT_KEY")


class FeishuChatbot(BaseChatbot):

    def __init__(self):
        self.app_settings = Config.new_internal_app_settings(feishu_app_id, feishu_app_secret,
                                                             feishu_app_verification_token, feishu_app_encrypt_key)
        # Currently, you are visiting larksuite, which uses default storage and default log (debug level). More optional configurations are as follows: README.md->Advanced use->How to build overall configuration(Config)。
        self.conf = Config.new_config_with_memory_store(DOMAIN_LARK_SUITE, self.app_settings, DefaultLogger(),
                                                        LEVEL_DEBUG)

    def send_text(self, msg):
        body = {
            'text': msg
        }
        self.post(body, "text")

    def send_image(self, pic_url):
        pass

    def send_markdown(self, title, text):
        pass

    def send_action_card(self, action_card: ActionCard):
        options = list(map(lambda x: {
            "text": {
                "tag": "plain_text",
                "content": x['title']
            },
            "value": x['actionURL']
        }, action_card.btns))
        body = {
            "config": {
                "wide_screen_mode": True
            },
            "i18n_elements": {
                "zh_cn": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": action_card.text
                        },
                        "extra": {
                            "tag": "select_static",
                            "placeholder": {
                                "tag": "plain_text",
                                "content": "点击选择菜单"
                            },
                            "value": {
                                "key": "value"
                            },
                            "options": options
                        }
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "img",
                                "img_key": "img_e344c476-1e58-4492-b40d-7dcffe9d6dfg",
                                "alt": {
                                    "tag": "plain_text",
                                    "content": "图片"
                                }
                            },
                            {
                                "tag": "plain_text",
                                "content": action_card.title
                            }
                        ]
                    }
                ]
            }
        }
        self.post(body, "interactive")

    def send_feed_card(self, links):
        pass

    def post(self, body, msg_type):
        if env_config.get("DEBUG_MODE") == '0':
            log.info(_json.dumps(body, indent=4))
            return
        receive_id = dark_local.receive_id
        post_data = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": _json.dumps(body)
        }
        req = Request('im/v1/messages?receive_id_type=chat_id', 'POST', ACCESS_TOKEN_TYPE_TENANT, post_data,
                      request_opts=[set_timeout(3)])
        resp = req.do(self.conf)
        log.info('request id = %s' % resp.get_request_id())
        log.info('request code = %s' % resp.code)
        if resp.code != 0:
            log.info(resp.msg)
            log.info(resp.error)
