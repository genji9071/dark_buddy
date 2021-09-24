from config import redis
from config.ChatbotsConfig import chatbots
from dark_listener.BaseListener import BaseListener
from dark_listener.BaseOperation import BaseOperator, OPERATOR_AND, SYMBOL_MATCH, BaseSymbol, \
    SYMBOL_GREATER, SYMBOL_LESS, SYMBOL_EQUALS, OPERATOR_OR, REGEX_ANY_FLOAT, SYMBOL_GREATER_EQUAL
from lib.BaseChatbot import ActionCard, CardItem


def build_daily_salary_operator():
    return BaseOperator(OPERATOR_AND, [
        BaseSymbol(SYMBOL_MATCH, REGEX_ANY_FLOAT),
        BaseSymbol(SYMBOL_GREATER, 0)
    ])


def build_hours_operator():
    return BaseOperator(OPERATOR_AND, [
        BaseSymbol(SYMBOL_MATCH, REGEX_ANY_FLOAT),
        BaseSymbol(SYMBOL_GREATER_EQUAL, 0),
        BaseSymbol(SYMBOL_LESS, 24),
    ])


def build_score_operator(choice):
    ls = []
    for i in range(0, choice):
        ls.append(BaseSymbol(SYMBOL_EQUALS, str(i + 1)))
    return BaseOperator(OPERATOR_OR, ls)


phase_list = [
    {
        'answer_type': 'DAILY_SALARY',
        'question': '输入你的平均日薪酬, 单位是元,月薪除22(996的人自行除以26)',
        'operator': build_daily_salary_operator()
    },
    {
        'answer_type': 'WORKING_HOURS',
        'question': '输入你的工作小时数，下班时间-上班时间',
        'operator': build_hours_operator()
    },
    {
        'answer_type': 'COMMUTING_HOURS',
        'question': '输入你的通勤小时数，路上一天花的时间',
        'operator': build_hours_operator()
    },
    {
        'answer_type': 'PLAYING_HOURS',
        'question': '输入你的摸鱼小时数，不干活时长+吃饭时长+午休时长',
        'operator': build_hours_operator()
    },
    {
        'answer_type': 'STUDY_SCORE',
        'question': '输入你的学历，「专科及以下」选1，「普通本科」选2，「985211海归本科」选3，「普通硕士」选4，「985211海归硕士」选5，「普通博士」选6，「985211海归博士」选7',
        'operator': build_score_operator(7)
    },
    {
        'answer_type': 'WORKING_AREA_SCORE',
        'question': '输入你的工作环境，「偏僻地区」选1，「工厂及郊区」选2，「市区」选3，「体制内」选4',
        'operator': build_score_operator(4)
    },
    {
        'answer_type': 'SEXY_AREA_SCORE',
        'question': '输入你的异性环境，「没有」选1，「不多不少」选2，「很多」选3',
        'operator': build_score_operator(3)
    },
    {
        'answer_type': 'GUYS_AREA_SCORE',
        'question': '输入你的同事环境，「SB很多」选1，「大都普通」选2，「有很多大佬」选3',
        'operator': build_score_operator(3)
    },
    {
        'answer_type': 'EVIL_MORNING_SCORE',
        'question': '是否8:30前上班，「是」选1，「否」选2',
        'operator': build_score_operator(2)
    }
]

WORKING_AREA_SCORE_MAP = {
    '1': 0.8,
    '2': 0.9,
    '3': 1,
    '4': 1.1
}

STUDY_SCORE_MAP = {
    '1': 0.8,
    '2': 1,
    '3': 1.2,
    '4': 1.4,
    '5': 1.6,
    '6': 1.8,
    '7': 2
}

SEXY_AREA_SCORE_MAP = {
    '1': 0.9,
    '2': 1,
    '3': 1.1
}

GUYS_AREA_SCORE_MAP = {
    '1': 0.95,
    '2': 1,
    '3': 1.05
}

EVIL_MORNING_SCORE_MAP = {
    '1': 0.95,
    '2': 1
}


def get_dark_work_shuang_rank_session_name(chatbotUserId):
    return 'tianhao:dark_buddy:dark_work_shuang_rank:{0}'.format(chatbotUserId)


def shut_down_work_shuang_rank(chatbot_user_id):
    redis.delete(get_dark_work_shuang_rank_session_name(chatbot_user_id))
    chatbots.get(chatbot_user_id).send_action_card(
        ActionCard(
            title="计算已关闭",
            text="### 计算已关闭......",
            btns=[CardItem(
                title="重新计算", url="**工作性价比:开启")]
        ))
    return


class DarkWorkShuangRankListener(BaseListener):
    def get_listener_task(self):
        scores = {}
        for phase in phase_list:
            answer = self.ask(phase['operator'], phase['question'])
            scores[phase['answer_type']] = answer
        self.display_result(scores)
        redis.delete(get_dark_work_shuang_rank_session_name(self.chatbot_user_id))

    def display_result(self, scores):
        daily_salary = float(scores['DAILY_SALARY'])
        working_hours = float(scores['WORKING_HOURS'])
        commuting_hours = float(scores['COMMUTING_HOURS'])
        playing_hours = float(scores['PLAYING_HOURS'])

        working_area_score = WORKING_AREA_SCORE_MAP.get(scores['WORKING_AREA_SCORE'])
        study_score = STUDY_SCORE_MAP.get(scores['STUDY_SCORE'])
        sexy_area_score = SEXY_AREA_SCORE_MAP.get(scores['SEXY_AREA_SCORE'])
        guys_area_score = GUYS_AREA_SCORE_MAP.get(scores['GUYS_AREA_SCORE'])
        evil_morning_score = EVIL_MORNING_SCORE_MAP.get(scores['EVIL_MORNING_SCORE'])

        result_1 = daily_salary * working_area_score * sexy_area_score * guys_area_score * evil_morning_score
        result_2 = 35 * study_score * (working_hours + commuting_hours - 0.5 * playing_hours)
        result = result_1 / result_2
        text = '爽到爆炸'
        if result < 0.8:
            text = '很惨'
        elif result < 1.5:
            text = '一般'
        elif result < 2:
            text = '很爽'
        chatbots.get(self.chatbot_user_id).send_action_card(
            ActionCard(
                title="计算完成",
                text="### 得分：{0}\n ### 你的工作性价比：「{1}」".format(result, text),
                btns=[CardItem(
                    title="重新计算", url="**工作性价比:开启")]
            ))
