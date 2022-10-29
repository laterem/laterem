from django import template
from django.utils.safestring import SafeString
from os.path import join as pathjoin

register = template.Library()

@register.simple_tag(takes_context=True)
def asset(context, format_string):
    taskname = context['meta_taskname']
    path = '/taskasset' + '/' + taskname + '/' + format_string
    return path

def _submenu(inp):
    output = ['<ul>', '</ul>']
    pointer = 1
    separator = '\\'
    for el in inp.keys():
        if type(inp[el]) == type(dict()):
            output.insert(pointer, '<li>' + el + _submenu(inp[el]) + '</li>')
            pointer += 1
        else:
            output.insert(pointer, '<li>' + el + '<ul>')
            pointer += 1
            output.insert(pointer, '</ul></li>')
            for elel in inp[el]:
                element = elel[elel.find(separator, elel.find(separator) + 1) + 1:elel.rfind('.')]
                output.insert(pointer, '<li><a href="' + 'http://localhost:8000/works/' + element.replace(separator, '.') + '">' + element[element.rfind(separator) + 1:] + '</a></li>')
                pointer += 1
            pointer += 1
    return ''.join(output)

@register.simple_tag(takes_context=True)
def tree(context, treename):
    rtree = context[treename]
    return SafeString(_submenu(rtree))