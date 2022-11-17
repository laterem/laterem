from ltm.fileutils import Scanner
from ltm.fileutils import rdir_to_tree
from extratypes import Literal, Flag

# Модуль инициализации и расположения объектов, общих для всех модулей системы

LTC_SingleStorage = Flag.new()
LTC_CheckerShortcuts = Flag.new()


from sys import platform
if platform == 'darwin':
    SEPARATOR = '/'
else:
    SEPARATOR = '\\'

LTM_SCANNER = Scanner('data' + SEPARATOR + 'tasks' + SEPARATOR)
WORK_DIR = rdir_to_tree('data' + SEPARATOR + 'works' + SEPARATOR)
SPACE_REPLACER = '§'

LATEREM_FLAGS = LTC_CheckerShortcuts | LTC_SingleStorage

def update_global_dict(container: dict, value):
    container.clear()
    for k, v in value.items():
        container[k] = v