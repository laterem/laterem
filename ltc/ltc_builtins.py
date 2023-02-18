try:
    from .ltc_core import *
    from .lib.formula_parser import FormulaParser
except ImportError:
    from ltc_core import *
    from lib.formula_parser import FormulaParser

from random import randint
import random
from math import sqrt, copysign, fabs, floor, isfinite, modf

# Подключение пакетов
try:
    from .lib.booleans import *
except ImportError:
    from lib.booleans import *

def call_ltc_function(function, *args):
    func = function(*args)
    return func()

class FloatBin(LTCFunction):
    expected_argsc = 2
    def call(self):
        f = float(self.args[0])
        tail = int(self.args[1])
        if not isfinite(f):
            return repr(f)  # inf nan

        sign = '-' * (copysign(1.0, f) < 0)
        frac, fint = modf(fabs(f))  # split on fractional, integer parts
        n, d = frac.as_integer_ratio()  # frac = numerator / denominator
        assert d & (d - 1) == 0  # power of two
        fract = f'{n:0{d.bit_length()-1}b}'
        return f'{sign}{floor(fint):b}.{fract[:tail]}'

class ConvertBase(LTCFunction):
    expected_argsc = 4
    # num, base_from, base_to
    def call(self):
        _ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        _POINT = '.'
        def _int_to_base(number, new_base):
            sign = -1 if number < 0 else 1
            number *= sign
            ans = ''
            while number:
                ans += _ALPHABET[number % new_base]
                number //= new_base
            if sign == -1:
                ans += '-'
            return ans[::-1]
        num, base_from, base_to, precision = self.args
        num = str(num)
        base_from = int(base_from)
        base_to = int(base_to)
        integral, point, fractional = num.strip().partition(_POINT)
        num = int(integral + fractional, base_from) * base_from ** -len(fractional)
        precision = len(fractional) if precision is None else int(precision)
        s = _int_to_base(int(round(num / base_to ** -precision)), base_to)
        part = s[-precision:]
        if precision and int(part):
            return s[:-precision] + _POINT + part
        else:
            return s

class GenerateLine(LTCFunction):
    expected_argsc = 2    
    def call(self):
        return self.args[1] * int(self.args[0])

class RandomNum10(LTCFunction):
    expected_argsc = 2    
    def call(self):
        random.seed(self.metadata.seed)
        self.metadata.tick_seed()
        return randint(int(self.args[0]), int(self.args[1]))

class RandomNum2(LTCFunction):
    expected_argsc = 2    
    def call(self):
        random.seed(self.metadata.seed)
        self.metadata.tick_seed()
        n10 = randint(int(self.args[0]), int(self.args[1]))
        return call_ltc_function(ConvertBase, n10, 10, 2)

class RandomFloat10(LTCFunction):
    expected_argsc = 3    
    def call(self):
        random.seed(self.metadata.seed)
        self.metadata.tick_seed()
        percision = 10**int(self.args[2])
        return randint(int(float(self.args[0]) * percision), int(float(self.args[1]) * percision)) / percision

class RandomFloat2(LTCFunction):
    expected_argsc = 3    
    def call(self):
        random.seed(self.metadata.seed)
        self.metadata.tick_seed()
        percision = 2**int(self.args[2])
        fl10 = randint(int(float(self.args[0]) * percision), int(float(self.args[1]) * percision)) / percision
        return call_ltc_function(ConvertBase, fl10, 10, 2)

class ReverseList(LTCFunction):
    expected_argsc = 1
    def call(self):
        return list(reversed(self.args[0]))

class Veclen(LTCFunction):
    expected_argsc = 2
    def call(self):
        r = sqrt(self.args[0] ** 2 + self.args[1] ** 2)
        return sqrt(self.args[0] ** 2 + self.args[1] ** 2)

