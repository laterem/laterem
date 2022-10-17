from .forms import *
from .abstracts import Task
from dtc.dtc_compiler import DTCCompiler, DTC
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import os
import shutil
import json

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
    
    def as_JSON(self):
        d = self.dtc.to_dict()
        print(d)
        d['template'] = self.template
        print(d)
        return json.dumps(d, indent=4)
    
    def from_JSON(self, data):
       # print(data)
        d = json.loads(data)
        self.dtc = DTC.from_dict(d)
        self.template = d['template']

# Функция рендера (обработки и конечного представления на сайте) задачи по имени (имя берётся из адресной строки)
def task_view(request, taskname):
    del request.session[taskname] # дебага ради
    additional_render_args = {}
    additional_render_args['button1'] = AddAnswerForm()
    if request.session.get(taskname) == None:
        dtcpath, templatepath = unravel_task_package('test_tasks\\' + taskname)

        dtc = prepare_dtc(dtcpath)
        task = DTCTask()
        task.configure(dtc=dtc, template=templatepath)

        request.session[taskname] = task.as_JSON() # !! Изменить ключ с таскнейма на таскнейм+соль
        return task_handle(request, task, additional_render_args)
    else:
        task = DTCTask()
        task.from_JSON(request.session[taskname])
        return task_handle(request, task, additional_render_args)

# Переадресация на страницу отображения результата
# (СПайд) Оповещаю о своих граблях, чтобы никто другой не наступил: request.session, каким-то 
# образом, сохраняет значение между запусками сервера, поэтому там может лежать мусор с прошлых нерабочих версий.
# его надо как-то его очищать.

def task_handle(request, task, additional_render_args):
    if request.method == 'POST': 
        if request.POST.getlist('checks'):
            ... # Проверка корректности ответа из нескольких элементов
        form = AddAnswerForm(request.POST) 
        if form.is_valid():
            if task.test(form.cleaned_data['answer']):
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
    if request.method == 'POST': 
        form = AddRedirectForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/task/' + form.cleaned_data['redirect'])
    else:
        form = AddRedirectForm()
    return render(request, 'task_base.html', {'title': 'Сайт по ЦЭ', 'text': 'Это базовая страница', 'text2': 'Отсюда вы можете переадресоваться на задачу', 'button': form, 'button_text': 'Вперёд!'})
