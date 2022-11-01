from dtstructure.fileutils import Scanner
from dtstructure.fileutils import rdir_to_tree
from extratypes import Literal

# Модуль инициализации и расположения объектов, общих для всех модулей системы

from sys import platform
if platform == 'darwin':
    SEPARATOR = '/'
else:
    SEPARATOR = '\\'
TASK_TYPES = dict()
WORKS = dict()
TASKS_IN_WORKS = dict()
DTM_SCANNER = Scanner('dtm' + SEPARATOR + 'tasks' + SEPARATOR)
WORK_DIR = rdir_to_tree('dtm' + SEPARATOR + 'works' + SEPARATOR)
SPACE_REPLACER = '§'


def update_global_dict(container: dict, value):
    container.clear()
    for k, v in value.items():
        container[k] = v