class QuadEquation(LTCFunction):
    expected_argsc = 3
    def call(self):
        a, b, c = self.args
        out = ''
        if a:
            if a < 0:
                out += '-'
            if abs(a) != 1:
                out += str(abs(a))
            out += 'x²'
            if b > 0:
                out += ' + '
        if b:
            if b < 0:
                out += ' - '
            if abs(b) != 1:
                out += str(abs(b))
            out += 'x'
            if c > 0:
                out += ' + '
        if c:
            if c < 0:
                out += ' - '
            out += str(abs(c))
        out += ' = 0'
        return out
        
class IsMetricEqual(LTCCheckerFunction):
    expected_argsc = 2
    def call(self, field):
        return field.endswith(self.args[1]) and float(field.strip(self.args[1])) == self.args[0]

class Sum(LTCFunction):
    expected_argsc = 2
    def call(self):
        return float(self.args[0]) + float(self.args[1])

class Multiply(LTCFunction):
    expected_argsc = 2
    def call(self):
        return float(self.args[0]) * float(self.args[1])

class Divide(LTCFunction):
    expected_argsc = 2
    def call(self):
        return float(self.args[0]) / float(self.args[1])

class Mod(LTCFunction):
    expected_argsc = 2
    def call(self):
        return float(self.args[0]) % float(self.args[1])

class Power(LTCFunction):
    expected_argsc = 2
    def call(self):
        return float(self.args[0]) ** float(self.args[1])

class Substract(LTCFunction):
    expected_argsc = 2
    def call(self):
        return float(self.args[0]) - float(self.args[1])

class Round(LTCFunction):
    expected_argsc = 2
    def call(self):
        try:
            r = round(float(self.args[0]), int(self.args[1]))
            return r
        except ValueError:
            return self.args[0]

class Calc(LTCFunction):
    expected_argsc = 1
    def call(self):
        string = self.args[0]
        return FormulaParser().eval(string)

class IsEqual(LTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        try:
            if isinstance(self.args[0], list):
                return sorted(field) == sorted(self.args[0])
            try:
                return float(field) == float(self.args[0])
            except ValueError:
                return str(field) == str(self.args[0])
        except ValueError:
            return False

class IsEqualSet(LTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        return set(self.args[0]) == set(field)

class IsEqualText(LTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        return field.strip().lower().replace('ё', 'е') == str(self.args[0]).strip().lower().replace('ё', 'е')

class IsNotEqual(LTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        if isinstance(self.args[0], list):
            return sorted(field) != sorted(self.args[0])
        return field != self.args[0]

class IsReversed(LTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        return field == self.args[0][::-1]

class Roots(LTCCheckerFunction):
    expected_argsc = 4
    def call(self, field):
        a, b, c, accuracy = self.args
        try:
            inp = float(field)
        except ValueError:
            return False

        accuracy = int(accuracy)
        if not a:
            return inp == round(-b/c, accuracy)
        D = b*b - 4 * a * c
        if D >= 0:
            sqrtd = sqrt(D)
            a2 = 2*a
            x1 = (sqrtd-b)/a2
            x2 = (-sqrtd-b)/a2
            _roots = (round(x1, accuracy), round(x2, accuracy))
            return inp in _roots
        else:
            return field.strip().lower() == 'нет корней'


builtintable = {
    'GenerateLine': GenerateLine,
    'Equal': IsEqual,
    'EqualText': IsEqualText,
    'EqualSet': IsEqualSet,
    'NotEqual': IsNotEqual,
    'Sum': Sum,
    'Multiply': Multiply,
    'Divide': Divide,
    'Mod': Mod,
    'Power': Power, 
    'Substract': Substract,
    'Reversed': IsReversed,
    'Reverse': ReverseList,
    'Roots': Roots,
    'QuadEquation': QuadEquation,
    'Veclen': Veclen,
    'MetricEqual': IsMetricEqual,
    'Round': Round,
    'ConvertBase': ConvertBase,
    'Calc': Calc, 
    'Rand10': RandomNum10,
    'Rand2': RandomNum2,
    'RandFloat10': RandomFloat10,
    'RandFloat2': RandomFloat2,
}

register_function(**builtintable)