class Literal:
    value = None

    def set(self, value):
        self.value = value
    
    def get(self):
        return self.value

    def __str__(self):
        return str(self.value)

class Flag:
    @classmethod
    def new(cls):
        return cls({object()})

    def __init__(self, chain):
        self.chain = chain
    
    def __or__(self, __t):
        chain = self.chain.union(__t.chain)
        return Flag(chain)
    
    def __contains__(self, __t):
        return __t.chain <= self.chain