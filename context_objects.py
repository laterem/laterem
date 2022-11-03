from ltm.fileutils import Scanner
from ltm.fileutils import rdir_to_tree
from extratypes import Literal

# Модуль инициализации и расположения объектов, общих для всех модулей системы

from sys import platform
if platform == 'darwin':
    SEPARATOR = '/'
else:
    SEPARATOR = '\\'

TASK_TYPES = dict()
WORKS = dict()
LTM_SCANNER = Scanner('data' + SEPARATOR + 'tasks' + SEPARATOR)
WORK_DIR = rdir_to_tree('data' + SEPARATOR + 'works' + SEPARATOR)
SPACE_REPLACER = '§'

HASH_FUNCTION = hash # Временно!


def update_global_dict(container: dict, value):
    container.clear()
    for k, v in value.items():
        container[k] = v