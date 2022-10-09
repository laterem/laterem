from random import randint
from dtc_core import *

class GenerateLine(DTCFunction):
    expected_argsc = 1    
    def __call__(self):
        return '-' * self.args[0]

KEYWORD_TABLE = {'GenerateLine': GenerateLine}