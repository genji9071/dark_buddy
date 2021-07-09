#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import json
import logging
import time
from threading import Lock

from config.EnvConfig import env_config
from config.ThreadLocalSource import dark_local
from dark_live_chat import namespace
from lib.BaseChatbot import BaseChatbot, is_not_null_and_blank_str, ActionCard

logging.basicConfig(level=logging.INFO)
lock = Lock()
import requests

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


class DingtalkChatbot(BaseChatbot):
    """
    钉钉群自定义机器人（每个机器人每分钟最多发送20条），支持文本（text）、连接（link）、markdown三种消息类型！
    """

    def __init__(self, webhook, is_live_chat=False):
        """
        机器人初始化
        :param webhook: 钉钉群自定义机器人webhook地址
        """
        super(DingtalkChatbot, self).__init__()
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.webhook = webhook
        self.times = 0
        self.start_time = time.time()
        self.is_live_chat = is_live_chat

    def send_text(self, msg, is_at_all=False, at_mobiles=[], at_dingtalk_ids=[]):
        """
        text类型
        :param msg: 消息内容
        :param is_at_all: @所有人时：true，否则为false（可选）
        :param at_mobiles: 被@人的手机号（可选）
        :param at_dingtalk_ids: 被@人的dingtalkId（可选）
        :return: 返回消息发送结果
        """
        data = {"msgtype": "text", "at": {}}
        if is_not_null_and_blank_str(msg):
            data["text"] = {"content": msg}
        else:
            logging.error("text类型，消息内容不能为空！")
            raise ValueError("text类型，消息内容不能为空！")

        if is_at_all:
            data["at"]["isAtAll"] = is_at_all

        if at_mobiles:
            at_mobiles = list(map(str, at_mobiles))
            data["at"]["atMobiles"] = at_mobiles

        if at_dingtalk_ids:
            at_dingtalk_ids = list(map(str, at_dingtalk_ids))
            data["at"]["atDingtalkIds"] = at_dingtalk_ids

        logging.debug('text类型：%s' % data)
        return self.post(data)

    def send_image(self, pic_url):
        """
        image类型（表情）
        :param pic_url: 图片表情链接
        :return: 返回消息发送结果
        """
        if is_not_null_and_blank_str(pic_url):
            data = {
                "msgtype": "image",
                "image": {
                    "picURL": pic_url
                }
            }
            logging.debug('image类型：%s' % data)
            return self.post(data)
        else:
            logging.error("image类型中图片链接不能为空！")
            raise ValueError("image类型中图片链接不能为空！")

    def send_markdown(self, title, text, is_at_all=False, at_mobiles=[], at_dingtalk_ids=[]):
        """
        markdown类型
        :param title: 首屏会话透出的展示内容
        :param text: markdown格式的消息内容
        :param is_at_all: 被@人的手机号（在text内容里要有@手机号，可选）
        :param at_mobiles: @所有人时：true，否则为：false（可选）
        :param at_dingtalk_ids: 被@人的dingtalkId（可选）
        :return: 返回消息发送结果
        """
        if is_not_null_and_blank_str(title) and is_not_null_and_blank_str(text):
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": text
                },
                "at": {}
            }
            if is_at_all:
                data["at"]["isAtAll"] = is_at_all

            if at_mobiles:
                at_mobiles = list(map(str, at_mobiles))
                data["at"]["atMobiles"] = at_mobiles

            if at_dingtalk_ids:
                at_dingtalk_ids = list(map(str, at_dingtalk_ids))
                data["at"]["atDingtalkIds"] = at_dingtalk_ids

            logging.debug("markdown类型：%s" % data)
            return self.post(data)
        else:
            logging.error("markdown类型中消息标题或内容不能为空！")
            raise ValueError("markdown类型中消息标题或内容不能为空！")

    def send_action_card(self, action_card):
        """
        ActionCard类型
        :param action_card: 整体跳转ActionCard类型实例或独立跳转ActionCard类型实例
        :return: 返回消息发送结果
        """
        if isinstance(action_card, ActionCard):
            data = action_card.get_data()
            logging.debug("ActionCard类型：%s" % data)
            return self.post(data)
        else:
            logging.error("ActionCard类型：传入的实例类型不正确！")
            raise TypeError("ActionCard类型：传入的实例类型不正确！")

    def send_feed_card(self, links):
        """
        FeedCard类型
        :param links: 信息集（FeedLink数组）
        :return: 返回消息发送结果
        """
        link_data_list = []
        for link in links:
            if isinstance(link, FeedLink) or isinstance(link, CardItem):
                link_data_list.append(link.get_data())
        if link_data_list:
            # 兼容：1、传入FeedLink或CardItem实例列表；2、传入数据字典列表；
            links = link_data_list
        data = {"msgtype": "feedCard", "feedCard": {"links": links}}
        logging.debug("FeedCard类型：%s" % data)
        return self.post(data)

    def post(self, data):
        """
        发送消息（内容UTF-8编码）
        :param data: 消息数据（字典）
        :return: 返回发送结果
        """
        if not self.is_live_chat:
            lock.acquire()
            self.times += 1
            if self.times % 20 == 0:
                if time.time() - self.start_time < 60:
                    logging.info('钉钉官方限制每个机器人每分钟最多发送20条，当前消息发送频率已达到限制条件，休眠一分钟')
                    time.sleep(61 - time.time() + self.start_time)
                self.start_time = time.time()
            lock.release()
        post_data = json.dumps(data)
        try:
            if env_config.get("DEBUG_MODE") == '0':
                logging.info(post_data.encode('utf-8').decode('unicode_escape'))
                return
            if self.is_live_chat:
                from dark_live_chat import socketio
                session_id = dark_local.session_id
                socketio.emit("answer", post_data, room=session_id, namespace=namespace)
                return
            response = requests.post(self.webhook, headers=self.headers, data=post_data)
        except requests.exceptions.HTTPError as exc:
            logging.error("消息发送失败， HTTP error: %d, reason: %s" % (exc.response.status_code, exc.response.reason))
            raise
        except requests.exceptions.ConnectionError:
            logging.error("消息发送失败，HTTP connection error!")
            raise
        except requests.exceptions.Timeout:
            logging.error("消息发送失败，Timeout error!")
            raise
        except requests.exceptions.RequestException:
            logging.error("消息发送失败, Request Exception!")
            raise
        else:
            try:
                result = response.json()
            except JSONDecodeError:
                logging.error("服务器响应异常，状态码：%s，响应内容：%s" % (response.status_code, response.text))
                return {'errcode': 500, 'errmsg': '服务器响应异常'}
            else:
                logging.debug('发送结果：%s' % result)
                # if result['punish']:
                #     error_data = {"msgtype": "text", "text": {"content": "钉钉机器人消息发送失败，原因：%s" % str(result)},
                #                   "at": {"isAtAll": True}}
                #     logging.error("消息发送失败，自动通知：%s" % error_data)
                #     requests.post(self.webhook, headers=self.headers, data=json.dumps(error_data))
                # return result
