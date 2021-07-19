# coding=utf-8
import traceback

import mapper as mapper
from config.ChatbotsConfig import chatbots
from dark_menu.BaseHandler import BaseHandler
from lib.BaseChatbot import ActionCard, CardItem
from lib.Logger import log


class RenShe(BaseHandler):
    def __init__(self):
        pass

    def do_handle(self, request_array, request_json):
        try:
            if request_array[1] == '显示':
                if len(request_array) < 3:
                    action_card = self.build_all_status_property_list_action_card()
                    chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
                    return True
                founded_status_property = mapper.mapper_user_status_property.select_by_name(request_array[2])
                if not founded_status_property:
                    action_card = self.build_all_status_property_list_action_card()
                    chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
                    return True
                founded_user = mapper.mapper_user.select_by_senderId(request_json['senderId'])
                founded_status = mapper.mapper_user_status.select_by_statusId_and_userId(
                    founded_status_property.get('id'), founded_user.get('id'))
                if not founded_status:
                    chatbots.get(request_json['chatbotUserId']).send_text('{0}，你还不曾拥有这个叫做"{1}"的属性，请对我说"**人设:增加:{2}:XXX"添加。'.format(request_json['senderNick'], request_array[2], request_array[2]))
                    return True
                chatbots.get(request_json['chatbotUserId']).send_text(
                    '{0}，你的属性「{1}」为: {2}.\n属性描述：{3}.'.format(request_json['senderNick'], request_array[2],
                                                             founded_status.get('value'),
                                                             founded_status_property.get('description')))
                return True

            elif request_array[1] == '增加':
                if len(request_array) != 4:
                    if len(request_array) != 3:
                        chatbots.get(request_json['chatbotUserId']).send_text('{0}，请对我说"**人设:增加:[你的属性]:[属性的值]"添加或者更改。'.format(request_json['senderNick']))
                    else:
                        founded_status_property = mapper.mapper_user_status_property.select_by_name(request_array[2])
                        if not founded_status_property:
                            chatbots.get(request_json['chatbotUserId']).send_text('{0}，我还不认识这个叫做"{1}"的属性，请联系管理员添加。'.format(request_json['senderNick'],
                                                                                       request_array[2].strip()))
                            return True
                        chatbots.get(request_json['chatbotUserId']).send_text('{0}，请对我说"**人设:增加:{1}:[属性的值]"添加或者更改。'.format(request_json['senderNick'], request_array[2]))
                    return True
                status_name = request_array[2]
                status_value = request_array[3]
                founded_status_property = mapper.mapper_user_status_property.select_by_name(status_name.strip())
                if not founded_status_property:
                    chatbots.get(request_json['chatbotUserId']).send_text(
                        '{0}，我还不认识这个叫做"{1}"的属性，请联系管理员添加。'.format(request_json['senderNick'], status_name.strip()))
                    return True
                if founded_status_property.get('editable') != 0:
                    chatbots.get(request_json['chatbotUserId']).send_text(
                        '{0}，"{1}"的属性不能被修改，请不要作弊！'.format(request_json['senderNick'], status_name.strip()))
                    return True
                founded_user = mapper.mapper_user.select_by_senderId(request_json['senderId'])
                user_status = {
                    'status_id': founded_status_property.get('id'),
                    'status_code': founded_status_property.get('code'),
                    'user_id': founded_user.get('id'),
                    'value': status_value
                }
                founded_status = mapper.mapper_user_status.update_user_status(user_status)

                chatbots.get(request_json['chatbotUserId']).send_text(
                    '{0}，同步完成！你的属性「{1}」为: {2}.'.format(request_json['senderNick'], status_name.strip(),
                                                       founded_status.get('value')))
                return True

        except:
            log.error(traceback.format_exc())
        return False

    def build_all_status_property_list_action_card(self):
        all_status_property = mapper.mapper_user_status_property.select_all()
        btns = []
        if len(all_status_property) == 0:
            btn = CardItem(title='增加',
                           url="**人设:增加")
            btns.append(btn)
            title = "你是想问？"
            text = "# 目前尚未拥有人设，请增加你的人设。"
            return ActionCard(title=title, text=text, btns=btns, btn_orientation=1)
        for status_property in all_status_property:
            btn = CardItem(title=status_property.get('name'),
                           url="**人设:显示:{0}".format(
                               status_property.get('name')))
            btns.append(btn)
        title = "你是想问？"
        text = "# 关于你的人设, 你是想问？"
        return ActionCard(title=title, text=text, btns=btns, btn_orientation=1)


ren_she_handler = RenShe()