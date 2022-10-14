class DTCCompileError(Exception):
    pass

class DTCObject:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value

NResult = object()

class DTCFunction:
    expected_argsc = 0
    result = NResult

    def __init__(self, *args):
        argsc = len(args)
        if argsc != self.expected_argsc:
            raise DTCCompileError(f'{type(self).__name__} expected {self.expected_argsc} arguments, {argsc} were given.')
        self.args = args

    def getarg(self, ns, n):
        arg = self.args[n]
        if isinstance(arg, str):
            return arg
        elif isinstance(arg, list):
            return [a(ns) for a in arg]
        else:
            return arg(ns)

    def __call__(self, ns):
        if self.result is NResult:
            self.result = self.call(ns)
        return self.result

class DTCCheckerFunction(DTCFunction):
    def __call__(self, field, ns):
        return self.call(field, ns)

class DTCValue(DTCFunction):
    expected_argsc = 1    
    def call(self, ns):
        return self.getarg(ns, 0)

class DTCAllias:
    def __init__(self, name):
        self.name = name
    
    def __call__(self, ns):
        return ns[self.name](ns)