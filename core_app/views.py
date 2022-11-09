from ltm.tasks import TaskData, Verdicts
from ltm.works import Work as Work
from ltm.users import User as LateremUser
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from context_objects import SEPARATOR, LTM_SCANNER, WORK_DIR, SPACE_REPLACER
from os.path import join as pathjoin
from .views_functions import fill_additional_args, change_color_theme
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, AddAnswerForm

def logout_view(request):
    logout(request)
    return HttpResponse('<h1>Успешный выход из аккаунта</h1>')

# Сделано в спешке, всё очень криво
# Ничего, Жура переделает!
# Ага, знаю я как Жура переделывает
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
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
    work_path = Work.split_full_name(work_name, separator='.', space_replacement=SPACE_REPLACER)
    work = Work(work_path)
    if 'compiled_tasks' in request.session: 
        request.session.modified = True
        request.session['compiled_tasks'] = {}
    return redirect('/task/' + work_name + '_id' + work.get_tasks_ids()[0][0])


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
    additional_render_args = fill_additional_args(request, taskname)
    if 'compiled_tasks' not in request.session: request.session['compiled_tasks'] = {}

    work_name, taskid = taskname.split('_id')
    taskid = taskid.replace(SPACE_REPLACER, ' ')
    work_path = Work.split_full_name(work_name, separator='.', space_replacement=SPACE_REPLACER)
    workobject = Work(work_path)

    if taskname not in request.session['compiled_tasks']:
        taskobject = TaskData.open(workobject.tasks[taskid])
        request.session['compiled_tasks'][taskname] = taskobject.as_JSON()
        request.session.modified = True
    else:
        taskobject = TaskData.from_JSON(request.session['compiled_tasks'][taskname])
    return task_handle(request, taskobject, workobject, taskid, additional_render_args)
    
def task_handle(request, taskobject, workobject, taskid, additional_render_args):
    if request.method == 'POST':  
        # Обработка кнопки смены темы
        if 'change-color-theme' in request.POST:
            with LateremUser(request.user.email) as user:
                change_color_theme(user, request)
                return redirect(request.path)
        else:
            # Проверка - есть ли нажатая нами кнопка в списке задач (нужно для переадрессации на другие задачи)
            for el in request.POST:
                if el in workobject.tasks:
                    # Переадрессация на задачу
                    return redirect('/task/' + workobject.get_full_name(separator='.', space_replacement=SPACE_REPLACER) + '_id' + el.replace(' ', SPACE_REPLACER))

            # Анализ ответа
            print(dict(request.POST))
            if taskobject.test(dict(request.POST)):
                with LateremUser(request.user.email) as user:
                    user.set_verdict(workobject.path, taskid, Verdicts.OK)
                return redirect(request.path)
            with LateremUser(request.user.email) as user:
                user.set_verdict(workobject.path, taskid, Verdicts.WRONG_ANSWER)
            return redirect(request.path)

    rargs = additional_render_args
    # Что-то на спайдовом
    for k, v in taskobject.ltc.field_table.items():
        rargs[k] = v
    return render(request, taskobject.template, rargs)

# отображение результата решения (страницы, на которые мы переадресовываем после проверки)
def completed(request):
    return HttpResponse("<h1>Решение Верно!</h1>")

def failed(request):
    return HttpResponse("<h1>Решение Неверно, переделывай!</h1>")

# Базовая страница сайта
@login_required
def index_page_render(request):
    with LateremUser(request.user.email) as user:
        if request.method == 'POST':  # Расхардкодить!!!
            # Обработка кнопки смены темы
            change_color_theme(user, request)
        if not request.session.get('color-theme'):
            request.session['color-theme'] = user.get_setting('theme')
        return render(request,
                    'task_base.html',
                    {
                        'title': 'Сайт по ЦЭ',
                        'text': 'Это базовая страница',
                        'text2': 'Перейдите на нужную работу по ссылке слева',
                        'workdir': WORK_DIR,
                        'theme': user.get_setting('theme'),
                        'user': LateremUser(request.user.email).open()
                    }
                    )

