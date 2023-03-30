from core_app.views.views_commons import *


@any_permission_required("can_manage_users", "can_manage_works", "can_manage_groups", "can_manage_tasks")
def teacher_hub(request):
    general_POST_handling(request)
    return render(
        request,
        "teacher_panel/teacher_panel_base.html",
        render_args(me=User(request.user),request=request, additional={"title": "Панель учителя"}),
    )
