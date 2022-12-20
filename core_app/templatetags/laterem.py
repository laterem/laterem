from django import template
from django.utils.safestring import SafeString
from dbapi.solutions import Verdicts
from dbapi.users import User
from dbapi.tasks import Work
from context_objects import SEPARATOR

register = template.Library()

@register.simple_tag(takes_context=True)
def asset(context, format_string):
    taskname = context['task'].task_type
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

def draw_progress_line(args):
    ret = '<table class="progress_line" cellpadding="0px"><tr>'
    for verdict, l in args:
        if l > 0:
            ret += '<td class="' + verdict + '" height="4px" width=' + str(l * 100).replace('.', ',')  + '%></td>'
    ret += '</tr></table>'
    return ret

# Кол-во вызовов = кол-во словарей в mask_tree(WORK_DIR, user.raw_available_branches)
def _submenu(inp, user: User, path=[], outer=False):
    if outer:
        output = '<ul id="myUL">'
    else:
        output = '<ul class="nested">'
    
    for key, value in inp.items():
        if isinstance(value, dict):
            output += '<li><span class="caret">' + key + '</span>' + _submenu(value, user, path=path + [key]) + '</li>'
        else:
            output += '<li><span class="caret">' + key + '</span><ul class="nested">'
            for work in value:
                name = work.name
                addr = str(work.id)
                stats = user.get_work_stats(work, True)

                green_len = stats[Verdicts.OK]
                orange_len = stats[Verdicts.SENT] + stats[Verdicts.PARTIALLY_SOLVED]
                red_len = stats[Verdicts.WRONG_ANSWER]
                gray_len = stats[Verdicts.NO_ANSWER]

                line_args = [("correct", green_len), ("unchecked", orange_len), ("wrong", red_len), ("no-answer", gray_len)]
                output += '<li><a href="' + 'http://localhost:8000/works/' + addr + '">' + name + '</a>' + draw_progress_line(line_args) + '</li>'
            output += '</ul></li>'

    output += '</ul>'
    return output

@register.simple_tag(takes_context=True)
def tree(context, treename):
    try:
        user = context['user']
        return SafeString(_submenu(context[treename], user, outer=True))
    except KeyError:
        return ''

