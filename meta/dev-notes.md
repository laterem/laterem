# Перечень возможных уязвимостей и багов проекта, необходимых к проверке и исправлению

***

- SolutionView было бы здорово переписать под запросы БД

- Нужно добавить проверку файлов в багрепортах

- Когда на сайт добавится разграничение прав на конкретных сущностей, в обработке сигналов на CRUD стоит добавить проверку доступа пользователя к данной сущности.

- Возвращаемые значения DTC и мета-аргументы контекста рендера html-разметки хранятся в одном словаре. Сайт может работать непредсказуемо в случае, если поле DTC будет иметь имя, используемое как мета-аргумент

- Запрос `http://localhost:8000/taskasset/<taskname>/<filename>` даёт доступ ко __всем__ файлам из директории задачи. Сейчас попытка клиента получить config.dtc или view.html вызывает ошибку 403, но мало ли.

- Скорее всего, добавлять новые вердикты будет очень больно. В users.py это всё захардкодено.

- У LTC есть доступ ко всему POST запросу. Включая токены безопасности и системные сигналы.

- В архитектуре API для работы с задачами слово "template" употребляется в двух разных значениях: шаблон Django Jinja (html файл задачи) и тип задачи. Предлагается заменить все использования слова в значении файла html на "view".