from core_app.views.views_commons import *


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
