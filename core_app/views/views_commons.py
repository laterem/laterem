from ..forms import *
from dbapi.solutions import *
from dbapi.tasks import *
from dbapi.groups import *
from dbapi.users import *
from dbapi.bug_reports import *
from ..models import LateremUser
from commons import NotSpecified, asciify, LateremNotFound, read_text_file
from context_objects import LATEREM_FLAGS, DEBUG_DBSamples, TASK_SCANNER

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, Http404
from django.core.exceptions import PermissionDenied

from os.path import join as pathjoin

if DEBUG_DBSamples in LATEREM_FLAGS:
    from secret_data import ADMIN_PASSWORD

    def DEBUG_assure_admin(email="admin@admin.admin", password=ADMIN_PASSWORD):
        admin = LateremUser.objects.filter(email=email)
        if not admin:
            admin = LateremUser.objects.create_user(
                email=email, password=password, username=email, settings="{}"
            )
            admin.save()
            testcat = LateremCategory.objects.create(name="Misc.")
            admins = LateremGroup.objects.create(
                name="ADMINS",
                can_solve_tasks=True,
                can_manage_groups=True,
                can_manage_users=True,
                can_manage_works=True,
                can_manage_tasks=True,
            )

            with Group(admins) as gr:
                gr.add_member(User(admin), is_group_admin=True)
            admins.save()
            testcat.save()
            print("\n")
            print(
                "|\t В базе данных не было обнаружено пользователя-админа, поэтому"
            )
            print("|\t были созданы следующие тестовые сущности:")
            print(
                "|\t - Пользователь-админ "
                + f'(Почта: "{email}"; Пароль: "{password}")'
            )
            print('|\t - Группа админов ("ADMINS")')
            print('|\t - Категория для работ ("Misc.")')
            print("\n")

else:

    def DEBUG_assure_admin(*args, **kwargs):
        pass


def render_args(
    *,
    me=NotSpecified,
    current_task=NotSpecified,
    current_work=NotSpecified,
    current_group=NotSpecified,
    request=NotSpecified,
    meta_all_users_available=False,
    meta_all_groups_available=False,
    meta_all_works_available=False,
    meta_all_task_types_available=False,
    meta_need_task_list=False,
    additional={},
):
    ret = {}
    # print(additional)

    if me is not NotSpecified:
        if meta_all_works_available:
            ret["workdir"] = WorkTreeView(RootsMimic())
        else:
            ret["workdir"] = WorkTreeView(
                RootsMimic(), filter=WorkTreeView.user_access_filter(me, True)
            )
        ret["user"] = me
        ret["theme"] = me.get_setting("theme")
        ret["is_teacher"] = me.is_teacher()

    if current_task is not NotSpecified:
        task_work = current_task.work
        if current_work is NotSpecified:
            current_work = task_work
        all_tasks_in_task_work = task_work.tasks()
        task_index = all_tasks_in_task_work.index(current_task)
        ret["task"] = current_task
        if (task_index >= 0) and task_index + 1 < len(all_tasks_in_task_work):
            ret["next_task"] = all_tasks_in_task_work[task_index + 1].id
        else:
            ret["next_task"] = all_tasks_in_task_work[0].id
        if task_index >= 1:
            ret["previous_task"] = all_tasks_in_task_work[task_index - 1].id
        else:
            ret["previous_task"] = all_tasks_in_task_work[-1].id

    if current_work is not NotSpecified:
        all_tasks_in_work = current_work.tasks()
        ret["work"] = current_work
        ret["work_name"] = current_work.name
        _colors = {
            Verdicts.NO_ANSWER: "no-answer",
            Verdicts.OK: "correct",
            Verdicts.PARTIALLY_SOLVED: "partial",
            Verdicts.SENT: "partial",
            Verdicts.WRONG_ANSWER: "wrong",
        }
        if me is not NotSpecified and meta_need_task_list:
            ret["task_list"] = [
                (_task, _colors[me.get_task_solution(_task).verdict])
                for _task in all_tasks_in_work
            ]
        elif meta_need_task_list:
            ret["task_list"] = [
                (_task, _colors[Verdicts.NO_ANSWER])
                for _task in all_tasks_in_work
            ]

    if current_group is not NotSpecified:
        ret["group"] = current_group

    if request is not NotSpecified:
        if ret.get("theme") is None:
            ret["theme"] = request.session.get("color-theme")

    if meta_all_users_available:
        ret["allusers"] = map(User, LateremUser.objects.all())

    if meta_all_groups_available:
        ret["allgroup"] = map(Group, LateremGroup.objects.all())

    if meta_all_works_available:
        ret["allworks"] = map(Work, LateremWork.objects.all())

    if meta_all_task_types_available:
        ret["alltasktypes"] = map(
            TaskTemplate, LateremTaskTemplate.objects.all()
        )

    for key, value in additional.items():
        ret[key] = value

    ret["all_themes"] = ["light", "dark", "absolute-dark", "soft-dark"]

    return ret


def change_color_theme(user, request):
    new_theme = request.POST.get("color-theme")

    if new_theme:
        usertheme = new_theme
    else:
        usertheme = user.get_setting("theme")
        if usertheme == "dark":
            usertheme = "light"
        elif usertheme == "light":
            usertheme = "dark"

    user.set_settings(theme=usertheme)
    request.session["color-theme"] = usertheme


@login_required
def general_POST_handling(request):
    if request.method == "POST":
        # Обработка кнопки смены темы
        if "change-color-theme" in request.POST:
            with User(request.user) as user:
                change_color_theme(user, request)
                return redirect(request.path)


def permission_required(permission):
    def wrapper(function):
        def wrap(request, *args, **kwargs):
            if not User(request.user).has_global_permission(permission):
                raise PermissionDenied()
            return function(request, *args, **kwargs)

        return login_required(wrap)

    return wrapper


def every_permission_required(*permissions):
    def wrapper(function):
        def wrap(request, *args, **kwargs):
            for permission in permissions:
                if not User(request.user).has_global_permission(permission):
                    raise PermissionDenied()
            return function(request, *args, **kwargs)

        return login_required(wrap)

    return wrapper


def any_permission_required(*permissions):
    def wrapper(function):
        def wrap(request, *args, **kwargs):
            for permission in permissions:
                if User(request.user).has_global_permission(permission):
                    return function(request, *args, **kwargs)
            raise PermissionDenied()

        return login_required(wrap)

    return wrapper
