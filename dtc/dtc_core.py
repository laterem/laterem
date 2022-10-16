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
    compiled = False

    def __init__(self, *args):
        argsc = len(args)
        if argsc != self.expected_argsc:
            raise DTCCompileError(f'{type(self).__name__} expected {self.expected_argsc} arguments, {argsc} were given.')
        self.args = list(args)

    def __call__(self, ns):
        if not self.compiled: self.compile(ns)
        if self.result is NResult:
            self.result = self.call()
        return self.result
    
    def compile(self, ns):
        for i, arg in enumerate(self.args):
            if isinstance(arg, str):
                continue
            elif isinstance(arg, list):
                self.args[i] = [a(ns) for a in arg]
            else:
                self.args[i] = arg(ns)
        self.compiled = True

class DTCCheckerFunction(DTCFunction):
    def __call__(self, field):
        return self.call(field)

class DTCValue(DTCFunction):
    expected_argsc = 1    
    def call(self):
        return self.args[0]

class DTCAllias:
    def __init__(self, name):
        self.name = name
    
    def __call__(self, ns):
        return ns[self.name](ns)