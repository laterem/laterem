try:
    from .dtc_core import *
except ImportError:
    from dtc_core import *

from random import randint

class GenerateLine(DTCFunction):
    expected_argsc = 2    
    def call(self):
        return self.args[1] * int(self.args[0])

class RandomNum10(DTCFunction):
    expected_argsc = 2    
    def call(self):
        return randint(int(self.args[0]), int(self.args[1]))

class IsEqual(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        if isinstance(self.args[0], list):
            return sorted(field) == sorted(self.args[0])
        return field == self.args[0]

class IsEqualSum(DTCCheckerFunction):
    expected_argsc = 2
    def call(self, field):
        return int(field) == int(self.args[0]) + int(self.args[1])

class IsNotEqual(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        if isinstance(self.args[0], list):
            return sorted(field) != sorted(self.args[0])
        return field != self.args[0]

class IsReversed(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, field):
        return field == self.args[0][::-1]

class ReverseList(DTCCheckerFunction):
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