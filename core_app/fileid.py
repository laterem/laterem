from os import listdir
from os.path import isfile, join

'''Module for identifying file within directories by their filenames only,
without specifying their full paths.'''

class Scanner:
    def __init__(self, root):
        self.root = root
        self.table = {}
    
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

    def id_to_path(self, id):
        if id not in self.table:
            self.table[id] = Scanner._scan([self.root], id)
        return self.table[id]


if __name__ == '__main__':
    SCANNER = Scanner("D:\\SP1DZMAIN")
    path = SCANNER.id_to_path('task1')
    print(path)