from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from commons import asciify, LateremNotFound
from context_objects import TASK_SCANNER

from os.path import join as pathjoin
from os import mkdir
from shutil import rmtree
import os

from .views_functions import (
    render_args,
    change_color_theme,
    DEBUG_assure_admin,
    general_POST_handling,
    any_permission_required,
    every_permission_required,
    permission_required
)
from .models import *
from .forms import LoginForm, NewUser, AddMember, AssignWork, UploadTask

from dbapi.users import User
from dbapi.tasks import Task, CompiledTask, Work, Category, TaskTemplate
from dbapi.solutions import Verdicts
from dbapi.groups import Group
from dbapi.bug_reports import BugReport



def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
    # <Костыль>
    DEBUG_assure_admin()
    # </Костыль>
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next"))
        else:
            return HttpResponse(
                "<h1>Такого аккаунта не существует! или данные некорректные</h1>"
            )
    else:
        form = LoginForm()
        return render(
            request, "login.html", render_args(additional={"title": "Вход в аккаунт", "form": form})
        )


@login_required
def profile_view(request):
    general_POST_handling(request)
    with User(request.user) as user:
        return render(
            request,
            "profile_page.html",
            render_args(
                me=user,
                request=request,
                additional={"title": "Настройки", "workdir": dict()},
            ),
        )  # <- Костыыыль! # где костыль нормально всё вроде


@any_permission_required("can_manage_users", "can_manage_works", "can_manage_groups", "can_manage_tasks")
def teacher_hub(request):
    general_POST_handling(request)
    return render(
        request,
        "teacher_panel/teacher_panel_base.html",
        render_args(request=request, additional={"title": "Панель учителя"}),
    )


@permission_required("can_manage_users")
def users_panel(request):
    general_POST_handling(request)
    if request.method == "POST":
        if "newuser" in request.POST:
            form = NewUser(request.POST)
            if form.is_valid():
                test = LateremUser.objects.filter(
                    email=form.cleaned_data["email"]
                )
                if test:
                    # Пользователь с такой почтой уже есть,
                    # надо(!!!!!!) как-то оповестить
                    pass
                else:
                    User.create(email=form.cleaned_data["email"],
                                password=form.cleaned_data["password"],
                                first_name=form.cleaned_data["first_name"],
                                last_name=form.cleaned_data["second_name"])
        elif "submit_import_users" in request.POST:
            # Импорт из файла
            import_file = request.FILES.get("import_file")
            header = True 
            for line in import_file:
                line = line.decode().strip()
                if header:
                    keys = line.split(';')
                    header = False
                    # print(keys)
                    if set(keys) != {'email', 'password', 'first_name', 'last_name'}:
                        # Таблица неполная, оповестить пользователя
                        break
                    continue
                args = line.split(';')
                if len(args) != 4:
                    # Таблица некорректная, оповестить пользователя
                    break
                # Добавить проверку корректности данных
                User.create(**dict(zip(keys, args)))
        else:
            flag = False
            for signal in request.POST:
                if signal.startswith("delete:"):
                    email = signal[len("delete:"):]
                    try:
                        user = LateremUser.objects.get(email=email)
                    except LateremUser.DoesNotExist:
                        continue
                    user.delete()
                    flag = True
                    break
                elif signal.startswith("edit:"):
                    email = signal.lstrip("edit:")
                    try:
                        user = LateremUser.objects.get(email=email)
                    except LateremUser.DoesNotExist:
                        continue
                    user.email = request.POST.get("user_email")
                    # if request.POST.get('user_password'):
                    #   user.password = request.POST.get('user_password')
                    user.first_name = request.POST.get("user_name")
                    user.last_name = request.POST.get("user_lastname")
                    user.save()
    form = NewUser()
    return render(
        request,
        "teacher_panel/user_panel.html",
        render_args(
            meta_all_users_available=True,
            request=request,
            additional={"newuserform": form,
                        "title": "Управление учениками"},
        ),
    )


