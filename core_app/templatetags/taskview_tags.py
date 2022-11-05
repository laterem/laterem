from django import template
from django.utils.safestring import SafeString
from ltm.tasks import Verdicts
from ltm.users import User
from context_objects import SEPARATOR

register = template.Library()

@register.simple_tag(takes_context=True)
def asset(context, format_string):
    taskname = context['meta_tasktype']
    path = '/taskasset' + '/' + taskname + '/' + format_string
    return path


# Кол-во вызовов = кол-во ключей во всех слоях mask
def mask_tree(source, mask):
    if not mask:
        return source
    output = {}
    for key, value in source.items():
        if key in mask:
            output[key] = mask_tree(value, mask[key])
    return output


def _submenu(inp, user: User, path=[], outer=False):
    if outer:
        output = ['<ul id="myUL">']
    else:
        output = ['<ul class="nested">']
    
    for key, value in inp.items():
        if isinstance(value, dict):
            output.append('<li><span class="caret">' + key + '</span>' + _submenu(value, user, path=path + [key]) + '</li>')
        else:
            for work in value:
                element = work[work.find(SEPARATOR, work.find(SEPARATOR) + 1) + 1:work.rfind('.')]
                name = element[element.rfind(SEPARATOR) + 1:]
                addr = element.replace(SEPARATOR, '.')
                verdict = user.get_work_verdict(path + [key] + [name])
                if verdict == Verdicts.NO_ANSWER:
                    output.append('<li><a href="' + 'http://localhost:8000/works/' + addr + '" id="no-answer_work">' + name + '</a></li>')
                else:
                    # Оперделение состояния задания
                    if verdict == Verdicts.OK:
                        output.append('<li><a href="' + 'http://localhost:8000/works/' + addr + '" id="correct_work">' + name + '</a></li>')
                    elif verdict == Verdicts.WRONG_ANSWER:
                        output.append('<li><a href="' + 'http://localhost:8000/works/' + addr + '" id="wrong_work">' + name + '</a></li>')
                    else:
                        output.append('<li><a href="' + 'http://localhost:8000/works/' + addr + '" id="unchecked_work">' + name + '</a></li>')

    output.append('</ul>')
    return ''.join(output)

@register.simple_tag(takes_context=True)
def tree(context, treename):
    user = context['user']
    rtree = mask_tree(context[treename], user.raw_available_branches)
    return SafeString(_submenu(rtree, user, outer=True))