# coding=utf-8
import traceback

from config.ChatbotsConfig import chatbots
from dark_chat.dark_qa.QACrawler import searchsummary
from lib.Logger import log


class DarkQa:

    def qa(self, question):
        ans = searchsummary.kwquery(question)
        return ans

    def get_dark_qa(self, request_json, debug_mode=False):
        request = request_json["text"]["content"]
        try:
            datas = self.qa(request)
            if debug_mode:
                log.info('datas:' + str(datas))
                return True
        except:
            log.error(traceback.format_exc())
            log.error(request)
            chatbots.get(request_json['chatbotUserId']).send_text("你这是说的什么弟弟鬼话呢！")
            return False

        if datas:
            log.info(str(datas))
            if datas['type'] is 'text':
                chatbots.get(request_json['chatbotUserId']).send_markdown(str(datas['from']), str(datas['value']))
            if datas['type'] is 'img':
                chatbots.get(request_json['chatbotUserId']).send_image(datas['value'][0])

        return True


dark_qa = DarkQa()
