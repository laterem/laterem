from .forms import *
from .abstracts import Task
from dtc.dtc_compiler import DTCCompiler
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import os
import shutil

# Клонирует шаблоны из dtm в папку django
def unravel_task_package(name):
    path = os.path.join( os.getcwd(), 'dtm', name)
    dtcpath = os.path.join(path, 'config.dtc')
    viewpath = os.path.join(path, 'view.html')
    
    tmpclones = 'core_app/templates/static_copies/'

    if not os.path.exists(tmpclones):
        os.makedirs(tmpclones)

    tmpviewpath = name.replace('\\', '_').replace('/', '_') + 'view' + '.html'

    shutil.copyfile(viewpath, tmpclones + tmpviewpath)

    return dtcpath, 'static_copies/' + tmpviewpath

# Вытаскивает из файла готовый dtc - объект
def prepare_dtc(path):
    if not path.endswith('.dtc'):
        path += '.dtc'

    with open(path, mode='r', encoding='UTF-8') as f:
        data = f.read()

    dtcc = DTCCompiler()

    dtc = dtcc.compile(data)
    dtc.execute()
    return dtc

# Функция по работе с задачей
class DTCTask(Task):
    def configure(self, dtc, template) -> None:
        self.dtc = dtc
        self.template = template
    
    def test(self, answer: str) -> int:
        fields = {'answer': answer.strip()}
        return self.dtc.check(fields)

# Функция рендера (обработки и конечного представления на сайте) задачи по имени (имя берётся из адресной строки)
def task_view(request, taskname):
    dtcpath, templatepath = unravel_task_package('test_tasks\\' + taskname)

    dtc = prepare_dtc(dtcpath)
    task = DTCTask()
    task.configure(dtc=dtc, template=templatepath)
    dtc.field_table['standart_button'] = AddAnswerForm()
    return task_handle(request, task)

# Переадресация на страницу отображения результата
def task_handle(request, task):
    if request.method == 'POST': 
        form = AddAnswerForm(request.POST) 
        if form.is_valid():
            if task.test(form.cleaned_data['answer']):
                return HttpResponseRedirect('/completed/')
            return HttpResponseRedirect('/failed/')
    else:
        form = AddAnswerForm()
    return render(request, task.template, task.dtc.field_table)

# отображение результата решения (страницы, на которые мы переадресовываем после проверки)
def completed(request):
    return HttpResponse("<h1>Решение Верно!</h1>")

def failed(request):
    return HttpResponse("<h1>Решение Неверно, переделывай!</h1>")

def index_page_render(request):
    if request.method == 'POST': 
        form = AddRedirectForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/task/' + form.cleaned_data['redirect'])
    else:
        form = AddRedirectForm()
    return render(request, 'task_base.html', {'title': 'Сайт по ЦЭ', 'text': 'Это базовая страница', 'text2': 'Отсюда вы можете переадресоваться на задачу', 'form': form})