"""de_web URL Configuration

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
from core_app.views import failed, completed, index_page_render
from core_app.views import task_view, render_work, getasset


urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/<str:taskname>', task_view),
    path('taskasset/<str:taskname>/<str:filename>', getasset),
    path('works/<str:work_name>', render_work),
    path('failed/', failed),
    path('completed/', completed),
    path('', index_page_render)
]
