from extratypes import Literal, Flag, Scanner

# Модуль инициализации и расположения объектов, общих для всех модулей системы

LTC_SingleStorage = Flag.new()
LTC_CheckerShortcuts = Flag.new()
DEBUG_DBSamples = Flag.new()

LATEREM_FLAGS = LTC_CheckerShortcuts | LTC_SingleStorage | DEBUG_DBSamples


from sys import platform
if platform == 'darwin':
    SEPARATOR = '/'
else:
    SEPARATOR = '\\'

LTM_SCANNER = Scanner('data' + SEPARATOR + 'tasks' + SEPARATOR)
SPACE_REPLACER = '§'

USER_DEFAULT_SETTINGS = {
    'theme': 'dark',
    }
USER_SETTINGS_FIELDS = USER_DEFAULT_SETTINGS.keys()

def update_global_dict(container: dict, value):
    container.clear()
    for k, v in value.items():
        container[k] = v