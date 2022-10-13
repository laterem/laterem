try:
    from .dtc_builtins import *
    from .dtc_core import *
except ImportError:
    from dtc_builtins import *
    from dtc_core import *

class DTC:
    def __init__(self, field_table, namespace, checker_functions):
        self.field_table = field_table
        self.checker_functions = checker_functions
        self.namespace = namespace
        self.executed = False
    
    def execute(self):
        if self.executed:
            raise Warning('Trying to execute an already executed DTC')
            return

        items = list(self.field_table.items())
        for key, value in items:
            self.field_table[key] = value(ns=self.namespace)
        self.executed = True
    
    def check(self, fields):
        valid = True
        for field, checker in self.checker_functions:
            valid = valid and checker(fields[field], self.namespace)
        return valid
    

class DTCCompiler:
    def _typevalue(txt):
        if txt[-1] == txt[0] == '"':
            txt = txt.strip('"')
            return DTCValue(txt)
        elif txt.isdigit():
            return DTCValue(txt)
        elif '(' in txt and ')' in txt:
            return DTCCompiler._build_func(txt)
        else:
            return DTCAllias(txt)

    def _build_func(txt):
        fname = txt[:txt.find('(')]
        try:
            func = KEYWORD_TABLE[fname]
        except KeyError:
            raise DTCCompileError('Unknown function ' + fname + '. Maybe you forgot to import it?')
        args = txt[txt.find('(') + 1:txt.find(')')].split(',')
        fargs = [DTCCompiler._typevalue(arg) for arg in args]
        return func(*fargs)

    def compile_shortstyle(self, txt):
        namespace = {}
        field_table = {}
        checker_functions = []
        code = txt.split('\n')
        for line in code:
            if '#' in line:
                line = line[:line.find('#')]
            line = line.strip()
            if not line:
                continue

            if '=' in line:
                linemode = 'set'
                line = line.replace('=', ' ')
            elif '?' in line:
                linemode = 'check'
                line = line.replace('?', ' ')
            else:
                raise DTCCompileError('DTC line has no known operators: ' + line)

            kws = line.strip().split()
            for i, kw in enumerate(kws):
                if kw is None:
                    continue
                if '(' in kw:
                    ff = kw
                    origin = i
                    while ')' not in ff:
                        i += 1
                        ff += kws[i]
                        kws[i] = None
                    kws[origin] = ff
                elif '"' in kw:
                    ffs = [kw]
                    origin = i
                    foundpair = kw.count('"') >= 2
                    while not foundpair:
                        i += 1
                        ffs.append(kws[i])
                        foundpair = '"' in ffs[-1]
                        kws[i] = None
                    kws[origin] = ' '.join(ffs)
            kws = [kw for kw in kws if kw]
            if linemode == 'set':
                try:
                    field = kws[0]
                    value = kws[1]
                    value = DTCCompiler._typevalue(value)
                    field_table[field] = value
                    if 'as' in kws:
                        allias = kws[kws.index('as') + 1]
                        namespace[allias] = value
                except IndexError:
                    raise DTCCompileError('Uncomplete operation: not enough keywords in ' + line)
            elif linemode == 'check':
                try:
                    field = kws[0]
                    checker_functions.append((field, DTCCompiler._build_func(kws[1])))
                except IndexError:
                    raise DTCCompileError('Uncomplete operation: not enough keywords in ' + line)
        
        return DTC(field_table=field_table, 
                   namespace=namespace, 
                   checker_functions=checker_functions)


    def compile(self, txt):
        namespace = {}
        field_table = {}
        checker_functions = []
        code = txt.split('\n')
        for line in code:
            if '#' in line:
                line = line[:line.find('#')]
            line = line.strip()
            if not line:
                continue
            kws = line.strip().split()
            for i, kw in enumerate(kws):
                if kw is None:
                    continue
                if '(' in kw:
                    ff = kw
                    origin = i
                    while ')' not in ff:
                        i += 1
                        ff += kws[i]
                        kws[i] = None
                    kws[origin] = ff
                elif '"' in kw:
                    ffs = [kw]
                    origin = i
                    foundpair = kw.count('"') >= 2
                    while not foundpair:
                        i += 1
                        ffs.append(kws[i])
                        foundpair = '"' in ffs[-1]
                        kws[i] = None
                    kws[origin] = ' '.join(ffs)
            kws = [kw for kw in kws if kw]
            if kws[0] == 'set':
                try: 
                    if 'to' not in kws:
                        raise DTCCompileError('Uncomplete operation: expected "to" keyword in ' + line)
                    field = kws[1]
                    value = kws[kws.index('to') + 1]
                    value = DTCCompiler._typevalue(value)
                    field_table[field] = value
                    if 'as' in kws:
                        allias = kws[kws.index('as') + 1]
                        namespace[allias] = value
                except IndexError:
                    raise DTCCompileError('Uncomplete operation: not enough keywords in ' + line)
            elif kws[0] == 'check':
                try:
                    if 'for' not in kws:
                        raise DTCCompileError('Uncomplete operation: expected "for" keyword in ' + line)
                    field = kws[1]
                    checker_functions.append((field, DTCCompiler._build_func(kws[3])))
                except IndexError:
                    raise DTCCompileError('Uncomplete operation: not enough keywords in ' + line)
            else:
                raise DTCCompileError('Unknown operation ' + kws[0])        

        return DTC(field_table=field_table, 
                   namespace=namespace, 
                   checker_functions=checker_functions)



if __name__ == '__main__':

    test = '''
set id0 to "Foo bar" as foo
set id1 to foo
set id2 to 42 as num
set id3 to GenerateLine(5, "a" )
set id4 to GenerateLine(num, "b" ) as bs #Big Spidz 
set id5 to bs


# Hello world! 

check input for Equal("foobar")
check input1 for Equal(123)'''

    dtcc = DTCCompiler()
    dtc = dtcc.compile(test)
    print(dtc.field_table)
    dtc.execute()
    print(dtc.field_table)
    print(dtc.check({'input': 'baz', 'input1': "123"}))
    print(dtc.check({'input': 'foobar', 'input1': "123"}))

    test = '''
id0="Foo bar"
id2= 43 as F3
id1 = GenerateLine(F3, "c")

input?Equal(F3)'''

    dtcc = DTCCompiler()
    dtc = dtcc.compile_shortstyle(test)
    print(dtc.field_table)
    dtc.execute()
    print(dtc.field_table)
    print(dtc.check({'input': '42'}))
    print(dtc.check({'input': '43'}))