@permission_required("can_manage_works")
def work_panel(request):
    general_POST_handling(request)
    if request.method == "POST":
        for signal in request.POST:
            if signal.startswith("add-work-"):
                cat_id = signal[len("add-work-"):]
                if cat_id == "mother":
                    with Work(
                        LateremWork.objects.create(
                            name="Новая работа",
                            author=request.user,
                        )
                    ) as new:
                        return redirect("/teacher/works/" + str(new.id))
                else:
                    try:
                        cat = Category.by_id(cat_id)
                    except LateremNotFound:
                        continue
                    with Work(
                        LateremWork.objects.create(
                            name="Новая работа",
                            author=request.user,
                            category=cat.dbmodel,
                        )
                    ) as new:
                        return redirect("/teacher/works/" + str(new.id))
            elif signal.startswith("add-category-"):
                cat_id = signal[len("add-category-"):]
                if cat_id == "mother":
                    with Category(
                        LateremCategory.objects.create(
                            name="Новая категория",
                        )
                    ) as new:
                        return redirect(request.path)
                else:
                    try:
                        cat = int(cat_id)
                    except ValueError:
                        continue
                    test = Category.__dbmodel__.objects.filter(id=cat)
                    if not test:
                        continue
                    with Category(
                        LateremCategory.objects.create(
                            name="Новая категория", root_category=cat
                        )
                    ) as new:
                        return redirect(request.path)
            elif signal.startswith("edit-"):
                s_cat_id = signal[len("edit-"):]
                try:
                    with Category.by_id(s_cat_id) as cat:
                        cat.dbmodel.name = request.POST.get(
                            "input-" + s_cat_id, "Empty"
                        )
                        cat.dbmodel.save()
                        return redirect(request.path)
                except LateremNotFound:
                    continue
            elif signal.startswith("delete-"):
                s_cat_id = signal[len("delete-"):]
                try:
                    with Category.by_id(s_cat_id) as cat:
                        if not cat.is_valid():
                            cat.delete()
                        else:
                            # Вызвать тост: удалять можно только пустые категории
                            pass
                        return redirect(request.path)
                except LateremNotFound:
                    continue

    return render(
        request,
        "teacher_panel/work_panel/work_panel.html",
        render_args(
            meta_all_works_available=True,
            request=request,
            me=User(request.user),
            additional={"title": "Управление работами"}
        ),
    )


@permission_required("can_manage_works")
def manage_work(request, work_id):
    general_POST_handling(request)
    try:
        work = Work.by_id(work_id)
    except LateremNotFound:
        raise Http404('Work not found')

    if request.method == "POST":
        for signal in request.POST:
            if signal.startswith("delete:"):
                id = int(signal.lstrip("delete:"))
                try:
                    task = Task.by_id(id)
                except LateremNotFound:
                    continue
                work.remove_task(task)
                return redirect(request.path)
        if "edit_data" in request.POST:
            name = request.POST.get("work_name")
            work.dbmodel.name = name
            work.dbmodel.save()
            return redirect(request.path)
        if "newtask" in request.POST:
            name = request.POST.get("task_name")
            task_type = request.POST.get("task_type")
            # /!\ Existence warning
            if name and task_type:
                task = work.add_task(
                    name=request.POST.get("task_name"),
                    task_type=request.POST.get("task_type"),
                )
            return redirect(request.path)
        if "appoint_to_group" in request.POST:
            try:
                group = Group.by_id(request.POST.get("group_name"))
            except LateremNotFound:
                return redirect(request.path)
            group.assign(work, User(request.user))
            return redirect(request.path)
        if "delete_work" in request.POST:
            work.delete()
            return redirect('/teacher/works/')

    groups_to_appoint = list()
    for group in User(request.user).groups():
        if work not in group.get_works():
            groups_to_appoint.append((group.id, group.name))
    return render(
        request,
        "teacher_panel/work_panel/work_manage.html",
        render_args(
            meta_all_task_types_available=True,
            me=User(request.user),
            request=request,
            additional={"title": "Работа " + work.name, "work": work, "groups_to_appoint": groups_to_appoint},
        ),
    )


@permission_required("can_manage_works")
def manage_task_in_work(request, work_id, task_id):
    general_POST_handling(request)
    try:
        work = Work.by_id(work_id)
    except LateremNotFound:
        raise Http404('Work not found')
    
    # Спайд: Допишу ловлю исключений когда вью будет в итоговом состоянии

    if request.method == "POST":
        for signal in request.POST:
            if signal.startswith("delete:"):
                id = int(signal.lstrip("delete:"))
                task = Task.by_id(id)
                work.remove_task(task)
                return redirect(request.path)
        if "edit_data" in request.POST:
            name = request.POST.get("work_name")
            work.dbmodel.name = name
            work.dbmodel.save()
            return redirect(request.path)
        if "newtask" in request.POST:
            task = work.add_task(
                name=request.POST.get("task_name"),
                task_type=request.POST.get("task_type"),
            )
            return redirect(request.path)
        if "appoint_to_group" in request.POST:
            group = Group.by_id(request.POST.get("group_name"))
            group.assign(work, User(request.user))
            return redirect(request.path)
    groups_to_appoint = list()
    for group in User(request.user).groups():
        if work not in group.get_works():
            groups_to_appoint.append((group.id, group.name))

    task = Task.by_id(task_id)

    return render(
        request,
        "teacher_panel/work_panel/work_task_manage.html",
        render_args(
            meta_all_task_types_available=True,
            me=User(request.user),
            request=request,
            additional={"title": "Работа " + work.name + "; задание " + task.name, "work": work, "groups_to_appoint": groups_to_appoint, "task": task},
        ),
    )


