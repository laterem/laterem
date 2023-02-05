try:
    from extratypes import NotSpecified
except ModuleNotFoundError:
    NotSpecified = object()

class Operator:
    def __init__(self, priority, function):
        self.priority = priority
        self.function = function

    def __call__(self, *args):
        return self.function(*args)


class FormulaParser:
    # Based on the tutorial from https://habr.com/ru/post/273253/
    # To be reworked

    operators = {'+': Operator(0, lambda a, b: a + b), 
                 '-': Operator(0, lambda a, b: a - b), 
                 '*': Operator(1, lambda a, b: a * b), 
                 '/': Operator(1, lambda a, b: a / b), 
                 '^': Operator(2, lambda a, b: pow(a, b))}

    @staticmethod
    def object_convert(string, variables):
        if string in variables:
            return variables[y]
        else:
            return float(string)

    @staticmethod
    def object_validation(string):
        if not string.strip():
            return False

        UNARY_OPERATORS = '-'
        for op in UNARY_OPERATORS:
            if string.strip() == op:
                return False
        return True

    @staticmethod
    def object_identification(symbol, carry):
        VARIABLE = 'abcdefghijklmnopqrstuvwxyz'
        VARIABLE += VARIABLE.upper()

        NUMBER = '1234567890'
        UNARY_PREFIX = '-'
        PERIOD = '.' 

        clean = not carry
        is_variable = (not clean) and carry.isalpha()
        cndot = carry.replace('.', '')
        is_number = (not clean) and (len(cndot) == 1 or cndot[1:].isdigit()) and (carry[0] in NUMBER or carry[0] in UNARY_PREFIX)
        
        if (is_variable or clean) and symbol in VARIABLE:
            return True
        if (is_number or clean) and symbol in NUMBER:
            return True
        if clean and symbol in UNARY_PREFIX:
            return True
        if (is_number) and (PERIOD not in carry) and symbol == PERIOD:
            return True
        return False

    @classmethod
    def _raw_parse(cls, formula_string):
        number = ''
        for s in formula_string:
            # Проверка на то, является ли символ частью математического объекта (числа)
            if cls.object_identification(s, number):
                number += s  
            else:
                # Дополнительная проверка на то, является ли собранное число 
                # корректным объектом (защита от ложного определения дуальных операторов
                # частью конструкций с унарными)
                if cls.object_validation(number): 
                    yield number
                    number = ''
                else:
                    # В случае ошибки, проверка на то, не был ли потерян оператор 
                    if len(number.strip()) and (number in cls.operators or number in "()"): 
                        yield number 
                    number = ''
                # Если символ являтся оператором, отправить его в стэк
                if s in cls.operators or s in "()": 
                    yield s 
        if number: 
            yield number
    
    @classmethod
    def _polish(cls, parsed_formula):
        stack = []  
        for token in parsed_formula:
            if token in cls.operators: 
                while stack and stack[-1] != "(" and cls.operators[token].priority <= cls.operators[stack[-1]].priority:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()
        
    @classmethod
    def _calc(cls, polish, variables=NotSpecified):
        if variables is NotSpecified:
            variables = {}
        stack = []
        for token in polish:
            if token in cls.operators: 
                y, x = stack.pop(), stack.pop()
                x, y = cls.object_convert(x, variables), cls.object_convert(y, variables)
                stack.append(cls.operators[token](x, y)) 
            else:
                stack.append(token)
        return stack[0]

    def eval(self, string, variables=NotSpecified):
        ps = self.polish_stack(string)
        return self._calc(ps,
                          variables=variables)
    
    def polish_stack(self, string):
        return self._polish(self._raw_parse(string))