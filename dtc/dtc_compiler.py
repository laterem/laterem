from dtc_builtins import *
from dtc_core import *

class DTC:
    def __init__(self, field_table, checker_functions):
        self.field_table = field_table
        self.checker_functions = checker_functions
        self.executed = False
    
    def execute(self):
        if self.executed:
            raise Warning('Trying to execute an already executed DTC')
            return

        items = list(self.field_table.items())
        for key, value in items:
            self.field_table[key] = value()
        self.executed = True
        

class DTCCompiler:
    def compile(self, txt):
        namespace = {}
        field
        code = txt.split('\n')
            
        for line in code:
            line = line[:line.find('#')].strip()
            if not line:
                continue
            kws = line.strip().split()
            if kws[0] == 'set':
                assert 'to' in kws and len(kws) >= 4

            
            
            
            
            
            """ for s in line:
                eol = (s == '\n')
                if mode == 0:
                    if s == '=':
                        tmpfields['field'] = tmpfields['currobj']
                        rs('currobj')
                        mode = 1
                        continue
                    tmpfields['currobj'] += s
                elif mode == 1:
                    if eol:
                        namespace[tmpfields['field']] = DTCObject(tmpfields['currobj'])
                        mode = 0
                        rs('currobj')
                        rs('field')
                        continue
                    tmpfields['currobj'] += s """
                    