@permission_required("can_manage_works")
def show_work_stats(request, work_id):
    general_POST_handling(request)
    try:
        work = Work.by_id(work_id)
    except LateremNotFound:
        raise Http404('Work not found')

    group_answers_pair = [(group.name, work.get_answers(group=group)) for group in work.groups()]


    return render(
        request,
        "teacher_panel/work_panel/work_stats.html",
        render_args(
            current_work=work,
            meta_all_task_types_available=True,
           # meta_all_groups_available=True,
            me=User(request.user),
            request=request,
            additional={
                "title": "Статистика по работе " + work.name,
                "work": work,
                "group_answers": group_answers_pair
            },
        ),
    )


@permission_required("can_manage_groups")
def group_panel(request):
    general_POST_handling(request)
    if request.method == "POST":
        if "new-group" in request.POST:
            with Group(
                LateremGroup.objects.create(name="Новая группа")
            ) as new:
                new.add_member(User(request.user), is_group_admin=True)
                return redirect("/teacher/groups/" + str(new.id))
    return render(
        request,
        "teacher_panel/group_panel/group_panel.html",
        render_args(
            meta_all_groups_available=True,
            request=request,
            additional={"title": "Управление группами"}
        ),
    )


@permission_required("can_manage_groups")
def manage_group(request, group_id):
    general_POST_handling(request)
    try:
        group = Group.by_id(group_id)
    except LateremNotFound:
        raise Http404('Group not found')
    me = User(request.user)

    if request.method == "POST":
        if "delete_group" in request.POST:
            group.delete()
            return redirect("/teacher/groups/")

        if "edit_data" in request.POST:
            name = request.POST.get("group_name", "Empty")
            description = request.POST.get("group_description")
            group.dbmodel.name = name
            group.dbmodel.description = description
            group.dbmodel.save()
            return redirect(request.path)

        for signal in request.POST:
            if signal.startswith("delete:"):
                email = signal[len("delete:"):]
                user = User.get(email=email)
                if user is not None:
                    group.remove_member(user)
                return redirect(request.path)
        assign_work_form = AssignWork(request.POST)
        if assign_work_form.is_valid():
            try:
                work = Work.by_id(assign_work_form.cleaned_data["id"])
            except LateremNotFound:
                return redirect(request.path)
            group.assign(work, me)
            return redirect(request.path)
        if "newuser" in request.POST:
            user = User.get(email=request.POST.get("user_email"))
            if user is not None:
                group.add_member(user)
            return redirect(request.path)
    else:
        assign_work_form = AssignWork()

    users = list()

    for user in map(User, LateremUser.objects.all()):
        if user not in group.get_members():
            users.append(user)

    return render(
        request,
        "teacher_panel/group_panel/group_manage.html",
        render_args(
            current_group=group,
            request=request,
            additional={
                "title": "Группа " + group.name,
                "assign_work_form": assign_work_form,
                "users": users, # Избыточная информация. Можно получить из current_group; Переделать
            },
        ),
    )


@permission_required("can_manage_tasks")
def task_panel(request):
    general_POST_handling(request)
    me = User(request.user)
    if request.method == "POST":
        if "newtask" in request.POST:
            name = request.POST.get("task_type_name")
            if name:
                config = request.FILES.get("config_file")
                view = request.FILES.get("view_file")
                TaskTemplate.new(name=name,
                                author=me,
                                config=config,
                                view=view)
        else:
            flag = False
            for signal in request.POST:
                if signal.startswith("delete:"):
                    try:
                        ID = int(signal[len("delete:"):])
                        TaskTemplate.delete(ID)
                    except LateremNotFound:
                        pass
                    except ValueError:
                        pass
                    break
        return redirect(request.path)
    return render(
        request,
        "teacher_panel/task_panel/task_panel.html",
        render_args(
            request=request,
            meta_all_task_types_available=True,
            additional={"title": "Управдение шаблонами задач"}
        ),
    )

# Unfinished
@permission_required("can_manage_tasks")
def manage_task(request, task_id):
    general_POST_handling(request)
    try:
        task = TaskTemplate.by_id(task_id)
    except LateremNotFound:
        raise Http404('Task not found')
    me = User(request.user)

    if request.method == "POST":
        if "delete_task" in request.POST:
            TaskTemplate.delete(task_id)
            return redirect("/teacher/tasks/")

        if "edit_data" in request.POST:
            # rename task dirrectory
            return redirect(request.path)
        
        if "download_ltc" in request.POST:
            resp = FileResponse(open(task.ltc_path, "rb"))
            resp['Content-Disposition'] = f'attachment; filename="{asciify(task.name.strip())}-config.ltc"'
            return resp
        
        if "download_html" in request.POST:
            resp = FileResponse(open(task.view_path_absolute, "rb"))
            resp['Content-Disposition'] = f'attachment; filename="{asciify(task.name.strip())}-view.html"'
            return resp
    
    with open(task.ltc_path, "r", encoding="utf-8") as f:
        ltc_text = f.read()

    with open(task.view_path_absolute, "r", encoding="utf-8") as f:
        html_text = f.read()

    return render(
        request,
        "teacher_panel/task_panel/manage_task.html",
        render_args(
            request=request,
            additional={
                "title": "Шаблон " + task.name,
                "task": task,
                "ltc_text": ltc_text,
                "html_text": html_text
            },
        ),
    )


