class DTCCompileError(Exception):
    pass

class DTCObject:
    # Временно: каждый объект хранится в виде строки
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class DTCFunction:
    expected_argsc = 0

    def __init__(self, *args):
        argsc = len(args)
        if argsc != self.expected_argsc:
            raise DTCCompileError(f'{type(self).__name__} expected {self.expected_argsc} arguments, {argsc} were given.')
        self.args = args

    def __call__(self):
        pass

class DTCValue(DTCFunction):
    expected_argsc = 1    
    def __call__(self):
        return self.args[0]

class DTCAllias:
    def __init__(self, name):
        self.name = name