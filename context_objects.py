from extratypes import Literal, Flag, Scanner
from os.path import join as pathjoin

# Модуль инициализации и расположения объектов, общих для всех модулей системы

LTC_SingleStorage = Flag.new()
LTC_CheckerShortcuts = Flag.new()
DEBUG_DBSamples = Flag.new()

LATEREM_FLAGS = LTC_CheckerShortcuts | LTC_SingleStorage | DEBUG_DBSamples

LTM_SCANNER = Scanner(pathjoin('data', 'tasks'))
SPACE_REPLACER = '§'

USER_DEFAULT_SETTINGS = {
    'theme': 'dark',
    }
USER_SETTINGS_FIELDS = USER_DEFAULT_SETTINGS.keys()

def update_global_dict(container: dict, value):
    container.clear()
    for k, v in value.items():
        container[k] = v