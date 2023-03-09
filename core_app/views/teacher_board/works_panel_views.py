from core_app.views.views_commons import *


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
def manage_task_in_work(request, task_id):
    general_POST_handling(request)
    try:
        task = Task.by_id(task_id)
    except LateremNotFound:
        raise Http404('Task not found')

    work = task.work

    if request.method == "POST":
        if "task-name" in request.POST:
            task_name = request.POST.get("task-name")
            if task_name:
                task.dbmodel.name = task_name
                task.dbmodel.save()
                return redirect(request.path)
        elif "edit-task-fields" in request.POST:
            with task:
                task.set_field_overrides(dict(request.POST),
                                         pick_first=True)
                

    return render(
        request,
        "teacher_panel/work_panel/work_task_manage.html",
        render_args(
            me=User(request.user),
            request=request,
            current_task=task,
            current_work=work,
            additional={"title": "Работа " + work.name + ": задание " + task.name},
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

