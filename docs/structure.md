# Структура проекта и прочие заметки для упрощения редактирования проекта
В этом файле рассматривается весь репозиторий (по возможности) 
# __Легенда__
папки обозначены заголовками, файлы - элементами списков; знаком _"©"_ обозначены создатели файлов/источники основных изменений/структурных особенностей
# .\
* quickrun.bash - скрипт для быстрого запуска виртуального окружения (venv) © Спайд
# docs
* dew-1-task-classification.md - результат первого спринта проекта (классификации задач); Представляет собой нашу классификацию задачек ЦЭ; Необходим для понимания списка ключевых функций, которые необходимы идеальному проекту © Спайд + Жура
# prototype
Директория для тестирования всякой всячины (для знакомства с django, работы с бд, наработке опыта коммуникации по проекту)
## venv
Место обитания виртуального окружения (на каждом компе свой, нужен для того что бы отделить Python для проекта от Python на всём компьюторе)
## de_web
Папка, в которой находится всё, связанное с кодом проекта и его реализацией
* custommath.py - файл, содержащий самописные (скопипасченные) функции для работы с математикой © Спайд
* manage.py - файл django, запускает тестовый сервер, создает новые модули и еще много чего делает © django
### de_web
Содержит базовые файлы проекта
* \_\_init__.py - файл, определяющий папку как пакет Python © Python
* asgi.py - файл настройки asgi © django
* urls.py - содержит все возможные ссылки на каталоги сайта (то, что после "/") и их соответствия с функциями обработки © django
* wsgi.py - файл настройки wsgi © django
### oop_taskengine
Содержит всё, что относится к задачам - от данныч до отображения на сайте
* \_\_init__.py - файл, определяющий папку как пакет Python © Python
* admin.py - файл, созданный django для определения моделей © django
* apps.py - нужен для указания обработки сигналов © django
* forms.py - определяет наполнение форм на странице (например, кнопки, поля ввода и т.д.) © django
* models.py - содержит описание моделей, создающих бд © django
* tasks.py - модуль, свозданный для генерации, рендера и прочей магии с данными что бы получить страницу © Спайд
* tests.py - нужен для тестирования сайта © django
* urls.py - содержит все возможные ссылки на каталоги сайта (то, что после "/"), относящиеся к решению задач, и их соответствия с функциями обработки © django
* views.py - предостовляет вид сайта (обрабатывает данные через tasks.py и направляет их через urls) © django
#### migrations
Список миграций БД (своего рода СКВ БД)
* \_\_init__.py - файл, определяющий папку как пакет Python © Python
* 0001_initial.py - Содержит операции сделанные с БД (пока тролько создание) © django
#### templates
Содержит шаблоны html для отображения сайта (преимущественно только самые основные - структуру типизированных страниц)
* task_base.html - стандартизированное отображение задачи с одним ответом © Жура