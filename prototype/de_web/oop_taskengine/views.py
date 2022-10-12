from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from oop_taskengine.tasks import AnswerMatching, BasicProblemSolving, NumberComparison, NumberNotationConvertation
from oop_taskengine.forms import *

def base_task_handle(request, task, template="task_base.html", render_args={'title': 'Задание по ЦЭ', 'text': None, 'form': None}):
    if request.method == 'POST': 
        form = AddAnswerForm(request.POST) 
        if form.is_valid():
            if task.test(form.cleaned_data['answer']):
                return HttpResponseRedirect('/completed/')
            return HttpResponseRedirect('/failed/')
    else:
        form = AddAnswerForm()
    if template == "task_base.html":
        return render(request, "task_base.html", {'title': 'Задание по ЦЭ', 'text': task.render(), 'form': form})
    else:
        template += '.html'
        return render(request, template, render_args)


def task_question(request):
    task = AnswerMatching()
    task.configure('42', 'Какой ответ на вопрос жизни вселенной и всего такого?')
    return base_task_handle(request, task)

def task_problem(request):
    task = BasicProblemSolving()
    task.configure(10, 5, BasicProblemSolving.Plus, 2, 16, 10)
    return base_task_handle(request, task)

def task_compare(request):
    task = NumberComparison()
    task.configure(10, 10, 16, 16)
    return base_task_handle(request, task)

def task_convert(request):
    task = NumberNotationConvertation()
    task.configure(10, 10, 16)
    return base_task_handle(request, task)

def completed(request):
    return HttpResponse("<h1>Решение Верно!</h1>")

def failed(request):
    return HttpResponse("<h1>Решение Неверно, переделывай!</h1>")
