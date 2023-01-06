from django import template
from django.utils.safestring import SafeString
from dbapi.solutions import Verdicts
from dbapi.users import User
from dbapi.tasks import Work

register = template.Library()

@register.simple_tag(takes_context=True)
def asset(context, format_string):
    taskname = context['task'].task_type
    path = '/taskasset' + '/' + taskname + '/' + format_string
    return path

def draw_progress_line(args):
    ret = '<table class="progress_line" cellpadding="0px"><tr>'
    for verdict, l in args:
        if l > 0:
            ret += '<td class="' + verdict + '" height="4px" width=' + str(l * 100).replace('.', ',')  + '%></td>'
    ret += '</tr></table>'
    return ret

def _submenu(inp, user: User, outer=False, editable=False, unravel=False):
    if editable:
        book_plus = """<svg class="svg-icon" style="width: 1.5em; height: 1.5em; vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
                       <path d="M768 938.666667H256a85.333333 85.333333 0 0 1-85.333333-85.333334V170.666667a85.333333 85.333333 0 0 1 85.333333-85.333334h42.666667v298.666667l106.666666-64L512 384V85.333333h256a85.333333 85.333333 0 0 1 85.333333 85.333334v682.666666a85.333333 85.333333 0 0 1-85.333333 85.333334m-170.666667-85.333334h85.333334v-85.333333h85.333333v-85.333333h-85.333333v-85.333334h-85.333334v85.333334h-85.333333v85.333333h85.333333v85.333333z" fill="" />
                       </svg>"""
        folder_plus = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width: 1.5em; height: 1.5em; vertical-align: middle;fill: currentColor;overflow: hidden;">
                         <path d="M512 416c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V96C0 60.7 28.7 32 64 32H181.5c17 0 33.3 6.7 45.3 18.7l26.5 26.5c12 12 28.3 18.7 45.3 18.7H448c35.3 0 64 28.7 64 64V416zM232 376c0 13.3 10.7 24 24 24s24-10.7 24-24V312h64c13.3 0 24-10.7 24-24s-10.7-24-24-24H280V200c0-13.3-10.7-24-24-24s-24 10.7-24 24v64H168c-13.3 0-24 10.7-24 24s10.7 24 24 24h64v64z"/>
                         </svg>"""
        pencil_icon = """<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                                width="1.5em" height="1.5em" viewBox="0 0 297.068 297.068" style="enable-background:new 0 0 297.068 297.068;" xml:space="preserve">
                            <g>
                                <path d="M288.758,46.999l-38.69-38.69c-5.347-5.354-12.455-8.303-20.02-8.303s-14.672,2.943-20.02,8.297L28.632,190.266L0,297.061
                                    l107.547-28.805L288.745,87.045c5.36-5.354,8.323-12.462,8.323-20.026S294.105,52.347,288.758,46.999z M43.478,193.583
                                    L180.71,55.823l60.554,60.541L103.761,253.866L43.478,193.583z M37.719,206.006l53.368,53.362l-42.404,11.35L26.35,248.384
                                    L37.719,206.006z M279.657,77.951l-19.493,19.505l-60.579-60.541l19.544-19.525c5.823-5.848,16.016-5.842,21.851,0l38.69,38.696
                                    c2.924,2.918,4.544,6.8,4.544,10.926C284.214,71.139,282.594,75.027,279.657,77.951z"/>
                            </g>
                         </svg>"""
        if outer:
            output = '<h1 class="title">'
            output += "Работы"
            # output += '<button type="submit" name="add-category-mother" class="button-icon" style="margin-left: 10px; height: min-content">'
            # output += folder_plus
            # output += '&nbsp; Добавить &nbsp;'
            # output += '</button>'
            output += '</h1>'
            output += '<ul class="wtree">'
            for child in inp.children():
                output += _submenu(child, user, editable=True)
            output += '</ul>'
            return  output
    elif outer:
        output = '<ul class="wtree">'
        for child in inp.children():
            output += _submenu(child, user)
        output += '</ul>'
        return  output
    
    output = ''

    if inp.has_children:
        output += '<li>' + '<span>' + '<input value="' + inp.name + '" name="input-' + str(inp.id) + '" id="input-' + str(inp.id) + '" disabled="true"/>'
        if editable:
            change_name = "edit=getElementById('input-" + str(inp.id) + "'); if (tree_is_editing) {document.getElementById('edit-" + str(inp.id) + "').type = 'submit';}; tree_is_editing = !tree_is_editing; edit.disabled = false; getElementById('input-" + str(inp.id) + "') = edit;"
            output += '<button type="button" name="edit-' + str(inp.id) + '" id="edit-' + str(inp.id) + '" class="button-icon" style="margin-left: 10px;" onclick="' + change_name + '">' + pencil_icon + '</button>'
            output += '<button type="submit" name="add-category-' + str(inp.id) + '" class="button-icon" style="margin-left: 10px; height: min-content">' + folder_plus + '</button>'
            output += '<button type="submit" name="add-work-' + str(inp.id) + '" class="button-icon" style="margin-left: 10px;">' + book_plus + '</button>'
        output += '</span>'
        if unravel:
            output += '<ul>'
        else:
            output += '<ul>' 
        for child in inp.children():
            output +=  _submenu(child, user, editable=editable) 
        output +=  '</ul>' + '</li>'
    else:
        name = inp.name
        addr = str(inp.id)
        if not editable:
            stats = user.get_work_stats(inp, True)

            green_len = stats[Verdicts.OK]
            orange_len = stats[Verdicts.SENT] + stats[Verdicts.PARTIALLY_SOLVED]
            red_len = stats[Verdicts.WRONG_ANSWER]
            gray_len = stats[Verdicts.NO_ANSWER]

            line_args = [("correct", green_len), ("unchecked", orange_len), ("wrong", red_len), ("no-answer", gray_len)]
            output = '<li><span><a href="' + '/works/' + addr + '">' + name + '</a></span>' + draw_progress_line(line_args) + '</li>'
        else:
            output = '<li><span style="border: none"><a href="' + '/teacher/works/' + addr + '">' + name + '</a></span>' + '</li>'
    print(output[:20] + " <...> " + output[-20:])
    assert output.count('<li') == output.count('</li>')
    assert output.count('<ul') == output.count('</ul>')
    return output

    


# Кол-во вызовов = кол-во словарей в mask_tree(WORK_DIR, user.raw_available_branches)
#def _submenu(inp, user: User, path=[], outer=False, fillable=False, first_active=False):
#    for key, value in inp.items():
#        if isinstance(value, dict):
#            output += '<li><span class="caret">' + key + '</span>'
#            if fillable:
#                output += '<button type="submit" name="new-folder_' + key + '" class="button-icon" style="margin-left: 10px; height: min-content">' + folder_plus + '&nbsp; Добавить &nbsp;</button>'
#            output += '</span>' + _submenu(value, user, path=path + [key], fillable=fillable) + '</li>'
#        else:
#            output += '<li><span class="caret">' + key + '</span>'
#            if fillable:
#                output += '<button type="submit" name="new-work_' + key + '" class="button-icon" style="margin-left: 10px;">' + book_plus + '&nbsp; Добавить &nbsp;</button>'
#            output += '<ul class="nested">'
#            for work in value:
#                name = work.name
#                addr = str(work.id)
#                if not fillable:
#                    stats = user.get_work_stats(work, True)
#
#                    green_len = stats[Verdicts.OK]
#                    orange_len = stats[Verdicts.SENT] + stats[Verdicts.PARTIALLY_SOLVED]
#                    red_len = stats[Verdicts.WRONG_ANSWER]
#                    gray_len = stats[Verdicts.NO_ANSWER]

#                    line_args = [("correct", green_len), ("unchecked", orange_len), ("wrong", red_len), ("no-answer", gray_len)]
#                    output += '<li><a href="' + '/works/' + addr + '">' + name + '</a>' + draw_progress_line(line_args) + '</li>'
#                else:
#                    output += '<li><a href="' + '/teacher/works/' + addr + '">' + name + '</a>' + '</li>'
#            output += '</ul></li>'

#    output += '</ul>'
#    return output

@register.simple_tag(takes_context=True)
def tree(context, treename):
    try:
        user = context['user']
        return SafeString(_submenu(context[treename], user, outer=True))
    except KeyError:
        return ''

@register.simple_tag(takes_context=True)
def fillable_tree(context, treename):
    try:
        user = context['user']
        return SafeString(_submenu(context[treename], user, outer=True, editable=True))
    except KeyError:
        return ''
