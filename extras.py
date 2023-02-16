from os import listdir
from os.path import isfile, join

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
        f = cls.__dbmodel__.objects.filter(**criteria)
        if f:
            return cls(f.first())
        else:
            return None
    
    @classmethod
    def by_id(cls, id):
        return cls(cls.__dbmodel__.objects.get(id=id))

    @property
    def id(self):
        return self.dbmodel.id

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def __eq__(self, __t):
        return self.dbmodel.id == __t.dbmodel.id
    
    def close(self):
        if self.modified:
            self.dbmodel.save()

class Scanner:
    '''Class for identifying file within directories by their filenames only,
       without specifying their full paths.'''
    def __init__(self, root):
        self.root = root
        self.table = {}
        self.leaves = []
        self.shoots = []
    
    @staticmethod
    def _scan(roots, id):
        if not roots:
            return -1
        root = roots.pop(0)
        children = listdir(root)
        if id in children:
            return join(root, id)
        ext = []
        for c in children:
            p = join(root, c)
            if not isfile(p):
                ext.append(p)
        return Scanner._scan(roots + ext, id)
    
    def all_shoots(self, use_cache=True):
        if use_cache and self.shoots:
            return self.shoots
        shoots = []
        roots = [self.root]
        while roots:
            root = roots.pop(0)
            children = listdir(root)
            for child in children:
                path = join(root, child)

                grandchildren = listdir(path)
                flag = False
                for grandchild in grandchildren:
                    if isfile(join(path, grandchild)):
                        flag = True
                        break

                if flag:
                    shoots.append(child)
                else:
                    roots.append(path)
        if use_cache:
            self.shoots = shoots
        return shoots

    def all_leaves(self, use_cache=True):
        if use_cache and self.leaves:
            return self.leaves
        leaves = []
        roots = [self.root]
        while roots:
            root = roots.pop(0)
            children = listdir(root)
            for child in children:
                path = join(root, child)
                if isfile(path):
                    leaves.append(child)
                else:
                    roots.append(path)
        if use_cache:
            self.leaves = leaves
        return leaves
        
    def id_to_path(self, id):
        if id not in self.table:
            self.table[id] = Scanner._scan([self.root], id)
        return self.table[id]


def transliterate_ru_en(string) -> str:
    alphabet = {'а': 'a',
                'б': 'b',
                'в': 'v',
                'г': 'g',
                'д': 'd',
                'е': 'ye',
                'ё': 'yo',
                'ж': 'zh',
                'з': 'z',
                'и': 'i',
                'к': 'k',
                'л': 'l',
                'м': 'm',
                'н': 'n',
                'о': 'o',
                'п': 'p',
                'р': 'r',
                'с': 's',
                'т': 't',
                'у': 'u',
                'ф': 'f',
                'х': 'h',
                'ц': 'ts',
                'ч': 'ch',
                'ш': 'sh',
                'щ': 'sch',
                'ъ': '',
                'ы': 'i',
                'ь': "'",
                'э': 'e',
                'ю': 'yu',
                'я': 'ya'}
    out = ''
    for letter in string:
        ll = letter.lower()
        if ll not in alphabet:
            out += letter
            continue
        add = alphabet[ll]
        if letter.isupper():
            out += add.upper()
        else:
            out += add
    return out


def asciify(string):
    return transliterate_ru_en(string).encode('ascii', 'replace').decode('ascii')