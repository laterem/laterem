class NotSpecified:
    def __bool__(self):
        return False

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


class Hybrid:
    ready = False

    def __init__(self):
        self.__sources = set()
        self.ready = True

    def source_from(self, obj):
        self.__sources.add(obj)
    
    def __setattr__(self, name, val):
        if not self.ready:
            object.__setattr__(self, name, val)
        for src in self.__sources:
            if hasattr(src, name):
                return src.__setattr__(name, val)
        else:
            object.__setattr__(self, name, val)

    def __getattr__(self, name):
        for src in self.__sources:
            if hasattr(src, name):
                return src.__getattribute__(name)
        else:
            raise AttributeError(f"{name} not found neither in {self.__class__.__name__} hybrid-like class itself, nor in any of it's sources.")

class DBHybrid(Hybrid):
    __dbmodel__ = None

    def __init__(self, dbobj):
        super().__init__()
        self.dbmodel = dbobj
        self.source_from(dbobj)
        self.modified = False
    
    @classmethod
    def get(cls, **criteria):
        return cls(cls.__dbmodel__.objects.get(**criteria))
    
    @classmethod
    def by_id(cls, id):
        return cls(cls.__dbmodel__.objects.get(id=id))

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def __eq__(self, __t):
        return self.dbmodel.id == __t.dbmodel.id
    
    def close(self):
        if self.modified:
            self.dbmodel.save()