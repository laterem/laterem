from ltm.tasks import TaskData, Verdicts
from ltm.works import Work as Work
from ltm.users import User as User
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from context_objects import SEPARATOR, LTM_SCANNER, WORK_DIR, SPACE_REPLACER
from os.path import join as pathjoin
from .views_functions import fill_additional_args, change_color_theme
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, NewUser, EditUser

def teacher_only(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_teacher:
            raise PermissionDenied()
        return function(request, *args, **kwargs)
    return login_required(wrap)


def logout_view(request):
    logout(request)
    return redirect('/')

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
                        if email.upper() == 'ADMIN@ADMIN.ADMIN':
                            tc = True
                        else:
                            tc = False
                        user = LateremUser.objects.create_user(email=email, password=rpassword, username=email, is_teacher=tc, settings=0)
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

def settings_view(request):
    if request.method == 'POST':  
        # Обработка кнопки смены темы
        if 'change-color-theme' in request.POST:
            with User(request.user.email) as user:
                change_color_theme(user, request)
                return redirect(request.path)
    with User(request.user.email) as user:
        return render(request, 'settings_page.html', {
                            'title': 'Laterem Настройки',
                            'theme': user.get_setting('theme'),
                            'user': User(request.user.email).open(),
                            'is_teacher': True,
                        })

@teacher_only
def users_panel(request, page_for_render='users_panel.html', rargs=dict()):
    if request.method == 'POST':
        if "newuser" in request.POST:
            form = NewUser(request.POST)
            if form.is_valid():
                test = LateremUser.objects.filter(email=form.cleaned_data['email'])
                if test:
                    # Пользователь с такой почтой уже есть, надо как-то оповестить 
                    pass
                else:
                    LateremUser.objects.create_user(email=form.cleaned_data['email'], password=form.cleaned_data['password'],
                                                    username=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'],
                                                    last_name=form.cleaned_data['second_name'],
                                                    is_teacher=False,
                                                    settings=0)
        else:
    # <Плохо! Переписать>
            flag = False
            for user in LateremUser.objects.all():
                if 'delete:' + user.email in request.POST:
                    user.delete()
                    flag = True
                    break
            form = NewUser()
        # <Не тестилось, технически должно работать>
            if not flag:
                editform = EditUser(request.POST)
                if editform.is_valid():
                    for user in LateremUser.objects.all():
                        if 'edit:' + user.email in request.POST:
                            user.email = editform.email
                            user.password = editform.password
                            user.first_name = editform.first_name
                            user.last_name = editform.last_name
                            user.save()
        # </Не тестилось, технически должно работать>
    # </Плохо! Переписать>

    else:
        form = NewUser()
    rargs['newuserform'] = form
    rargs['allusers'] = LateremUser.objects.all()
    return render(request, page_for_render, rargs)

@teacher_only
def user_managing(request):
    return users_panel(request, page_for_render='user_panel/user_managing.html')

@teacher_only
def right_managing(request):
    return users_panel(request, page_for_render='user_panel/right_managing.html')

@teacher_only
def group_managing(request):
    return users_panel(request, page_for_render='user_panel/group_managing.html', rargs={'allgroup': {'Тестовая группа 1': ['Вася', 'Петя'], 'Тестовая группа 2': ['Петя', 'Федя', 'Спайд']}})

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
    additional_render_args = fill_additional_args(request, taskname, taskobject.template)
    return task_handle(request, taskobject, workobject, taskid, additional_render_args)
    
def task_handle(request, taskobject, workobject, taskid, additional_render_args):
    if request.method == 'POST':
        # Проверка - есть ли нажатая нами кнопка в списке задач (нужно для переадрессации на другие задачи)
        for el in request.POST:
            if el in workobject.tasks:
                # Переадрессация на задачу
                return redirect('/task/' + workobject.get_full_name(separator='.', space_replacement=SPACE_REPLACER) + '_id' + el.replace(' ', SPACE_REPLACER))

        # Анализ ответа
        if taskobject.test(dict(request.POST)):
            with User(request.user.email) as user:
                user.set_verdict(workobject.path, taskid, Verdicts.OK)
            return redirect(request.path)
        with User(request.user.email) as user:
            user.set_verdict(workobject.path, taskid, Verdicts.WRONG_ANSWER)
        return redirect(request.path)

    rargs = additional_render_args
    # Что-то на спайдовом
    for k, v in taskobject.ltc.field_table.items():
        rargs[k] = v
    return render(request, "work_base.html", rargs)

# Базовая страница сайта
@login_required
def index_page_render(request):
    with User(request.user.email) as user:
        if not request.session.get('color-theme'):
            request.session['color-theme'] = user.get_setting('theme')
        return render(request,
                    'index.html',
                    {
                        'title': 'Laterem',
                        'text': 'Это базовая страница',
                        'text2': 'Перейдите на нужную работу по ссылке слева',
                        'workdir': WORK_DIR,
                        'theme': user.get_setting('theme'),
                        'user': User(request.user.email).open(),
                        'is_teacher': True,
                    }
                    )

