from random import randint
from dtc_core import *

class GenerateLine(DTCFunction):
    expected_argsc = 1    
    def call(self, ns):
        return '-' * int(self.getarg(ns, 0))

class IsEqual(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, field, ns):
        return field == self.getarg(ns, 0)

class IsNotEqual(DTCCheckerFunction):
    expected_argsc = 1
    def call(self, field, ns):
        return field != self.getarg(ns, 0)

KEYWORD_TABLE = {
    'GenerateLine': GenerateLine,
    'Equal': IsEqual,
    'NotEqual': IsNotEqual
}