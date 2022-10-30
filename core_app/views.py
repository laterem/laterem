from .forms import *
from dtstructure.tasks import TaskData
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect
import json
from django.core.exceptions import PermissionDenied
from context_objects import TASKS, DTM_SCANNER, TASKS_IN_WORKS, WORK_DIR, SPACE_REPLACER, WORKS
from os.path import join as pathjoin

def fill_work_dicts(request, work_name):
    # Считывание состава работы из json
    with open('dtm/works/' + work_name.replace('.', '/') + '.json', 'r', encoding='UTF-8') as f:
        text = json.load(f)
    
    # Заполнение словарей работы, необходимо для системы навигации
    WORKS[work_name] = list()
    for el in text['tasks'].keys():
        task_key = str(work_name + '_id' + el)
        TASKS[task_key] = text['tasks'][el]
        WORKS[work_name].append([el, el.replace(' ', SPACE_REPLACER)])
        TASKS_IN_WORKS[task_key] = work_name

        if task_key in request.session: del request.session[task_key] # Наспайдено
    
    return list(text['tasks'].keys())[0].replace(' ', SPACE_REPLACER)

# Рендер страницы работы
def render_work(request, work_name):
    return redirect('/task/' + work_name + '_id' + fill_work_dicts(request, work_name))


def getasset(request, taskname, filename):
    if filename == 'view.html' or filename == 'config.dtc':
        raise PermissionDenied()
    path = DTM_SCANNER.id_to_path(taskname)
    path = pathjoin(path, filename)
    return FileResponse(open(path, 'rb'))

def fill_additional_args(taskname):
    ret = {}
    ret['button1'] = AddAnswerForm()
    ret['workdir'] = WORK_DIR
    ret['meta_taskname'] = TASKS[taskname]
    ret['task_list'] = WORKS[TASKS_IN_WORKS[taskname]]
    ret['task_name'] = taskname[taskname.rfind('_id') + 3:]
    return ret

# Функция рендера (обработки и конечного представления на сайте) задачи по имени (имя берётся из адресной строки)
# ОЧЕНЬ КРИВО
def task_view(request, taskname):
    # Добавление пробелов в taskname
    taskname  = taskname.replace(SPACE_REPLACER, ' ')

    # Заполнение Дополнительных аргументов (Костыль?)
    additional_render_args = fill_additional_args(taskname)
    # Вызов функции рендера (Если задание зранится в сессии, то берем оттуда, иначе рендерим с 0)
    if request.session.get(taskname) == None:
        task = TaskData.open(TASKS[taskname])

        request.session[taskname] = task.as_JSON()
        return task_handle(request, task, taskname, additional_render_args)
    
    # Рендер из сессии
    return task_handle(request, TaskData.from_JSON(request.session[taskname]), taskname, additional_render_args)

# Переадресация на страницу отображения результата
def task_handle(request, task, taskname, additional_render_args):
    if request.method == 'POST':  # Расхардкодить!!!
        # Заполнение списка с id задач (нужно для последующей переадрессации)
        ids = list()
        for _, i in additional_render_args['task_list']:
            ids.append(i)

        # Проверка - есть ли нажатая нами кнопка в списке задач (нужно для переадрессации на другие задачи)
        for el in request.POST:
            if el in ids:
                # Переадрессация на задачу
                return redirect('/task/' + TASKS_IN_WORKS[taskname] + '_id' + el)

        # Анализ ответа
        answer = None
        if request.POST.getlist('checks'):
            answer = request.POST.getlist('checks')
        else:
            form = AddAnswerForm(request.POST) 
            if form.is_valid():
                answer = form.cleaned_data['answer'].strip()

        # Проверка ответа -> переадрессация на нужную страницу
        if task.test(answer):
            # Тут надо записывать что ученик правильно сдал задачу 
            return HttpResponseRedirect('/completed/')
        return HttpResponseRedirect('/failed/')
    else:
        form = AddAnswerForm()
    rargs = additional_render_args
    # Что-то на спайдовом
    for k, v in task.dtc.field_table.items():
        rargs[k] = v
    return render(request, task.template, rargs)

# отображение результата решения (страницы, на которые мы переадресовываем после проверки)
def completed(request):
    return HttpResponse("<h1>Решение Верно!</h1>")

def failed(request):
    return HttpResponse("<h1>Решение Неверно, переделывай!</h1>")

# Базовая страница сайта
def index_page_render(request):
    return render(request, 'task_base.html', {'title': 'Сайт по ЦЭ', 'text': 'Это базовая страница', 'text2': 'Перейдите на нужную работу по ссылке слева', 'workdir': WORK_DIR})
