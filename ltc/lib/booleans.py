from .formula_parser import FormulaParser, Operator

class BooleanParser(FormulaParser):
    operators = {'|': Operator(0, lambda a, b: a or b), 
                 '&': Operator(1, lambda a, b: a and b)
                 }

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