from config import redis
from config.ChatbotsConfig import chatbots
from config.TianApi import get_true_or_false, get_multiple_choice
from dark_menu.BaseHandler import BaseHandler
from lib.BaseChatbot import ActionCard, CardItem
from user.login.User_login import user_login


class DarkQuiz(BaseHandler):
    def do_handle(self, request_object, request_json):
        if request_object[2] == '答题':
            type = request_object[3]
            answer = request_object[4]
            self.treat_dark_quiz(answer, type, request_json=request_json)
            return True
        if '是非题' in request_object[2]:
            self.true_or_false(request_json)
            return True
        if '单选题' in request_object[2]:
            self.multiple_choice(request_json)
            return True
        return False

    def true_or_false(self, request_json):
        redis_data_str = redis.get(self.get_dark_quiz_tf_session_name(request_json['chatbotUserId']))
        if redis_data_str is None:
            data = get_true_or_false()
            redis_data_str = self.put_into_redis(request_json, data['newslist'][0], 0)
        redis_data = eval(redis_data_str)
        self.display_tf_quiz(redis_data, request_json)

    def treat_dark_quiz(self, answer, type, request_json):
        redis_data_str = redis.get(self.get_session_name_by_type(request_json['chatbotUserId'], int(type)))
        if redis_data_str is None:
            return
        redis_data = eval(redis_data_str)
        if redis_data['answer'] == int(answer):
            chatbots.get(request_json['chatbotUserId']).send_action_card(ActionCard(
                title="暗黑答题",
                text="### 回答正确！6六6！",
                btns=[
                    CardItem(
                        title="再来一题是非题", url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑答题:是非题(10金币)"),
                    CardItem(
                        title="再来一题单选题", url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑答题:单选题(20金币)")
                ]
            ))
            if type == '0':
                user_login.rewards_to_sender_id(10, request_json)
            if type == '1':
                user_login.rewards_to_sender_id(20, request_json)
        else:
            chatbots.get(request_json['chatbotUserId']).send_action_card(ActionCard(
                title="暗黑答题",
                text="### GG！回答错误！正确答案是「{0}」,相关信息：{1}".format(redis_data['answer_str'], redis_data['analytic']),
                btns=[
                    CardItem(
                        title="再来一题是非题", url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑答题:是非题(10金币)"),
                    CardItem(
                        title="再来一题单选题", url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑答题:单选题(20金币)")
                ]
            ))
            user_login.rewards_to_sender_id(-5, request_json)
        redis.delete(self.get_session_name_by_type(request_json['chatbotUserId'], int(type)))

    def multiple_choice(self, request_json):
        redis_data_str = redis.get(self.get_dark_quiz_mc_session_name(request_json['chatbotUserId']))
        if redis_data_str is None:
            data = get_multiple_choice()
            redis_data_str = self.put_into_redis(request_json, data['newslist'][0], 1)
        redis_data = eval(redis_data_str)
        self.display_mc_quiz(redis_data, request_json)

    @staticmethod
    def get_dark_quiz_tf_session_name(chatbotUserId):
        return 'tianhao:dark_buddy:dark_quiz_tf:{0}'.format(chatbotUserId)

    @staticmethod
    def get_dark_quiz_mc_session_name(chatbotUserId):
        return 'tianhao:dark_buddy:dark_quiz_mc:{0}'.format(chatbotUserId)

    def put_into_redis(self, request_json, data, type):
        if isinstance(data['answer'], int):
            data['answer'] = 0 if data['answer'] == 1 else 1
            data['answer_str'] = '是' if data['answer'] == 0 else '否'
            data['choices'] = ['是', '否']
            data['analytic'] = data['analyse']
        else:
            if data['answer'] == 'A':
                data['answer'] = 0
            if data['answer'] == 'B':
                data['answer'] = 1
            if data['answer'] == 'C':
                data['answer'] = 2
            if data['answer'] == 'D':
                data['answer'] = 3
            data['choices'] = ['A：{0}'.format(data['answerA']), 'B：{0}'.format(data['answerB']), 'C：{0}'.format(data['answerC']), 'D：{0}'.format(data['answerD'])]
            data['answer_str'] = data['choices'][data['answer']]
        data_str = str(data)
        redis.setex(name=self.get_session_name_by_type(request_json['chatbotUserId'], type), time=3600,
                    value=data_str)
        return data_str

    def display_tf_quiz(self, redis_data, request_json):
        btns = []
        for i, choice in enumerate(redis_data['choices']):
            btns.append(CardItem(
                    title=choice, url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑答题:答题:0:{0}".format(i)))
        chatbots.get(request_json['chatbotUserId']).send_action_card(ActionCard(
            title="暗黑答题",
            text="### 答对加10金币，答错扣5金币\n{0}".format(redis_data['title']),
            btns=btns
        ))

    def display_mc_quiz(self, redis_data, request_json):
        btns = []
        for i, choice in enumerate(redis_data['choices']):
            btns.append(CardItem(
                title=choice, url="dtmd://dingtalkclient/sendMessage?content=**游戏:暗黑答题:答题:1:{0}".format(i)))
        chatbots.get(request_json['chatbotUserId']).send_action_card(ActionCard(
            title="暗黑答题",
            text="### 答对加20金币，答错扣5金币\n{0}".format(redis_data['title']),
            btns=btns
        ))

    def get_session_name_by_type(self, chatbotUserId, type):
        if type == 0:
            return self.get_dark_quiz_tf_session_name(chatbotUserId)
        if type == 1:
            return self.get_dark_quiz_mc_session_name(chatbotUserId)

dark_quiz = DarkQuiz()