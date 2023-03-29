from .views_commons import *


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


def getasset(request, task_id, filename):
    if filename == "view.html" or filename == "config.ltc":
        raise PermissionDenied()
    taskid = int(task_id)
    task = TaskTemplate.by_id(taskid)
    path = pathjoin(task.assets_path, filename)
    try:
        return FileResponse(open(path, "rb"))
    except FileNotFoundError:
        raise Http404("Asset not found")


@login_required
def main_page_render(request):
    general_POST_handling(request)
    with User(request.user) as user:
        if not user.is_teacher():
            return redirect("/student/")
        return render(
            request,
            "main.html",
            render_args(request=request, me=user),
        )


def bug_report_render(request):
    general_POST_handling(request)
    user = User(request.user)
    if request.method == "POST":
        BugReport.new_report(
            user, request.POST.get("report_text"), request.FILES.get("files")
        )
        return redirect("/")
    return render(
        request,
        "bug_report.html",
        render_args(me=user, additional={"title": "Баг репорт"}),
    )
