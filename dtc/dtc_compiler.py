try:
    from .dtc_builtins import *
    from .dtc_core import *
except ImportError:
    from dtc_builtins import *
    from dtc_core import *

VERSION = 0.2
# Set objects cannot be part of another set objects. Needs fixing?


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
        txt = txt.strip()
        if txt[-1] == txt[0] == '"':
            txt = txt.strip('"')
            return DTCValue(txt)
        elif txt.isdigit():
            return DTCValue(txt)
        elif txt[0] == '[' and txt[-1] == ']':
            args = txt[1:-1].split(',')
            args = DTCCompiler._combine_kws(args, ',')
            args = {DTCCompiler._typevalue(arg) for arg in args}
            return DTCValue(args)
        elif '(' in txt and txt[-1] == ')':
            return DTCCompiler._build_func(txt)
        else:
            return DTCAllias(txt)

    def _build_func(txt):
        fname = txt[:txt.find('(')]
        try:
            func = KEYWORD_TABLE[fname]
        except KeyError:
            raise DTCCompileError('Unknown function ' + fname + '. Maybe you forgot to import it?')
        args = txt[txt.find('(') + 1:-1].split(',')
        args = DTCCompiler._combine_kws(args, ',')
        fargs = [DTCCompiler._typevalue(arg) for arg in args]
        return func(*fargs)

    def _combine_kws(kws, joiner=' '):
        for i, kw in enumerate(kws):
            if kw is None:
                continue
            kw = kw.strip()
            if kw.startswith('['):
                DTCCompiler._combine_kw(i, '[', ']', kws, joiner)
            elif kw.startswith('"'):
                DTCCompiler._combine_kw(i, '"', '"', kws, joiner)
            elif '(' in kw:
                DTCCompiler._combine_kw(i, '(', ')', kws, joiner)
            
        kws = [kw for kw in kws if kw]
        return kws

    def _combine_kw(origin, opener, closer, kws, joiner=' '):
        print(kws)
        kw = kws[origin]
        ff = kw
        if opener != closer:
            runf = lambda _: ff.count(opener) != ff.count(closer) 
        else:
            runf = lambda _: ff.count(opener) % 2 != 0
        i = origin
        while runf(...):
            i += 1
            ff += joiner + kws[i]
            kws[i] = None
        kws[origin] = ff

    def compile(self, txt):
        COMPILER_VERSION = 0.2
        if COMPILER_VERSION != VERSION:
            raise NotImplemented

        namespace = {}
        field_table = {}
        checker_functions = []
        if txt[:9] == '[VERBAL]\n':
            return self.compile_alt(txt[9:])

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
            kws = DTCCompiler._combine_kws(line.strip().split())
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


    def compile_alt(self, txt):
        COMPILER_VERSION = 0.2
        if COMPILER_VERSION != VERSION:
            raise NotImplemented

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
            kws = DTCCompiler._combine_kws(line.strip().split())
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
id0 = "Foo bar"
id2 = 43 as F3
id1 = GenerateLine(F3, GenerateLine(3, "b"))
id3 = [GenerateLine(3, "b"), GenerateLine(4, "c"), "[я делаю вид, что я список]", 5]

input ? Equal(F3)'''

    dtcc = DTCCompiler()
    dtc = dtcc.compile(test)
    print(dtc.field_table)
    dtc.execute()
    print(dtc.field_table)
    print(dtc.check({'input': '42'}))
    print(dtc.check({'input': '43'}))