from django import template
from django.utils.safestring import SafeString
from dbapi.solutions import Verdicts
from dbapi.users import User
from dbapi.tasks import Work

register = template.Library()


@register.simple_tag(takes_context=True)
def asset(context, format_string):
    taskname = str(context["task"].task_type.id)
    path = "/taskasset" + "/" + taskname + "/" + format_string
    return path


def draw_progress_line(args):
    ret = '<table class="progress_line" cellpadding="0px"><tr>'
    for verdict, l in args:
        if l > 0:
            ret += (
                '<td class="'
                + verdict
                + '" height="4px" width='
                + str(l * 100).replace(".", ",")
                + "%></td>"
            )
    ret += "</tr></table>"
    return ret


def _submenu(root, user: User, outer=False, editable=False, unravel=None, title="Доступные работы"):
    #inp = root.root

    if unravel is None:
        unravel = set()
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
        del_icon = """<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 width="1.5em" height="1.5em" viewBox="0 0 482.428 482.429" style="enable-background:new 0 0 482.428 482.429;"
	 xml:space="preserve">
<g>
	<g>
		<path d="M381.163,57.799h-75.094C302.323,25.316,274.686,0,241.214,0c-33.471,0-61.104,25.315-64.85,57.799h-75.098
			c-30.39,0-55.111,24.728-55.111,55.117v2.828c0,23.223,14.46,43.1,34.83,51.199v260.369c0,30.39,24.724,55.117,55.112,55.117
			h210.236c30.389,0,55.111-24.729,55.111-55.117V166.944c20.369-8.1,34.83-27.977,34.83-51.199v-2.828
			C436.274,82.527,411.551,57.799,381.163,57.799z M241.214,26.139c19.037,0,34.927,13.645,38.443,31.66h-76.879
			C206.293,39.783,222.184,26.139,241.214,26.139z M375.305,427.312c0,15.978-13,28.979-28.973,28.979H136.096
			c-15.973,0-28.973-13.002-28.973-28.979V170.861h268.182V427.312z M410.135,115.744c0,15.978-13,28.979-28.973,28.979H101.266
			c-15.973,0-28.973-13.001-28.973-28.979v-2.828c0-15.978,13-28.979,28.973-28.979h279.897c15.973,0,28.973,13.001,28.973,28.979
			V115.744z"/>
		<path d="M171.144,422.863c7.218,0,13.069-5.853,13.069-13.068V262.641c0-7.216-5.852-13.07-13.069-13.07
			c-7.217,0-13.069,5.854-13.069,13.07v147.154C158.074,417.012,163.926,422.863,171.144,422.863z"/>
		<path d="M241.214,422.863c7.218,0,13.07-5.853,13.07-13.068V262.641c0-7.216-5.854-13.07-13.07-13.07
			c-7.217,0-13.069,5.854-13.069,13.07v147.154C228.145,417.012,233.996,422.863,241.214,422.863z"/>
		<path d="M311.284,422.863c7.217,0,13.068-5.853,13.068-13.068V262.641c0-7.216-5.852-13.07-13.068-13.07
			c-7.219,0-13.07,5.854-13.07,13.07v147.154C298.213,417.012,304.067,422.863,311.284,422.863z"/>
	</g>
</g>
</svg>
"""
        if outer:
            output = '<h1 class="title">'
            output += title
            output += '<button type="submit" name="add-category-mother" class="button-icon" style="margin-left: 10px; height: min-content">'
            output += folder_plus
            output += "&nbsp; Добавить &nbsp;"
            output += "</button>"
            output += "</h1>"
            output += '<ul class="wtree">'
            for child in root.children():
                output += _submenu(child, user, editable=True, unravel=unravel)
            output += "</ul>"
            return output
    elif outer:
        output = '<h1 class="title">'
        output += title
        output += "</h1>"
        output += '<ul class="wtree">'
        for child in root.children():
            output += _submenu(child, user, unravel=unravel)
        output += "</ul>"
        return output

    output = ""

    if root.root.has_children:
        if f"category-id-{root.root.dbmodel.id}" in unravel:
            if editable:
                output += (
                    "<li>"
                    + '<span class="caret caret-down">'
                    + '<input value="'
                    + root.root.name
                    + '" name="input-'
                    + str(root.root.id)
                    + '" id="input-'
                    + str(root.root.id)
                    + '" disabled="true"/>'
                )
                change_name = (
                    "edit=getElementById('input-"
                    + str(root.root.id)
                    + "');"
                    + "if (tree_is_editing) {document.getElementById('edit-"
                    + str(root.root.id)
                    + "').type = 'submit';};"
                    + "tree_is_editing = !tree_is_editing;"
                    + "edit.disabled = false;"
                    + "getElementById('input-"
                    + str(root.root.id)
                    + "') = edit;"
                )
                output += (
                    '<button type="submit" name="delete-'
                    + str(root.root.id)
                    + '" class="button-icon">'
                    + del_icon
                    + "</button>"
                )
                output += (
                    '<button type="button" name="edit-'
                    + str(root.root.id)
                    + '" id="edit-'
                    + str(root.root.id)
                    + '" class="button-icon" onclick="'
                    + change_name
                    + '">'
                    + pencil_icon
                    + "</button>"
                )
                output += (
                    '<button type="submit" name="add-category-'
                    + str(root.root.id)
                    + '" class="button-icon">'
                    + folder_plus
                    + "</button>"
                )
                output += (
                    '<button type="submit" name="add-work-'
                    + str(root.root.id)
                    + '" class="button-icon">'
                    + book_plus
                    + "</button>"
                )
            else:
                output += "<li>" + '<span class="caret caret-down">' + root.root.name
            output += "</span>"
            output += (
                f'<ul id="category-id-{root.root.dbmodel.id}" class="nested active">'
            )
        else:
            if editable:
                output += (
                    "<li>"
                    + '<span class="caret">'
                    + '<input value="'
                    + root.root.name
                    + '" name="input-'
                    + str(root.root.id)
                    + '" id="input-'
                    + str(root.root.id)
                    + '" disabled="true"/>'
                )
                change_name = (
                    "edit=getElementById('input-"
                    + str(root.root.id)
                    + "');"
                    + "if (tree_is_editing) {document.getElementById('edit-"
                    + str(root.root.id)
                    + "').type = 'submit';};"
                    + "tree_is_editing = !tree_is_editing;"
                    + "edit.disabled = false;"
                    + "getElementById('input-"
                    + str(root.root.id)
                    + "') = edit;"
                )
                output += (
                    '<button type="submit" name="delete-'
                    + str(root.root.id)
                    + '" class="button-icon">'
                    + del_icon
                    + "</button>"
                )
                output += (
                    '<button type="button" name="edit-'
                    + str(root.root.id)
                    + '" id="edit-'
                    + str(root.root.id)
                    + '" class="button-icon" onclick="'
                    + change_name
                    + '">'
                    + pencil_icon
                    + "</button>"
                )
                output += (
                    '<button type="submit" name="add-category-'
                    + str(root.root.id)
                    + '" class="button-icon">'
                    + folder_plus
                    + "</button>"
                )
                output += (
                    '<button type="submit" name="add-work-'
                    + str(root.root.id)
                    + '" class="button-icon">'
                    + book_plus
                    + "</button>"
                )
            else:
                output += "<li>" + '<span class="caret">' + root.root.name
            output += "</span>"
            output += f'<ul id="category-id-{root.root.dbmodel.id}" class="nested">'
        for child in root.children():
            output += _submenu(child, user, unravel=unravel, editable=editable)
        output += "</ul>" + "</li>"
    else:
        name = root.root.name
        addr = str(root.root.id)
        if not editable:
            stats = user.get_work_stats(root.root, True)

            green_len = stats[Verdicts.OK]
            orange_len = (
                stats[Verdicts.SENT] + stats[Verdicts.PARTIALLY_SOLVED]
            )
            red_len = stats[Verdicts.WRONG_ANSWER]
            gray_len = stats[Verdicts.NO_ANSWER]

            line_args = [
                ("correct", green_len),
                ("unchecked", orange_len),
                ("wrong", red_len),
                ("no-answer", gray_len),
            ]
            output = (
                '<li><span style="border: none"><a href="'
                + "/works/"
                + addr
                + '/">'
                + name
                + "</a></span>"
                + draw_progress_line(line_args)
                + "</li>"
            )
        else:
            output = (
                '<li><span style="border: none"><a href="'
                + "/teacher/works/"
                + addr
                + '/">'
                + name
                + "</a></span>"
                + "</li>"
            )
    # print(output[:20] + " <...> " + output[-20:])
    assert output.count("<li") == output.count("</li>")
    assert output.count("<ul") == output.count("</ul>")
    return output


@register.simple_tag(takes_context=True)
def tree(context, treename):
    try:
        # print(context.get("unraveled_categories"))
        user = context["user"]
        unraveled_categories = (
            context["unraveled_categories"]
            if "unraveled_categories" in context
            else None
        )
        return SafeString(
            _submenu(
                context[treename],
                user,
                outer=True,
                unravel=unraveled_categories,
                title=context.get("tree_title", "Доступные работы"),
            )
        )
    except KeyError as e:
        return str(e)


@register.simple_tag(takes_context=True)
def fillable_tree(context, treename):
    try:
        user = context["user"]
        unraveled_categories = (
            context["unraveled_categories"]
            if "unraveled_categories" in context
            else None
        )
        return SafeString(
            _submenu(
                context[treename],
                user,
                outer=True,
                unravel=unraveled_categories,
                editable=True,
                title=context.get("tree_title", "Доступные работы"),
            )
        )
    except KeyError as e:
        return str(e)
