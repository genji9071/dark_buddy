import uuid

from config.ChatbotsConfig import chatbots
from dark_listener.BaseListener import BaseListener
from dark_listener.BaseOperation import BaseOperator, OPERATOR_OR, BaseSymbol, SYMBOL_EQUALS, SYMBOL_MATCH, \
    REGEX_ANY_NUMBER, OPERATOR_AND, SYMBOL_GREATER_EQUAL
from dark_twenty_one.DarkTwentyOneGameProcess import DarkTwentyOneGameProcess

minimum_bet = 10

bet_operation = BaseOperator(
    OPERATOR_OR,
    [
        BaseSymbol(SYMBOL_EQUALS, 'giveup'),
        BaseOperator(OPERATOR_AND, [
            BaseSymbol(SYMBOL_MATCH, REGEX_ANY_NUMBER),
            BaseSymbol(SYMBOL_GREATER_EQUAL, minimum_bet)
        ])
    ]
)

call_operation = BaseOperator(
    OPERATOR_OR,
    [
        BaseSymbol(SYMBOL_EQUALS, 'call'),
        BaseSymbol(SYMBOL_EQUALS, 'done')
    ]
)


class DarkTwentyOneListener(BaseListener):

    def get_listener_task(self):
        self.game_process = DarkTwentyOneGameProcess(uuid.uuid1(), self.user_id, chatbots.get(self.chatbot_user_id),
                                                     self)
        return self.game_process.main_process()

    def ask_for_bet(self):
        return self.ask(bet_operation, '请输入金额，不少于{0}块，或者输入giveup放弃，颗粒无收！'.format(minimum_bet))

    def ask_for_call(self):
        return self.ask(call_operation, '请输入call多要一张牌，或者done停止要牌。')
