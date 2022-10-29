from dtstructure.fileutils import Scanner
from dtstructure.fileutils import rdir_to_tree

# Модуль инициализации и расположения объектов, общих для всех модулей системы

class Literal():
    value = None

    def set(self, value):
        self.value = value
    
    def get(self):
        return self.value

    def __str__(self):
        return str(self.value)

from sys import platform
if platform == 'darwin':
    SEPARATOR = '/'
else:
    SEPARATOR = '\\'
TASKS = dict()
DTM_SCANNER = Scanner('dtm' + SEPARATOR + 'tasks' + SEPARATOR)
WORK_DIR = rdir_to_tree('dtm' + SEPARATOR + 'works' + SEPARATOR)



def update_global_dict(container: dict, value):
    container.clear()
    for k, v in value.items():
        container[k] = v