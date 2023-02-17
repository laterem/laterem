from commons import Literal, Flag, Scanner
from os.path import join as pathjoin

# Модуль инициализации и расположения объектов, общих для всех модулей системы

# Флаги окружения

LTC_SingleStorage = Flag.new()
LTC_CheckerShortcuts = Flag.new()
DEBUG_DBSamples = Flag.new()

LATEREM_FLAGS = LTC_CheckerShortcuts | LTC_SingleStorage | DEBUG_DBSamples

# Настройки компилятора LTC

LTC_DEFAULT_EXPORT_VALUE = '0'
LTC_DEFAULT_INPUT_VALUE = '0'

# Определение хранилища заданий

TASK_UPLOAD_PATH = pathjoin('data', 'tasks')
TASK_VIEW_UPLOAD_PATH = 'task_views'
TASK_SCANNER = Scanner(TASK_UPLOAD_PATH)
SPACE_REPLACER = '§'

# Конфигурация пользовательских настроек

USER_DEFAULT_SETTINGS = {
    'theme': 'dark',
    }
USER_SETTINGS_FIELDS = USER_DEFAULT_SETTINGS.keys()