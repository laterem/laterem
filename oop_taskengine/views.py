from .forms import *
from .tasks import Task
from dtc.dtc_compiler import DTCCompiler
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import os
import shutil

def unravel_task_package(name):
    path = os.path.join( os.getcwd(), 'dtm', name)
    dtcpath = os.path.join(path, 'config.dtc')
    viewpath = os.path.join(path, 'view.html')
    
    tmpclones = 'oop_taskengine/templates/static_copies/'

    if not os.path.exists(tmpclones):
        os.makedirs(tmpclones)

    tmpviewpath = name.replace('\\', '_').replace('/', '_') + 'view' + '.html'

    shutil.copyfile(viewpath, tmpclones + tmpviewpath)

    return dtcpath, 'static_copies/' + tmpviewpath

def prepare_dtc(file):
    if not file.endswith('.dtc'):
        file += '.dtc'

    with open(file, mode='r') as f:
        txt = f.read()

    dtcc = DTCCompiler()

    dtc = dtcc.compile(txt)
    dtc.execute()
    return dtc

class DTCTask(Task):
    def configure(self, dtc, template) -> None:
        self.dtc = dtc
        self.template = template
    
    def test(self, answer: str) -> int:
        fields = {'answer': answer.strip()}
        return self.dtc.check(fields)

def task_view(request, taskname):
    dtcpath, templatepath = unravel_task_package('test_tasks\\' + taskname)

    dtc = prepare_dtc(dtcpath)
    task = DTCTask()
    task.configure(dtc=dtc, template=templatepath)
    dtc.field_table['standart_button'] = AddAnswerForm()
    return task_handle(request, task)


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


def completed(request):
    return HttpResponse("<h1>Решение Верно!</h1>")

def failed(request):
    return HttpResponse("<h1>Решение Неверно, переделывай!</h1>")