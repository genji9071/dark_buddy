import re
from abc import abstractmethod

TYPE_OPERATOR = 'operator'
TYPE_SYMBOL = 'symbol'

OPERATOR_AND = 'and'
OPERATOR_OR = 'or'
OPERATOR_NOT = 'not'

SYMBOL_EQUALS = 'eq'
SYMBOL_NOT_EQUALS = 'ne'
SYMBOL_GREATER = 'gt'
SYMBOL_LESS = 'lt'
SYMBOL_GREATER_EQUAL = 'ge'
SYMBOL_LESS_EQUAL = 'le'
SYMBOL_MATCH = 'match'

REGEX_ANY_NUMBER = r'\d+'
REGEX_ANY_THING = r'.+'

base_symbol_map = {
    'eq': SYMBOL_EQUALS,
    'ne': SYMBOL_NOT_EQUALS,
    'gt': SYMBOL_GREATER,
    'lt': SYMBOL_LESS,
    'ge': SYMBOL_GREATER_EQUAL,
    'le': SYMBOL_LESS_EQUAL,
    'match': SYMBOL_MATCH
}

base_operator_map = {
    'and': OPERATOR_AND,
    'or': OPERATOR_OR,
    'not': OPERATOR_NOT
}


class BaseOperation:

    def __init__(self):
        self.operation_type = self.get_operation_type()

    @abstractmethod
    def get_operation_type(self):
        pass

    @abstractmethod
    def encode(self):
        pass


class BaseSymbol(BaseOperation):
    def encode(self):
        result = {
            'operation_type': self.operation_type,
            'symbol': self.symbol,
            'target': self.target
        }
        return result

    def get_operation_type(self):
        return TYPE_SYMBOL

    def __init__(self, symbol, target):
        super().__init__()
        self.symbol = symbol
        self.target = target


class BaseOperator(BaseOperation):
    def get_operation_type(self):
        return TYPE_OPERATOR

    def __init__(self, operator, target):
        super().__init__()
        self.operator = operator
        self.target = target

    def encode(self):
        result = {
            'operation_type': self.operation_type,
            'operator': self.operator,
        }
        sub_targets = []
        for sub_target in self.target:
            sub_targets.append(sub_target.encode())
        result['target'] = sub_targets
        return result


def validate(source, target):
    operation_type = target['operation_type']
    if operation_type == TYPE_SYMBOL:
        return _validate_symbol(source, target['target'], target['symbol'])
    elif operation_type == TYPE_OPERATOR:
        return _validate_operator(source, target['target'], target['operator'])
    return False


def _validate_symbol(source: str, target, symbol) -> bool:
    if source.isdecimal() and symbol == SYMBOL_GREATER:
        return int(source) > target
    elif source.isdecimal() and symbol == SYMBOL_LESS:
        return int(source) < target
    elif source.isdecimal() and symbol == SYMBOL_GREATER_EQUAL:
        return int(source) >= target
    elif source.isdecimal() and symbol == SYMBOL_LESS_EQUAL:
        return int(source) <= target
    elif symbol == SYMBOL_MATCH:
        return re.fullmatch(target, source) is not None
    elif symbol == SYMBOL_EQUALS:
        return source == target
    elif symbol == SYMBOL_NOT_EQUALS:
        return source != target
    return False


def _validate_operator(source, target, operator) -> bool:
    if operator == OPERATOR_AND:
        for sub_target in target:
            if not validate(source, sub_target):
                return False
        return True
    elif operator == OPERATOR_OR:
        for sub_target in target:
            if validate(source, sub_target):
                return True
        return False
    elif operator == OPERATOR_NOT:
        return not validate(source, target)
    return False


def build_mock_operator():
    return BaseOperator(OPERATOR_NOT, BaseSymbol(SYMBOL_MATCH, REGEX_ANY_THING))


def build_all_accept_operator():
    return BaseSymbol(SYMBOL_MATCH, REGEX_ANY_THING)


if __name__ == "__main__":
    test_operation = BaseOperator(OPERATOR_OR, [BaseSymbol(SYMBOL_EQUALS, 'giveup'),
                                                BaseSymbol(SYMBOL_MATCH, REGEX_ANY_NUMBER)]).encode()
    print(validate('303', test_operation))
