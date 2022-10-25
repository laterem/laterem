from os import listdir
from os.path import isfile, join

# Построение объекта вложенного словаря по директории (рекурсия, произвольная вложенность)
def rdir_to_tree(sourcepath, layers=-1):
    dirlist = listdir(sourcepath)
    if dirlist:
        if layers == 0 or (layers < 0 and dirlist[0].endswith('.json')): # Костыль, но учителю нужно постараться чтобы его заабузить
            return [join(sourcepath, path) for path in dirlist if path.endswith('.json')]
        else:
            output = {}
            for key in dirlist:
                output[key] = rdir_to_tree(join(sourcepath, key), layers-1)
            return output
    else:
        return []

# Поиск пути к файлу по его названию
class Scanner:
    '''Class for identifying file within directories by their filenames only,
       without specifying their full paths.'''
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