# coding=utf-8
import codecs
import time
import traceback

import requests

import mapper
from config.ChatbotsConfig import chatbots
from dark_menu.BaseHandler import BaseHandler
from lib.BaseChatbot import ActionCard, CardItem, FeedLink
from lib.Logger import log
from lib.RandomLib import random


class JuheApi(BaseHandler):
    def __init__(self):
        self.header = {}
        self.function_map = {
            "joke": "http://v.juhe.cn/joke/randJoke.php?key=c41014c93556a6a3e9580ccd576c020a",
            "toutiao": "http://v.juhe.cn/toutiao/index?type=top&key=29c9fec25a4f50472339708671e4baf3",
            "weixin": "http://v.juhe.cn/weixin/query?key=d55bdd0377a80047ae451bff3c2c2f90",
            # "constellation": "http://web.juhe.cn:8080/constellation/getAll?consName=%s&type=today&key=c8c08fa89017c1e794b7a816270432e5",
            "constellation": "http://api.tianapi.com/txapi/star?key=e023522efde1f79611b561ce341c0376&astro=%s&y=%s&m=%s&d=%s",
            "laohuangli": "http://v.juhe.cn/laohuangli/d?date=%s&key=c41014c93556a6a3e9580ccd576c020a",
            "dongtu": "https://www.soogif.com/hotGif?start=%s&size=1",
            "today": "http://v.juhe.cn/todayOnhistory/queryEvent.php?key=0a1d8a00deca567a57e107d444c23bef&date=",
            "name": "http://api.tianapi.com/txapi/cname/?key=e023522efde1f79611b561ce341c0376",
            "honey": "http://api.tianapi.com/txapi/saylove/?key=e023522efde1f79611b561ce341c0376",
            "sweet": "http://api.tianapi.com/txapi/caihongpi/index?key=b51ebfea67131117bab4d5252f24b1a7",
            "shit": "http://api.tianapi.com/txapi/dujitang/index?key=b51ebfea67131117bab4d5252f24b1a7"
        }
        self.request_map = {
            "笑话": "joke",
            "新闻": "toutiao",
            "骚东西": "weixin",
            "星座": "constellation",
            "今日黄历": "laohuangli",
            "动图": "dongtu",
            "今天": "today",
            "土味情话": "honey",
            "取名": "name",
            "远哥语录": "sweet",
            "孟婆汤": "shit"
        }
        self.status_constellation_map = {
            "白羊座": "aries",
            "白羊": "aries",
            "金牛座": "taurus",
            "金牛": "aquarius",
            "双子座": "gemini",
            "双子": "gemini",
            "狮子座": "leo",
            "狮子": "leo",
            "处女座": "virgo",
            "处女": "virgo",
            "天蝎座": "scorpio",
            "天蝎": "scorpio",
            "摩羯座": "capricorn",
            "摩羯": "capricorn",
            "双鱼座": "pisces",
            "双鱼": "pisces",
            "水瓶座": "aquarius",
            "水瓶": "aquarius",
            "射手座": "sagittarius",
            "射手": "sagittarius",
            "巨蟹座": "cancer",
            "巨蟹": "cancer",
            "天秤座": "libra",
            "天秤": "libra",
            "天平座": "libra",
            "天平": "libra"
        }
        self.random = 0

    def do_handle(self, request_object, request_json):
        matched = self.request_map.get(request_object[1])

        if matched is None:
            return False
        return self.get_request(matched, request_json)

    def get_request(self, matched, json):
        request = self.function_map.get(matched)
        if matched == "constellation":
            # 拿这个人的星座，是最骚的
            ding_id = json["senderId"]
            user = mapper.mapper_user.select_by_senderId(ding_id)
            user_status = mapper.mapper_user_status.select_by_statusCode_and_userId('constellation', user.id)
            if not user_status:
                log.error('{0}这个人没星座这个属性。'.format(json["senderNick"]))
                return None
            constellation = self.status_constellation_map.get(user_status.value)
            if not constellation:
                log.error('{0}这个人星座这个属性乱写：{1}。'.format(json["senderNick"], user_status.value))
                return None
            year = time.strftime("%Y", time.localtime(int(time.time()) / 1000))
            month = time.strftime("%m", time.localtime(int(time.time()) / 1000))
            day = time.strftime("%d", time.localtime(int(time.time()) / 1000))
            request = request % (constellation, year, month, day)
        elif matched == "laohuangli":
            date = time.strftime("%Y-%m-%d", time.localtime(int(time.time()) / 1000))
            request = request % date
        elif matched == "dongtu":
            self.random = random.randint(0,5000)
            request = request % self.random
        elif matched == "today":
            date = time.strftime("%-m/%-d", time.localtime(int(time.time()) / 1000))
            request = request + date
        if not request:
            chatbots.get(json['chatbotUserId']).send_text("你并不能得到这个信息，你觉得是为什么呢？")
            return True
        response = requests.request("GET", request, headers=self.header)
        content = codecs.decode(response.content, "utf-8")
        content.replace("null", "None")
        response_json = eval(content)
        try:
            self.send_message_by_response(matched, json, response_json)
            return True
        except:
            log.error(traceback.format_exc())
            log.error(content)
            return False

    def send_message_by_response(self, matched, request_json, response_json):
        if matched == "joke":
            for i in range(0, 3):
                joke = response_json["result"][i]
                chatbots.get(request_json['chatbotUserId']).send_text(joke["content"])
        elif matched == "toutiao":
            feed_links = []
            datas = response_json.get('result').get('data')
            for i in range(0, 4):
                data = datas[i]
                feed_link = FeedLink(title=data.get('title'), message_url=data.get('url'), pic_url=data.get('thumbnail_pic_s'))
                feed_links.append(feed_link)
            chatbots.get(request_json['chatbotUserId']).send_feed_card(feed_links)
        elif matched == "weixin":
            log.info(str(response_json))
            chatbots.get(request_json['chatbotUserId']).send_text("敬请期待...")
        elif matched == "constellation":
            name = request_json["senderNick"]
            text = ""
            for i in range(len(response_json["newslist"])):
                text+=response_json["newslist"][i]["type"]
                text+=": "
                text+=response_json["newslist"][i]["content"]
                text+="\n\n"
            chatbots.get(request_json['chatbotUserId']).send_markdown(title="%s，这就是你今天的暗黑星座运势" % name, text=text, is_at_all=False)
        elif matched == "laohuangli":
            log.info(str(response_json))
            datas = response_json.get('result')
            chatbots.get(request_json['chatbotUserId']).send_markdown(title="今日黄历", text="### 宜：" + datas["yi"] + "\n" + "### 忌：" + datas["ji"])
        elif matched == "dongtu":
            log.info(str(response_json))
            datas = response_json["data"]["result"][0]
            action_card = ActionCard(title=datas["title"],
                                     text="![screenshot](" + datas["gifurl"] + ")\n" + "#### " + datas["title"],
                                     btns=[CardItem(title="查看更多", url="**小功能:动图")])
            chatbots.get(request_json['chatbotUserId']).send_action_card(action_card)
        elif matched == "today":
            log.info(str(response_json))
            dataCollection = response_json["result"]
            data = random.choice(dataCollection)
            chatbots.get(request_json['chatbotUserId']).send_text(
                "早啊！^_^ 历史上的今天--" + data["date"] + " " + data["title"])
        elif matched == "honey":
            log.info(str(response_json))
            chatbots.get(request_json['chatbotUserId']).send_text(response_json["newslist"][0]["content"])
        elif matched == "name":
            log.info(str(response_json))
            chatbots.get(request_json['chatbotUserId']).send_text(response_json["newslist"][0]["naming"])
        elif matched == "sweet":
            log.info(str(response_json))
            chatbots.get(request_json['chatbotUserId']).send_text(response_json["newslist"][0]["content"])
        elif matched == "shit":
            log.info(str(response_json))
            chatbots.get(request_json['chatbotUserId']).send_text(response_json["newslist"][0]["content"])
        else:
            chatbots.get(request_json['chatbotUserId']).send_text("你TM说啥呢！滚犊子")

juhe_api = JuheApi()