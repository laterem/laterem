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
def _submenu(inp, user: User, path=[], outer=False, fillable=False, first_active=False):
    if fillable:
        book_plus = '<svg class="svg-icon" style="width: 1.5em; height: 1.5em; vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M768 938.666667H256a85.333333 85.333333 0 0 1-85.333333-85.333334V170.666667a85.333333 85.333333 0 0 1 85.333333-85.333334h42.666667v298.666667l106.666666-64L512 384V85.333333h256a85.333333 85.333333 0 0 1 85.333333 85.333334v682.666666a85.333333 85.333333 0 0 1-85.333333 85.333334m-170.666667-85.333334h85.333334v-85.333333h85.333333v-85.333333h-85.333333v-85.333334h-85.333334v85.333334h-85.333333v85.333333h85.333333v85.333333z" fill="" /></svg>'
        folder_plus = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width: 1.5em; height: 1.5em; vertical-align: middle;fill: currentColor;overflow: hidden;"><path d="M512 416c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V96C0 60.7 28.7 32 64 32H181.5c17 0 33.3 6.7 45.3 18.7l26.5 26.5c12 12 28.3 18.7 45.3 18.7H448c35.3 0 64 28.7 64 64V416zM232 376c0 13.3 10.7 24 24 24s24-10.7 24-24V312h64c13.3 0 24-10.7 24-24s-10.7-24-24-24H280V200c0-13.3-10.7-24-24-24s-24 10.7-24 24v64H168c-13.3 0-24 10.7-24 24s10.7 24 24 24h64v64z"/></svg>'
        if outer:
            return '<ul id="myUL"><li><span class="caret caret-down" style="font-size: larger;">' + "Работы" + "</span>" + '<button type="submit" name="new-folder_' + "Работы" + '" class="button-icon" style="margin-left: 10px; height: min-content">' + folder_plus + '&nbsp; Добавить &nbsp;</button>' + _submenu(inp, user, path=path, fillable=fillable, first_active=True) + '</li></ul>'
    if outer:
        output = '<ul id="myUL">'
    else:
        output = '<ul class="nested">'
        if first_active:
            output = '<ul class="nested active">'

    for key, value in inp.items():
        if isinstance(value, dict):
            output += '<li><span class="caret">' + key + '</span>'
            if fillable:
                output += '<button type="submit" name="new-folder_' + key + '" class="button-icon" style="margin-left: 10px; height: min-content">' + folder_plus + '&nbsp; Добавить &nbsp;</button>'
            output += '</span>' + _submenu(value, user, path=path + [key], fillable=fillable) + '</li>'
        else:
            output += '<li><span class="caret">' + key + '</span>'
            if fillable:
                output += '<button type="submit" name="new-work_' + key + '" class="button-icon" style="margin-left: 10px;">' + book_plus + '&nbsp; Добавить &nbsp;</button>'
            output += '<ul class="nested">'
            for work in value:
                name = work.name
                addr = str(work.id)
                if not fillable:
                    stats = user.get_work_stats(work, True)

                    green_len = stats[Verdicts.OK]
                    orange_len = stats[Verdicts.SENT] + stats[Verdicts.PARTIALLY_SOLVED]
                    red_len = stats[Verdicts.WRONG_ANSWER]
                    gray_len = stats[Verdicts.NO_ANSWER]

                    line_args = [("correct", green_len), ("unchecked", orange_len), ("wrong", red_len), ("no-answer", gray_len)]
                    output += '<li><a href="' + '/works/' + addr + '">' + name + '</a>' + draw_progress_line(line_args) + '</li>'
                else:
                    output += '<li><a href="' + '/teacher/works/' + addr + '">' + name + '</a>' + '</li>'
            output += '</ul></li>'

    output += '</ul>'
    return output

@register.simple_tag(takes_context=True)
def tree(context, treename):
    return 'I AM A TREE'
    try:
        user = context['user']
        return SafeString(_submenu(context[treename], user, outer=True))
    except KeyError:
        return ''

@register.simple_tag(takes_context=True)
def fillable_tree(context, treename):
    try:
        user = context['user']
        return SafeString(_submenu(context[treename], user, outer=True, fillable=True))
    except KeyError:
        return ''
