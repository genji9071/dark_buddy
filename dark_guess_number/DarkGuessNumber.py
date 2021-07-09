from config import redis
from config.ChatbotsConfig import chatbots
from dark_listener.BaseOperation import BaseSymbol, SYMBOL_MATCH, REGEX_ANY_NUMBER
from lib.BaseChatbot import CardItem, ActionCard
from lib.RandomLib import random
from user.login.User_login import user_login

digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

guess_number_operator = BaseSymbol(SYMBOL_MATCH, REGEX_ANY_NUMBER)


def get_dark_guess_number_session_name(chatbotUserId):
    return 'tianhao:dark_buddy:dark_guess_number:{0}'.format(chatbotUserId)


def shut_down_guess_number(chatbot_user_id):
    redis.delete(get_dark_guess_number_session_name(chatbot_user_id))
    chatbots.get(chatbot_user_id).send_action_card(
        ActionCard(
            title="游戏结束",
            text="### 数字已经忘记......",
            btns=[CardItem(
                title="再来一把", url="dtmd://dingtalkclient/sendMessage?content=**游戏:猜数字:开启")]
        ))
    return


class DarkGuessNumber():
    def __init__(self, user_id, chatbot_user_id, listener):
        self.turn = 8
        self.digit_count = 4
        self.mode = 0  # 0-easy,1-hard
        self.user_id = user_id
        self.chatbot_user_id = chatbot_user_id
        self.listener = listener

    def treat_guess_number(self, number):
        guess_number_data = redis.get(get_dark_guess_number_session_name(self.chatbot_user_id))
        if guess_number_data is None:
            chatbots.get(self.chatbot_user_id).send_text('你要不先对我说：**游戏:猜数字:开启')
            return False
        data = eval(redis.get(get_dark_guess_number_session_name(self.chatbot_user_id)).decode())
        if number == '':
            self.display_guess_number(data)
            return True
        current_number = data['current_number']
        tried_record = data['tried_record']
        if len(number) != self.digit_count or not number.isdigit():
            chatbots.get(self.chatbot_user_id).send_text(
                '咱这个数字答案是{0}位数字，我寻思着你在这输的啥JB玩意儿呢！'.format(self.digit_count))
            return True
        a, b = self.calculate_guess_number(current_number, number)
        if a == self.digit_count:
            chatbots.get(self.chatbot_user_id).send_text(
                '哇你好屌，正确答案就是：「{0}」,秀秀秀！'.format(str(current_number)))
            user_login.get_luck_point_by_sender_id(50, self.user_id)
            return False
        tried_record.append({
            "try_number": number,
            "a": a,
            "b": b
        })
        data['try_time'] += 1
        if data['try_time'] >= self.turn:
            chatbots.get(self.chatbot_user_id).send_text(
                '游戏结束，正确答案是：「{0}」,小朋友你不行啊！'.format(str(current_number)))
            return False
        redis.setex(name=get_dark_guess_number_session_name(self.chatbot_user_id), time=3600,
                    value=str(data))
        self.display_guess_number(data)
        return True

    def start_guess_number(self):
        if redis.get(get_dark_guess_number_session_name(self.chatbot_user_id)) is None:
            chatbots.get(self.chatbot_user_id).send_text('正在生成数字......')
            guess_number_session_data = self.build_guess_number()
            redis.setex(name=get_dark_guess_number_session_name(self.chatbot_user_id), time=3600,
                        value=str(guess_number_session_data))
        self.display_guess_number(
            data=eval(redis.get(get_dark_guess_number_session_name(self.chatbot_user_id)).decode()))
        number = ''
        while self.treat_guess_number(number):
            number = self.listener.ask(guess_number_operator, '输入任意数字')
        shut_down_guess_number(self.chatbot_user_id)

    def build_guess_number(self):
        current_numbers_array = []
        if self.mode == 0:
            current_numbers_array = random.sample(population=digits, k=self.digit_count)
        elif self.mode == 1:
            current_numbers_array = random.choices(population=digits, k=self.digit_count)
        current_number = ''
        for num in current_numbers_array:
            current_number = current_number + str(num)
        try_time = 0
        tried_record = []
        return {
            'current_number': current_number,
            'try_time': try_time,
            'tried_record': tried_record
        }

    def display_guess_number(self, data):
        tried_record = data['tried_record']
        text = "# 暗黑数字：{0}\n 给出你的答案！输入：\n# **游戏:猜数字:猜:「你的答案」。\n 你还有「{1}」次机会，以下是记录。\n".format('*' * self.digit_count,
                                                                                             self.turn - int(
                                                                                                 data['try_time']))
        for record in tried_record:
            text = text + "- 【{0}】\t「{1}」个数字数位皆同，「{2}」个数字数同位不同\n".format(record['try_number'], record['a'], record['b'])
        chatbots.get(self.chatbot_user_id).send_markdown(title="猜数字", text=text)

    def calculate_guess_number(self, answer_number: str, current_number: str):
        a = 0
        b = 0
        for i in range(self.digit_count):
            if answer_number[i] == current_number[i]:
                a += 1
            elif current_number[i] in answer_number:
                b += 1
        return a, b
