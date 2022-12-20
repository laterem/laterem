from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from context_objects import SEPARATOR, LTM_SCANNER
from os.path import join as pathjoin
from .views_functions import render_args, change_color_theme
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, NewUser, EditUser, AddMember, AddTask

from dbapi.users import User
from dbapi.tasks import Task, CompiledTask, Work, Category
from dbapi.solutions import Verdicts
from dbapi.groups import Group

#import db_test_create

def permission_required(permission):
    def wrapper(function):
        def wrap(request, *args, **kwargs):
            if not User(request.user).has_global_permission(permission):
                raise PermissionDenied()
            return function(request, *args, **kwargs)
        return login_required(wrap)
    return wrapper


def logout_view(request):
    logout(request)
    return redirect('/')

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

                        user = LateremUser.objects.create_user(email=email, password=rpassword, username=email, settings='{}')
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
        return render(request, 'login.html', render_args(additional={'form': form}))

@login_required
def profile_view(request):
    if request.method == 'POST':  
        # Обработка кнопки смены темы
        if 'change-color-theme' in request.POST:
            with User(request.user) as user:
                change_color_theme(user, request)
                return redirect(request.path)
    with User(request.user) as user:
        return render(request, 'profile_page.html', render_args(me=user, 
                                                                 additional={'title': 'Laterem Настройки', 'workdir': dict()}))

@login_required
def teacher_hub(request):
    return render(request, "teacher_panel/teacher_panel_base.html", render_args())

@permission_required("can_manage_users")
def users_panel(request):
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
                                                    settings="{}")

        else:
    # <Плохо! Переписать>
            flag = False
            for signal in request.POST:
                if signal.startswith('delete:'):
                    email = signal.lstrip('delete:')
                    user = LateremUser.objects.get(email=email)
                    user.delete()
                    flag = True
                    break
            form = NewUser()
        # <Не тестилось, технически должно работать>
            if not flag:
                editform = EditUser(request.POST)
                if editform.is_valid():
                    for signal in request.POST:
                        if signal.startswith('edit:'):
                            email = signal.lstrip('edit:')
                            user = LateremUser.objects.get(email=email)
                            user.email = editform.email
                            user.password = editform.password
                            user.first_name = editform.first_name
                            user.last_name = editform.last_name
                            user.save()
        # </Не тестилось, технически должно работать>
    # </Плохо! Переписать>

    else:
        form = NewUser()
    return render(request, "teacher_panel/user_panel.html", render_args(meta_all_users_available=True,
                                                                        additional={'newuserform': form}))

@permission_required("can_manage_works")
def work_panel(request):
    if request.method == 'POST':
        if 'new-work' in request.POST:
            with Work(LateremWork.objects.create(name="Новая работа",
                                                 author=request.user)) as new:
                return redirect('/teacher/works/' + str(new.id))
    return render(request, "teacher_panel/work_panel.html", render_args(meta_all_works_available=True,
                                                                        ))

@permission_required("can_manage_works")
def manage_work(request, work_id):
    work = Work.by_id(work_id)

    if request.method == 'POST':
        for signal in request.POST:
            if signal.startswith('delete:'):
                id = int(signal.lstrip('delete:'))
                task = Task.by_id(id)
                work.remove_task(task)
                return redirect(request.path)
        add_task_form = AddTask(request.POST)
        if add_task_form.is_valid():
            task = work.add_task(name=add_task_form.cleaned_data['name'], 
                                 task_type=add_task_form.cleaned_data['task_type'])
            return redirect(request.path)
    else:
        add_task_form = AddTask()

    return render(request, 'teacher_panel/work_manage.html', render_args(current_work=work,
                                                                         additional={"add_task_form":add_task_form}))



@permission_required("can_manage_groups")
def group_panel(request):
    if request.method == 'POST':
        if 'new-group' in request.POST:
            with Group(LateremGroup.objects.create(name="Новая группа")) as new:
                new.add_member(User(request.user), is_group_admin=True)
                return redirect('/teacher/groups/' + str(new.id))
    return render(request, "teacher_panel/group_panel.html", render_args(meta_all_groups_available=True,
                                                                          ))

@permission_required("can_manage_groups")
def manage_group(request, group_id):
    group = Group.by_id(group_id)

    if request.method == 'POST':
        for signal in request.POST:
            if signal.startswith('delete:'):
                email = signal.lstrip('delete:')
                user = User.get(email=email)
                group.remove_member(user)
                return redirect(request.path)
        add_member_form = AddMember(request.POST)
        if add_member_form.is_valid():
            user = User.get(email=add_member_form.cleaned_data['email'])
            group.add_member(user)
            return redirect(request.path)
    else:
        add_member_form=AddMember()

    return render(request, 'teacher_panel/group_manage.html', render_args(current_group=group,
                                                                          additional={"add_member_form":add_member_form}))

# Рендер страницы работы
@login_required
def render_work(request, work_id):
    work_id = int(work_id)

    work = Work.by_id(work_id)
    #if 'compiled_tasks' in request.session: 
     #   request.session.modified = True
      #  request.session['compiled_tasks'] = {}
    return redirect('/task/' + str(work.tasks()[0].id))


def getasset(request, taskname, filename):
    if filename == 'view.html' or filename == 'config.ltc':
        raise PermissionDenied()
    path = LTM_SCANNER.id_to_path(taskname)
    path = pathjoin(path, filename)
    return FileResponse(open(path, 'rb'))

# Функция рендера (обработки и конечного представления на сайте) задачи по имени (имя берётся из адресной строки)
@login_required
def task_view(request, stask_id):
    if 'compiled_tasks' not in request.session: 
        request.session['compiled_tasks'] = {}

    task_id = int(stask_id)
    task = Task.by_id(task_id)
    if stask_id not in request.session['compiled_tasks']:
        compiled_task = task.compile()
        request.session['compiled_tasks'][stask_id] = compiled_task.as_JSON()
        request.session.modified = True
    else:
        compiled_task = CompiledTask.from_JSON(request.session['compiled_tasks'][stask_id])

    if request.method == 'POST':
        # Проверка - есть ли нажатая нами кнопка в списке задач (нужно для переадрессации на другие задачи)
        for el in request.POST:
            if el.startswith('redirect:task'):
                # Переадрессация на задачу
                l_task_id = el.lstrip('redirect:task')
                return redirect('/task/' + l_task_id)

        # Анализ ответа
        if compiled_task.test(dict(request.POST)):
            with User(request.user) as user:
                user.solve(task, compiled_task.ltc.mask_answer_dict(dict(request.POST)), Verdicts.OK)
            return redirect(request.path)
        with User(request.user) as user:
            user.solve(task, dict(request.POST), Verdicts.WRONG_ANSWER)
        return redirect(request.path)
    return render(request, "work_base.html", render_args(me=User(request.user),
                                                         current_task=task,
                                                         additional=compiled_task.ltc.field_table))

# Базовая страница сайта
@login_required
def student_page_render(request):
    with User(request.user) as user:
        if not request.session.get('color-theme'):
            request.session['color-theme'] = user.get_setting('theme')
        return render(request, 'student.html', render_args(me=User(request.user),
                                                         additional={'title': 'Laterem',
                                                                     'text': 'Это базовая страница',
                                                                     'text2': 'Перейдите на нужную работу по ссылке слева'}))

def main_page_render(request):
    with User(request.user) as user:
        return render(request,
                    'main.html',
                    {
                        'title': 'Laterem'
                    }
                    )
