class LTCCompileError(Exception):
    pass

class LTCObject:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value

NResult = object()

class LTCFunction:
    expected_argsc = 0
    result = NResult
    compiled = False
    _is_checker = False

    def __init__(self, *args):
        argsc = len(args)
        if argsc != self.expected_argsc:
            raise LTCCompileError(f'{type(self).__name__} expected {self.expected_argsc} arguments, {argsc} were given.')
        self.args = list(args)

    def __call__(self, ns):
        if not self.compiled: self.compile(ns)
        if self.result is NResult:
            self.result = self.call()
        return self.result
    
    def compile(self, ns):
        for i, arg in enumerate(self.args):
            if callable(arg):
                self.args[i] = arg(ns)
            elif isinstance(arg, list):
                self.args[i] = [a(ns) for a in arg]
            else:
                continue
        self.compiled = True

class LTCCheckerFunction(LTCFunction):
    _is_checker = True

    def __call__(self, field):
        return self.call(field)

class LTCValue(LTCFunction):
    expected_argsc = 1    
    def call(self):
        return self.args[0]

class LTCAllias:
    def __init__(self, name):
        self.name = name
    
    def __call__(self, ns):
        r = ns[self.name]
        if callable(r):
            return r(ns)
        else:
            return r