try:
    from .ltc_core import *
except ImportError:
    from ltc_core import *

from random import randint

class GenerateLine(LTCFunction):
    expected_argsc = 2    
    def call(self):
        return self.args[1] * int(self.args[0])

class RandomNum10(LTCFunction):
    expected_argsc = 2    
    def call(self):
        return randint(int(self.args[0]), int(self.args[1]))

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

class ReverseList(LTCCheckerFunction):
    expected_argsc = 1
    def call(self):
        return reversed(self.args[0])

KEYWORD_TABLE = {
    'GenerateLine': GenerateLine,
    'Equal': IsEqual,
    'NotEqual': IsNotEqual,
    'Rand10': RandomNum10,
    'Sum': IsEqualSum,
    'Reversed': IsReversed,
    'Reverse': ReverseList
}

INVERSE_TABLE = dict((v,k) for k,v in KEYWORD_TABLE.items())