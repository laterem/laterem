from core_app.views.views_commons import *

from ltc.ltc import LTCExecutionError

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

    try:
        if stask_id not in request.session["compiled_tasks"]:
            compiled_task = task.compile(User(request.user))
            request.session["compiled_tasks"][stask_id] = compiled_task.as_JSON()
            request.session.modified = True
        else:
            compiled_task = CompiledTask.from_JSON(
                request.session["compiled_tasks"][stask_id]
            )
    except LTCExecutionError:
        return render(
            request,
            "student.html",
            render_args(
                me=User(request.user),
                request=request,
                additional={
                    "text": "Ой!",
                    "text2": f"Что-то пошло не так при попытке открыть задание {task.name} ({task.id}) " 
                             f"типа {task.template.name} ({task.template.id}) из работы {task.work.name} ({task.work.id}). " 
                             f"Если эта ошибка повторяется, сообщите об этом вашему учителю или "
                             f"заполните форму сообщениия об ошибке администрации сайта, "
                             f"нажав на большую красную кнопку выше, прикрепив к сообщению содержание этого текста."
                             ,
                    "unraveled_categories": request.session.get("active_ids")
                },
            ),
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
            meta_need_task_list=True,
            request=request,
            current_task=task,
            additional=additional_render_args,
        ),
    )