from .forms import *
from dbapi.solutions import Verdicts
from dbapi.tasks import Category
from dbapi.groups import Group
from dbapi.users import User
from extratypes import NotSpecified

def render_args(*, 
                me=NotSpecified, 
                current_task=NotSpecified,
                current_work=NotSpecified,
                current_group=NotSpecified,
                meta_all_users_available=True,
                meta_all_groups_available=True,
                additional={}
                ):
    ret = {}

    if me is not NotSpecified:
        ret['workdir'] = Category.global_tree(me)
        ret['user'] = me
        ret['theme'] = me.get_setting('theme')
        ret['is_teacher'] = True
    
    if current_task is not NotSpecified:
        task_work = current_task.work
        if current_work is NotSpecified:
            current_work = task_work
        all_tasks_in_task_work = task_work.tasks()
        task_index = all_tasks_in_task_work.index(current_task)
        ret['meta_tasktype'] = current_task.task_type
        ret['task_name'] = current_task.id
        if (task_index >= 0) and task_index + 1 < len(all_tasks_in_task_work):
            ret['next_task'] = all_tasks_in_task_work[task_index + 1].id
        else:
            ret['next_task'] = all_tasks_in_task_work[0].id
        ret['task_template'] = current_task.template_path
    
    if current_work is not NotSpecified:
        all_tasks_in_work = current_work.tasks()
        ret['work_name'] = current_work.name
        _colors = {Verdicts.NO_ANSWER: 'no-answer',
                   Verdicts.OK: 'correct',
                   Verdicts.PARTIALLY_SOLVED: 'partial',
                   Verdicts.SENT: 'partial',
                   Verdicts.WRONG_ANSWER: 'wrong'}
        if me is not NotSpecified:
            ret['task_list'] = [(_task.id, _colors[me.get_task_solution(_task).verdict]) 
                                for _task in all_tasks_in_work]
        else:
            ret['task_list'] = [(_task.id, _colors[Verdicts.NO_ANSWER]) 
                                for _task in all_tasks_in_work]
    
    if current_group is not NotSpecified:
        ret['group'] = current_group

    if meta_all_users_available:
        ret['allusers'] = map(User, LateremUser.objects.all())
    
    if meta_all_groups_available:
        ret['allgroup'] = map(Group, LateremGroup.objects.all())

    for key, value in additional.items():
        ret[key] = value

    return ret


def change_color_theme(user, request):
    usertheme = user.get_setting('theme')
    
    if usertheme == 'dark':
        usertheme = 'light'
    elif usertheme == 'light':
        usertheme = 'dark'
    
    user.set_settings(theme=usertheme)
    request.session['color-theme'] = usertheme