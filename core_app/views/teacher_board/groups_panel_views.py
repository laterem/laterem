from core_app.views.views_commons import *


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
