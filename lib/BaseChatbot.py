# coding=utf-8
from abc import ABCMeta, abstractmethod

from lib.Logger import log


def is_not_null_and_blank_str(content):
    """
    非空字符串
    :param content: 字符串
    :return: 非空 - True，空 - False

    >>> is_not_null_and_blank_str('')
    False
    >>> is_not_null_and_blank_str(' ')
    False
    >>> is_not_null_and_blank_str('  ')
    False
    >>> is_not_null_and_blank_str('123')
    True
    """
    if content and content.strip():
        return True
    else:
        return False


class BaseChatbot(metaclass=ABCMeta):
    @abstractmethod
    def send_text(self, msg, is_at_all=False, at_mobiles=[], at_dingtalk_ids=[]):
        pass

    @abstractmethod
    def send_image(self, pic_url):
        pass

    @abstractmethod
    def send_markdown(self, title, text, is_at_all=False, at_mobiles=[], at_dingtalk_ids=[]):
        pass

    @abstractmethod
    def send_action_card(self, action_card):
        pass

    @abstractmethod
    def send_feed_card(self, links):
        pass


class ActionCard(object):
    """
    ActionCard类型消息格式（整体跳转、独立跳转）
    """

    def __init__(self, title, text, btns, btn_orientation=0, hide_avatar=0):
        """
        ActionCard初始化
        :param title: 首屏会话透出的展示内容
        :param text: markdown格式的消息
        :param btns: 按钮列表：（1）按钮数量为1时，整体跳转ActionCard类型；（2）按钮数量大于1时，独立跳转ActionCard类型；
        :param btn_orientation: 0：按钮竖直排列，1：按钮横向排列（可选）
        :param hide_avatar: 0：正常发消息者头像，1：隐藏发消息者头像（可选）
        """
        super(ActionCard, self).__init__()
        self.title = title
        self.text = text
        self.btn_orientation = btn_orientation
        self.hide_avatar = hide_avatar
        btn_list = []
        for btn in btns:
            if isinstance(btn, CardItem):
                btn_list.append(btn.get_data())
        if btn_list:
            btns = btn_list  # 兼容：1、传入CardItem示例列表；2、传入数据字典列表
        self.btns = btns


class FeedLink(object):
    """
    FeedCard类型单条消息格式
    """

    def __init__(self, title, message_url, pic_url):
        """
        初始化单条消息文本
        :param title: 单条消息文本
        :param message_url: 点击单条信息后触发的URL
        :param pic_url: 点击单条消息后面图片触发的URL
        """
        super(FeedLink, self).__init__()
        self.title = title
        self.message_url = message_url
        self.pic_url = pic_url

    def get_data(self):
        """
        获取FeedLink消息数据（字典）
        :return: 本FeedLink消息的数据
        """
        if is_not_null_and_blank_str(self.title) and is_not_null_and_blank_str(
                self.message_url) and is_not_null_and_blank_str(self.pic_url):
            data = {
                "title": self.title,
                "messageURL": self.message_url,
                "picURL": self.pic_url
            }
            return data
        else:
            log.error("FeedCard类型单条消息文本、消息链接、图片链接不能为空！")
            raise ValueError("FeedCard类型单条消息文本、消息链接、图片链接不能为空！")


class CardItem(object):
    """
    ActionCard和FeedCard消息类型中的子控件
    """

    def __init__(self, title, url, pic_url=None):
        """
        CardItem初始化
        @param title: 子控件名称
        @param url: 点击子控件时触发的URL
        @param pic_url: FeedCard的图片地址，ActionCard时不需要，故默认为None
        """
        super(CardItem, self).__init__()
        self.title = title
        self.url = url
        self.pic_url = pic_url

    def get_data(self):
        """
        获取CardItem子控件数据（字典）
        @return: 子控件的数据
        """
        if is_not_null_and_blank_str(self.pic_url) and is_not_null_and_blank_str(
                self.title) and is_not_null_and_blank_str(self.url):
            # FeedCard类型
            data = {
                "title": self.title,
                "messageURL": self.url,
                "picURL": self.pic_url
            }
            return data
        elif is_not_null_and_blank_str(self.title) and is_not_null_and_blank_str(self.url):
            # ActionCard类型
            data = {
                "title": self.title,
                "actionURL": self.url
            }
            return data
        else:
            log.error("CardItem是ActionCard的子控件时，title、url不能为空；是FeedCard的子控件时，title、url、pic_url不能为空！")
            raise ValueError("CardItem是ActionCard的子控件时，title、url不能为空；是FeedCard的子控件时，title、url、pic_url不能为空！")
