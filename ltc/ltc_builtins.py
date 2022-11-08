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
        print(r)
        return sqrt(self.args[0] ** 2 + self.args[1] ** 2)

class QuadEquation(LTCFunction):
    expected_argsc = 3
    def call(self):
        print(self.args)
        a, b, c = self.args
        out = ''
        if a:
            if abs(a) != 1:
                out += str(abs(a))
            elif a == -1:
                out += '-'
            out += 'x²'
        if b:
            if b > 0:
                out += ' + '
            else:
                out += ' - '
            if abs(b) != 1:
                out += str(abs(b))
            out += 'x'
        if c:
            if c > 0:
                out += ' + '
            else:
                out += ' - '
            if abs(c) != 1:
                out += str(abs(c))
        out += ' = 0'
        return out
        
class IsMetricEqual(LTCCheckerFunction):
    expected_argsc = 2
    def call(self, field):
        return field.endswith(self.args[1]) and field.strip(self.args[1]) == self.args[0]

class Round(LTCFunction):
    expected_argsc = 2
    def call(self):
        r = round(float(self.args[0]), int(self.args[1]))
        print(r)
        return r

class IsEqual(LTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        if isinstance(self.args[0], list):
            return sorted(field) == sorted(self.args[0])
        return field == self.args[0]

class IsEqualSum(LTCCheckerFunction):
    expected_argsc = 2
    def call(self, field):
        return int(field) == int(self.args[0]) + int(self.args[1])

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
    expected_argsc = 3
    def __init__(self, *args):
        super().__init__(*args)
        a, b, c = args
        D = b*b - 4 * a * c
        if D >= 0:
            sqrtd = sqrt(D)
            a2 = 2*a
            x1 = (sqrtd-b)/a2
            x2 = (-sqrtd-b)/a2
            self._roots = (str(x1), str(x2))
        else:
            self._roots = ("нет корней",)

    def call(self, field):
        return field in self._roots


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