from .forms import *
from dtstructure.tasks import TaskData
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect
import json
from django.core.exceptions import PermissionDenied
from context_objects import TASKS, DTM_SCANNER, WORK_DIR
from os.path import join as pathjoin

# Рендер страницы работы
def render_work(request, work_name):
    with open('dtm/works/' + work_name.replace('.', '/') + '.json', 'r', encoding='UTF-8') as f:
        text = json.load(f)
    
    #global tasks
    for el in text['tasks'].keys():
        task_key = str(work_name + '_id' + el)
        TASKS[task_key] = text['tasks'][el]

        if task_key in request.session: del request.session[task_key] # Наспайдено
    
    return work_handle(request, text, work_name)

def work_handle(request, text, work_name):
    if request.method == 'POST':
        return redirect('/task/' + work_name + '_id' + request.POST['combobox_choosed'])
    return render(request, 'work_base.html', {"title": text["title"], 'work_title': 'Тестовая Работа №1', 'additional_text': 'Выберите номер задания:', "task_names": text['tasks'].keys(), 'workdir': WORK_DIR})


def getasset(request, taskname, filename):
    if filename == 'view.html' or filename == 'config.dtc':
        raise PermissionDenied()
    path = DTM_SCANNER.id_to_path(taskname)
    path = pathjoin(path, filename)
    return FileResponse(open(path, 'rb'))

# Функция рендера (обработки и конечного представления на сайте) задачи по имени (имя берётся из адресной строки)
# ОЧЕНЬ КРИВО
def task_view(request, taskname):
    additional_render_args = {}
    additional_render_args['button1'] = AddAnswerForm()
    additional_render_args['workdir'] = WORK_DIR
    additional_render_args['meta_taskname'] = TASKS[taskname]
    if request.session.get(taskname) == None:
        taskname1 = TASKS[taskname]
        task = TaskData.open(taskname1)

        request.session[taskname] = task.as_JSON() # !! Изменить ключ с таскнейма на таскнейм+соль
        return task_handle(request, task, additional_render_args)
    else:
        task = TaskData.from_JSON(request.session[taskname])
        return task_handle(request, task, additional_render_args)

# Переадресация на страницу отображения результата
def task_handle(request, task, additional_render_args):
    if request.method == 'POST':  # Расхардкодить!!!
        answer = None
        if request.POST.getlist('checks'):
            answer = request.POST.getlist('checks')
        else:
            form = AddAnswerForm(request.POST) 
            if form.is_valid():
                answer = form.cleaned_data['answer'].strip()
        if task.test(answer):
            return HttpResponseRedirect('/completed/')
        return HttpResponseRedirect('/failed/')
    else:
        form = AddAnswerForm()
    rargs = additional_render_args
    for k, v in task.dtc.field_table.items():
        rargs[k] = v
    return render(request, task.template, rargs)

# отображение результата решения (страницы, на которые мы переадресовываем после проверки)
def completed(request):
    return HttpResponse("<h1>Решение Верно!</h1>")

def failed(request):
    return HttpResponse("<h1>Решение Неверно, переделывай!</h1>")

def index_page_render(request):
    return render(request, 'task_base.html', {'title': 'Сайт по ЦЭ', 'text': 'Это базовая страница', 'text2': 'Перейдите на нужную работу по ссылке слева', 'workdir': WORK_DIR})
