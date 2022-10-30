from django import template
from django.utils.safestring import SafeString
from os.path import join as pathjoin

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
        if type(inp[el]) == type(dict()):
            output.insert(pointer, '<li><span class="caret">' + el + '</span>' + _submenu(inp[el], deep=deep + 1) + '</li>')
            pointer += 1
        else:
            output.insert(pointer, '<li><span class="caret">' + el + '</span><ul class="nested">')
            pointer += 1
            output.insert(pointer, '</ul></li>')
            for elel in inp[el]:
                element = elel[elel.find(SEPARATOR, elel.find(SEPARATOR) + 1) + 1:elel.rfind('.')]
                output.insert(pointer, '<li><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                pointer += 1
            pointer += 1
    return ''.join(output)

@register.simple_tag(takes_context=True)
def tree(context, treename):
    rtree = context[treename]
    return SafeString(_submenu(rtree))