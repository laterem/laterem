from .formula_parser import FormulaParser, Operator

class BooleanParser(FormulaParser):
    operators = {'|': Operator(0, lambda a, b: a or b), 
                 '&': Operator(1, lambda a, b: a and b), 
                 '!': Operator(2, lambda a: not a, 1)
                 }

    @staticmethod
    def object_convert(string, variables):
        if string in variables:
            return variables[string]
        else:
            return bool(int(string))

    @staticmethod
    def object_validation(string):
        if not string.strip():
            return False
        return True

    @staticmethod
    def object_identification(symbol, carry):
        VARIABLE = 'abcdefghijklmnopqrstuvwxyz'
        VARIABLE += VARIABLE.upper()
        NUMBER = '10' 
        if symbol in VARIABLE or symbol in NUMBER:
            return True
        return False