# Рендер страницы работы
@login_required
def render_work(request, work_id):
    general_POST_handling(request)
    try:
        work = Work.by_id(work_id)
    except LateremNotFound:
        raise Http404('Work not found')
    if not work.is_valid():
        raise Http404('Work not found')
    if 'compiled_tasks' in request.session:
        request.session.modified = True
        request.session['compiled_tasks'] = {}
    return redirect("/task/" + str(work.tasks()[0].id))


def getasset(request, task_id, filename):
    if filename == "view.html" or filename == "config.ltc":
        raise PermissionDenied()
    taskid = int(task_id)
    task = TaskTemplate.by_id(taskid)
    path = pathjoin(task.dir_path, filename)
    try:
        return FileResponse(open(path, "rb"))
    except FileNotFoundError:
        raise Http404('Asset not found')


# Функция рендера (обработки и конечного представления на сайте)
# задачи по имени (имя берётся из адресной строки)
@login_required
def task_view(request, stask_id):
    general_POST_handling(request)
    additional_render_args = {}

    if "compiled_tasks" not in request.session:
        request.session["compiled_tasks"] = {}
    try:
        task = Task.by_id(stask_id)
    except LateremNotFound:
        raise Http404('Task not found')
    
    if not task.work.is_visible(User(request.user)):
        raise PermissionDenied

    if stask_id not in request.session["compiled_tasks"]:
        compiled_task = task.compile(User(request.user))
        request.session["compiled_tasks"][stask_id] = compiled_task.as_JSON()
        request.session.modified = True
    else:
        compiled_task = CompiledTask.from_JSON(
            request.session["compiled_tasks"][stask_id]
        )

    if request.method == "POST":
        # print(request.POST)
        if "active_ids" in request.POST:
            request.session["active_ids"] = request.POST.get("active_ids")

        # Проверка - есть ли нажатая нами кнопка в списке задач (нужно для переадрессации на другие задачи)
        for el in request.POST:
            if el.startswith("redirect:task"):
                # Переадрессация на задачу
                l_task_id = el.lstrip("redirect:task")
                return redirect("/task/" + l_task_id)

        # Анализ ответа
        answers = dict(request.POST)
        del answers['csrfmiddlewaretoken']

        with User(request.user) as user:
            test_compiled = task.compile(user, answers)
            request.session["compiled_tasks"][stask_id] = test_compiled.as_JSON()
            request.session.modified = True

            if test_compiled.ltc.check():
                user.solve(
                    task,
                    compiled_task.ltc.mask_answer_dict(answers),
                    Verdicts.OK,
                )
                return redirect(request.path)
            user.solve(task, answers, Verdicts.WRONG_ANSWER)
        return redirect(request.path)
    
    additional_render_args["unraveled_categories"] = request.session.get("active_ids")
    additional_render_args["title"] = task.work.name + "; " + task.name
    additional_render_args.update(compiled_task.ltc.field_table)
    return render(
        request,
        "work_base.html",
        render_args(
            me=User(request.user),
            request=request,
            current_task=task,
            additional=additional_render_args,
        ),
    )


# Базовая страница сайта
@login_required
def student_page_render(request):
    general_POST_handling(request)
    if request.method == "POST":
        # print(request.POST)
        if "active_ids" in request.POST:
            request.session["active_ids"] = request.POST.get("active_ids")
    with User(request.user) as user:
        if not request.session.get("color-theme"):
            request.session["color-theme"] = user.get_setting("theme")
        return render(
            request,
            "student.html",
            render_args(
                me=User(request.user),
                request=request,
                additional={
                    "text": "Это базовая страница",
                    "text2": "Перейдите на нужную работу по ссылке слева",
                    "unraveled_categories": request.session.get("active_ids")
                },
            ),
        )


def main_page_render(request):
    general_POST_handling(request)
    with User(request.user) as user:
        return render(
            request,
            "main.html",
            render_args(
                request=request,
            ),
        )


def bug_report_render(request):
    general_POST_handling(request)
    user = User(request.user)
    if request.method == 'POST':
        BugReport.new_report(user, 
                             request.POST.get('report_text'), 
                             request.FILES.get('files'))
        return redirect('/')
    return render(
        request,
        "bug_report.html",
        render_args(
            additional={"title": "Баг репорт"}
        )
    )
