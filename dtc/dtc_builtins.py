try:
    from .dtc_core import *
except ImportError:
    from dtc_core import *

from random import randint

class GenerateLine(DTCFunction):
    expected_argsc = 2    
    def call(self, ns):
        return self.getarg(ns, 1) * int(self.getarg(ns, 0))

class RandomNum10(DTCFunction):
    expected_argsc = 2    
    def call(self, ns):
        return randint(int(self.getarg(ns, 0)), int(self.getarg(ns, 1)))

class IsEqual(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, field, ns):
        return field == self.getarg(ns, 0)

class IsEqualSum(DTCCheckerFunction):
    expected_argsc = 2
    def call(self, field, ns):
        return int(field) == int(self.getarg(ns, 0)) + int(self.getarg(ns, 1))

class IsNotEqual(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, field, ns):
        return field != self.getarg(ns, 0)

class IsReversed(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, field, ns):
        return field == self.getarg(ns, 0)[::-1]

class ReverseList(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, ns):
        return reversed(self.getarg(ns, 0))

KEYWORD_TABLE = {
    'GenerateLine': GenerateLine,
    'Equal': IsEqual,
    'NotEqual': IsNotEqual,
    'Rand10': RandomNum10,
    'Sum': IsEqualSum,
    'Reversed': IsReversed,
    'Reverse': ReverseList
}