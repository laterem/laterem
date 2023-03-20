from core_app.views.views_commons import *


@permission_required("can_manage_tasks")
def task_panel(request):
    general_POST_handling(request)
    me = User(request.user)
    if request.method == "POST":
        if "newtask" in request.POST:
            name = request.POST.get("task_type_name")
            if name:
                config = read_text_file(request.FILES.get("config_file"))
                view = read_text_file(request.FILES.get("view_file"))
                if config and view:
                    try:
                        TaskTemplate.new(name=name,
                                        author=me,
                                        config=config,
                                        view=view)
                    except TaskTemplateValidationFailed as e:
                        return render(
                                request,
                                "teacher_panel/task_panel/task_panel.html",
                                render_args(
                                    request=request,
                                    meta_all_task_types_available=True,
                                    additional={"title": "Управдение шаблонами задач",
                                                "notification": f"Задача вызывает ошибку компиляции: {str(e)}"}
                                ),
                            )   
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

    with open(task.ltc_path, "r", encoding="utf-8") as f:
        ltc_text = f.read()

    with open(task.view_path_absolute, "r", encoding="utf-8") as f:
        html_text = f.read()


    if request.method == "POST":
        if "delete_task" in request.POST:
            TaskTemplate.delete(task_id)
            return redirect("/teacher/tasks/")

        if "edit_data" in request.POST:
            name = request.POST["task_name"]
            task.dbmodel.name = name
            task.dbmodel.save()
            return redirect(request.path)
        
        if "download_ltc" in request.POST:
            resp = FileResponse(open(task.ltc_path, "rb"))
            resp['Content-Disposition'] = f'attachment; filename="{asciify(task.name.strip())}-config.ltc"'
            return resp
        
        if "download_html" in request.POST:
            resp = FileResponse(open(task.view_path_absolute, "rb"))
            resp['Content-Disposition'] = f'attachment; filename="{asciify(task.name.strip())}-view.html"'
            return resp

        if "edit_ltc" in request.POST:
            try:
                task.write_ltc(request.POST.get("ltc_text"))
            except TaskTemplateValidationFailed as e:
                return render(
                        request,
                        "teacher_panel/task_panel/manage_task.html",
                        render_args(
                            request=request,
                            additional={
                                "title": "Шаблон " + task.name,
                                "task": task,
                                "notification": f"Задача вызывает ошибку компиляции: {str(e)}",
                                "ltc_text": ltc_text,
                                "html_text": html_text
                            },
                        ),
                    )
            return redirect(request.path)

        if "edit_html" in request.POST:
            task.write_html(request.POST.get("html_text"))
            return redirect(request.path)

        if "add_asset" in request.POST:
            asset = request.FILES.get("asset_file")
            if asset is not None:
                task.add_asset(asset.name, asset)
                return redirect(request.path)
        
        for signal in request.POST:
            if signal.startswith('delete_asset:'):
                asset = signal[len("delete_asset:"):]
                task.remove_asset(asset)
                return redirect(request.path)
    
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
