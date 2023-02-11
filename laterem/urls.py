"""laterem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import re
from django.urls import re_path
from django.views.static import serve
from core_app.views import main_page_render, student_page_render, login_view, profile_view, manage_group
from core_app.views import task_view, render_work, getasset, logout_view
from core_app.views import users_panel, teacher_hub, group_panel, work_panel, manage_work, show_work_stats, task_panel


urlpatterns = [
   # path('admin/', admin.site.urls),
    path('task/<str:stask_id>', task_view),
    path('taskasset/<str:taskname>/<str:filename>', getasset),
    path('works/<str:work_id>', render_work),
    path('login/', login_view),
    path('logout/', logout_view),
    path('profile/', profile_view),
    path('', main_page_render),
    path('student/', student_page_render),
    path('teacher/', teacher_hub),
    path('teacher/users/', users_panel),
    path('teacher/works/', work_panel),
    path('teacher/works/<str:work_id>', manage_work),
    path('teacher/works/<str:work_id>/answer_stats', show_work_stats),
    path('teacher/groups/', group_panel),
    path('teacher/groups/<str:group_id>', manage_group),
    path('teacher/tasks/', task_panel)
] + [re_path(
        r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")), serve, kwargs={'document_root': settings.STATIC_ROOT}
    ),]
