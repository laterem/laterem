# Перечень возможных уязвимостей и багов проекта, необходимых к проверке и исправлению.

- Возвращаемые значения DTC и мета-аргументы контекста рендера html-разметки хранятся в одном словаре. Сайт может работать непредсказуемо в случае, если поле DTC будет иметь имя, используемое как мета-аргумент

- Запрос http://localhost:8000/taskasset/<taskname>/<filename> даёт доступ ко __всем__ файлам из директории задачи. Сейчас попытка клиента получить config.dtc или view.html вызывает ошибку 403, но мало ли.
