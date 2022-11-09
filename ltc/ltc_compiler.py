try:
    from .ltc_builtins import *
    from .ltc_core import *
except ImportError:
    from ltc_builtins import *
    from ltc_core import *

VERSION = 0.2


class LTC:
    def __init__(self, field_table, namespace, checker_functions):
        self.field_table = field_table
        self.checker_functions = checker_functions
        self.namespace = namespace
        self.executed = False
    
    @classmethod
    def from_dict(cls, data):
        executed = True
        namespace = {}
        field_table = data['field_values']
        checker_functions = []
        for checkerobj in data['checkers']:
            function = KEYWORD_TABLE[checkerobj['function']](*checkerobj['args'])
            field = checkerobj['field']
            checker_functions.append((field, function))
        ltc = cls(field_table, namespace, checker_functions)
        ltc.executed = executed 
        return ltc

    def to_dict(self):
        if not self.executed: self.execute()
        mainobj = {}
        mainobj['field_values'] = self.field_table
        mainobj['checkers'] = []
        for field, checker in self.checker_functions:
            checkerobj = {}
            checkerobj['function'] = INVERSE_TABLE[checker.__class__]
            checkerobj['args'] = checker.args
            checkerobj['field'] = field
            mainobj['checkers'].append(checkerobj)
        return mainobj
    
    def execute(self):
        if self.executed:
            raise Warning('Trying to execute an already executed LTC')
            return

        items = list(self.field_table.items())
        for key, value in items:
            self.field_table[key] = value(ns=self.namespace)
        for _, value in self.checker_functions:
            value.compile(self.namespace)
        self.executed = True
    
    def check(self, fields):
        valid = True
        for field, checker in self.checker_functions:
            print(field, checker.args, fields[field], checker(fields[field]), checker.__dict__)
            valid = valid and checker(fields[field])
        return valid
    

class LTCCompiler:
    def _typevalue(txt):
        txt = txt.strip()
        if txt[-1] == txt[0] == '"':
            txt = txt.strip('"')
            return LTCValue(txt)
        elif txt[-1] == txt[0] == "'":
            txt = txt.strip("'")
            return LTCValue(txt)
        elif txt.isdigit():
            return LTCValue(txt)
        elif txt[0] == '[' and txt[-1] == ']':
            args = txt[1:-1].split(',')
            args = LTCCompiler._combine_kws(args, ',')
            args = [LTCCompiler._typevalue(arg) for arg in args]
            return LTCValue(args)
        elif '(' in txt and txt[-1] == ')':
            return LTCCompiler._build_func(txt)
        else:
            return LTCAllias(txt)

    def _build_func(txt):
        fname = txt[:txt.find('(')]
        try:
            func = KEYWORD_TABLE[fname]
        except KeyError:
            raise LTCCompileError('Unknown function ' + fname + '. Maybe you forgot to import it?')
        args = txt[txt.find('(') + 1:-1].split(',')
        args = LTCCompiler._combine_kws(args, ',')
        fargs = [LTCCompiler._typevalue(arg) for arg in args]
        return func(*fargs)

    def _combine_kws(kws, joiner=' '):
        for i, kw in enumerate(kws):
            if kw is None:
                continue
            kw = kw.strip()
            if kw.startswith('['):
                LTCCompiler._combine_kw(i, '[', ']', kws, joiner)
            elif kw.startswith('"'):
                LTCCompiler._combine_kw(i, '"', '"', kws, joiner)
            elif kw.startswith("'"):
                LTCCompiler._combine_kw(i, "'", "'", kws, joiner)
            elif '(' in kw:
                LTCCompiler._combine_kw(i, '(', ')', kws, joiner)
            
        kws = [kw for kw in kws if kw]
        return kws

    def _combine_kw(origin, opener, closer, kws, joiner=' '):
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
            if ':=' in line:
                linemode = 'contain'
                line = line.replace(':=', ' ')
            elif '=' in line:
                linemode = 'set'
                line = line.replace('=', ' ')
            elif '?' in line:
                linemode = 'check'
                line = line.replace('?', ' ')
            else:
                raise LTCCompileError('LTC line has no known operators: ' + line)
            kws = LTCCompiler._combine_kws(line.strip().split())
            if linemode == 'set':
                try:
                    field = kws[0]
                    value = kws[1]
                    value = LTCCompiler._typevalue(value)
                    field_table[field] = value
                    if 'as' in kws:
                        allias = kws[kws.index('as') + 1]
                        namespace[allias] = value
                except IndexError:
                    raise LTCCompileError('Uncomplete operation: not enough keywords in ' + line)
            elif linemode == 'check':
                try:
                    field = kws[0]
                    checker_functions.append((field, LTCCompiler._build_func(kws[1])))
                except IndexError:
                    raise LTCCompileError('Uncomplete operation: not enough keywords in ' + line)
            elif linemode == 'contain':
                allias = kws[0]
                value = kws[1]
                value = LTCCompiler._typevalue(value)
                namespace[allias] = value
        return LTC(field_table=field_table, 
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
            kws = LTCCompiler._combine_kws(line.strip().split())
            if kws[0] == 'set':
                try: 
                    if 'to' not in kws:
                        raise LTCCompileError('Uncomplete operation: expected "to" keyword in ' + line)
                    field = kws[1]
                    value = kws[kws.index('to') + 1]
                    value = LTCCompiler._typevalue(value)
                    field_table[field] = value
                    if 'as' in kws:
                        allias = kws[kws.index('as') + 1]
                        namespace[allias] = value
                except IndexError:
                    raise LTCCompileError('Uncomplete operation: not enough keywords in ' + line)
            elif kws[0] == 'check':
                try:
                    if 'for' not in kws:
                        raise LTCCompileError('Uncomplete operation: expected "for" keyword in ' + line)
                    field = kws[1]
                    checker_functions.append((field, LTCCompiler._build_func(kws[3])))
                except IndexError:
                    raise LTCCompileError('Uncomplete operation: not enough keywords in ' + line)
            elif kws[0] == 'contain':
                try: 
                    if 'as' not in kws:
                        raise LTCCompileError('Uncomplete operation: expected "as" keyword in ' + line)
                    allias = kws[1]
                    value = kws[kws.index('as') + 1]
                    value = LTCCompiler._typevalue(value)
                    namespace[allias] = value
                except IndexError:
                    raise LTCCompileError('Uncomplete operation: not enough keywords in ' + line)
            
            else:
                raise LTCCompileError('Unknown operation ' + kws[0])        

        return LTC(field_table=field_table, 
                   namespace=namespace, 
                   checker_functions=checker_functions)



if __name__ == '__main__':
    test = '''
aaa := 'bbb'
0 = NaN
id2 = 43 as F3
id1 = GenerateLine(F3, GenerateLine(3, "b"))
id3 = [["я", "список"], GenerateLine(4, "c"), "[я делаю вид, что я список]", 5]

input ? Equal(GenerateLine(F3, GenerateLine(3, "b")))'''

    ltcc = LTCCompiler()
    ltc = ltcc.compile(test)
    print(ltc.field_table)
    ltc.execute()
    print(ltc.field_table)
    print(ltc.check({'input': '42'}))
    print(ltc.check({'input': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'}))
    print(ltc.to_dict())