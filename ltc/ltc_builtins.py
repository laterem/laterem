try:
    from .ltc_core import *
except ImportError:
    from ltc_core import *

from random import randint
from math import sqrt

class GenerateLine(LTCFunction):
    expected_argsc = 2    
    def call(self):
        return self.args[1] * int(self.args[0])

class RandomNum10(LTCFunction):
    expected_argsc = 2    
    def call(self):
        return randint(int(self.args[0]), int(self.args[1]))

class ReverseList(LTCFunction):
    expected_argsc = 1
    def call(self):
        return reversed(self.args[0])

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

class Round(LTCFunction):
    expected_argsc = 2
    def call(self):
        r = round(float(self.args[0]), int(self.args[1]))
        return r

class IsEqual(LTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        if isinstance(self.args[0], list):
            return sorted(field) == sorted(self.args[0])
        return field == str(self.args[0])

class IsEqualSum(LTCCheckerFunction):
    expected_argsc = 2
    def call(self, field):
        return float(field) == float(self.args[0]) + float(self.args[1])

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
        accuracy = int(accuracy)
        if not a:
            return float(field) == round(-b/c, accuracy)
        D = b*b - 4 * a * c
        print(a, b, c, D)
        if D >= 0:
            sqrtd = sqrt(D)
            a2 = 2*a
            x1 = (sqrtd-b)/a2
            x2 = (-sqrtd-b)/a2
            _roots = (round(x1, accuracy), round(x2, accuracy))
            return float(field) in _roots
        else:
            return field.strip().lower() == 'нет корней'


KEYWORD_TABLE = {
    'GenerateLine': GenerateLine,
    'Equal': IsEqual,
    'NotEqual': IsNotEqual,
    'Rand10': RandomNum10,
    'Sum': IsEqualSum,
    'Reversed': IsReversed,
    'Reverse': ReverseList,
    'Roots': Roots,
    'QuadEquation': QuadEquation,
    'Veclen': Veclen,
    'MetricEqual': IsMetricEqual,
    'Round': Round
}

INVERSE_TABLE = dict((v,k) for k,v in KEYWORD_TABLE.items())