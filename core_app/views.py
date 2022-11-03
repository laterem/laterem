from ltm.tasks import TaskData
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from context_objects import SEPARATOR, TASK_TYPES, LTM_SCANNER, WORK_DIR, SPACE_REPLACER, HASH_FUNCTION
from os.path import join as pathjoin
from .views_functions import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return HttpResponse('<h1>Успешный выход из аккаунта</h1>')

# Сделано в спешке, всё очень криво
# Ничего, Жура переделает!
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        print('>>>', user)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next'))
        else:
            with open('data' + SEPARATOR + 'userdata' + SEPARATOR + 'auth.txt', mode='r') as file:
                for line in file:
                    remail, rpassword = line.split('\\')
                    if remail == email:
                        user = User.objects.create_user(email=email, password=rpassword, username=email)
                        if password == rpassword:
                            user = authenticate(username=email, password=password)
                            login(request, user)
                            return redirect(request.GET.get('next'))
                        else:
                            return HttpResponse('<h1>Такого аккаунта не существует! или данные некорректные</h1>')
                else:
                    # Пользователь не найден ни в файле auth.txt, ни в базе данных
                    return HttpResponse('<h1>Такого аккаунта не существует! или данные некорректные</h1>')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})



# Рендер страницы работы
@login_required
def render_work(request, work_name):
    return redirect('/task/' + work_name + '_id' + fill_work_dicts(request, work_name))


def getasset(request, taskname, filename):
    if filename == 'view.html' or filename == 'config.ltc':
        raise PermissionDenied()
    path = LTM_SCANNER.id_to_path(taskname)
    path = pathjoin(path, filename)
    return FileResponse(open(path, 'rb'))

# Функция рендера (обработки и конечного представления на сайте) задачи по имени (имя берётся из адресной строки)
# ОЧЕНЬ КРИВО
@login_required
def task_view(request, taskname):
    session = request.session
    if 'compiled_tasks' not in session: session['compiled_tasks'] = {}

    # Добавление пробелов в taskname
    taskname  = taskname.replace(SPACE_REPLACER, ' ')

    # Заполнение Дополнительных аргументов (Костыль?)
    additional_render_args = fill_additional_args(request, taskname, request.session.get('color-theme'))
    # Вызов функции рендера (Если задание хранится в сессии, то берем оттуда, иначе рендерим с 0)
    if taskname not in session['compiled_tasks']:
        task = TaskData.open(TASK_TYPES[taskname])

        session['compiled_tasks'][taskname] = task.as_JSON()
        request.session.modified = True
        return task_handle(request, task, taskname, additional_render_args)
    
    # Рендер из сессии
    return task_handle(request, TaskData.from_JSON(session['compiled_tasks'][taskname]), taskname, additional_render_args)

# Переадресация на страницу отображения результата
def task_handle(request, task, taskname, additional_render_args):
    if request.method == 'POST':  # Расхардкодить!!!
        # Обработка кнопки смены темы
        if 'change-color-theme' in request.POST:
            change_color_theme(request)
        else:
            # Заполнение списка с id задач (нужно для последующей переадрессации)
            ids = list()
            for _, i in additional_render_args['task_list']:
                ids.append(i)

            # Проверка - есть ли нажатая нами кнопка в списке задач (нужно для переадрессации на другие задачи)
            for el in request.POST:
                if el in ids:
                    # Переадрессация на задачу
                    return redirect('/task/' + count_work(taskname) + '_id' + el)

            # Анализ ответа
            return analyze_answer(request, task, taskname)

    rargs = additional_render_args
    # Что-то на спайдовом
    for k, v in task.ltc.field_table.items():
        rargs[k] = v
    return render(request, task.template, rargs)

# отображение результата решения (страницы, на которые мы переадресовываем после проверки)
def completed(request):
    return HttpResponse("<h1>Решение Верно!</h1>")

def failed(request):
    return HttpResponse("<h1>Решение Неверно, переделывай!</h1>")

# Базовая страница сайта
@login_required
def index_page_render(request):
    if request.method == 'POST':  # Расхардкодить!!!
        # Обработка кнопки смены темы
        change_color_theme(request)
    if not request.session.get('color-theme'):
        request.session['color-theme'] = 'dark'
    if not request.session.get('personal_tree'):
        request.session['personal_tree'] = init_personal_tree(WORK_DIR)
    return render(request,
                'task_base.html',
                {
                    'title': 'Сайт по ЦЭ',
                    'text': 'Это базовая страница',
                    'text2': 'Перейдите на нужную работу по ссылке слева',
                    'workdir': request.session['personal_tree'],
                    'theme': request.session['color-theme'],
                    'user': request.user
                }
                )

