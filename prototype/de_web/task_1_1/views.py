from django.http import HttpResponse
from django.shortcuts import render

from task_1_1.forms import *


def Resp(request):
    form = AddAnswerForm()
    return render(request, "task_1_1/1_1.html", {'title': 'Задача 1', 'text': 'Текст задачи 1', 'form': form})

def completed_task_1_1_Resp(request):
    return HttpResponse("<h1>Решение Верно!</h1>")
