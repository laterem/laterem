from django import template
from django.utils.safestring import SafeString
from dtm.tasks import Verdicts

from context_objects import SEPARATOR

register = template.Library()

@register.simple_tag(takes_context=True)
def asset(context, format_string):
    taskname = context['meta_taskname']
    path = '/taskasset' + '/' + taskname + '/' + format_string
    return path

def _submenu(inp, deep=0):
    if deep == 0:
        output = ['<ul id="myUL">', '</ul>']
    else:
        output = ['<ul class="nested">', '</ul>']
    pointer = 1
    for el in inp.keys():
        # print('§§§§§§')
        # print(deep)
        # print(inp[el])
        # print(list(inp[el].items())[0])
        # print()
        if type(list(inp[el].values())[0]) == type(dict()):
            output.insert(pointer, '<li><span class="caret">' + el + '</span>' + _submenu(inp[el], deep=deep + 1) + '</li>')
            pointer += 1
        else:
            output.insert(pointer, '<li><span class="caret">' + el + '</span><ul class="nested">')
            pointer += 1
            output.insert(pointer, '</ul></li>')
            for elel in inp[el].keys():
                element = elel[elel.find(SEPARATOR, elel.find(SEPARATOR) + 1) + 1:elel.rfind('.')]
                if inp[el][elel] == Verdicts.NO_ANSWER:
                    output.insert(pointer, '<li id="no-answer_work"><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                else:
                    # Оперделение состояния задания
                    if inp[el][elel] == Verdicts.OK:
                        output.insert(pointer, '<li id="correct_work"><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                    elif inp[el][elel] == Verdicts.WRONG_ANSWER:
                        output.insert(pointer, '<li id="wrong_work"><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                    else:
                        output.insert(pointer, '<li id="unchecked_work"><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                pointer += 1
            pointer += 1
    return ''.join(output)

@register.simple_tag(takes_context=True)
def tree(context, treename):
    rtree = context[treename]
    return SafeString(_submenu(rtree))