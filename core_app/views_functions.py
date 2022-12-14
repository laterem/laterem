from .forms import *
from dbapi.solutions import Verdicts
from dbapi.tasks import Category

def taskview_rargs(user, task, compiled_task):
    _colors = {Verdicts.NO_ANSWER: 'no-answer',
                Verdicts.OK: 'correct',
                Verdicts.PARTIALLY_SOLVED: 'partial',
                Verdicts.SENT: 'partial',
                Verdicts.WRONG_ANSWER: 'wrong'}
    all_tasks_in_work = task.work.tasks()
    task_index_in_work = all_tasks_in_work.index(task)
    ret = {}
    ret['workdir'] = Category.global_tree(user)
    ret['meta_tasktype'] = task.task_type
    ret['task_list'] = [(_task.id, _colors[user.get_task_solution(_task).verdict]) 
                        for _task in all_tasks_in_work]
    ret['task_name'] = task.id
    if (task_index_in_work >= 0) and task_index_in_work + 1 < len(all_tasks_in_work):
        ret['next_task'] = all_tasks_in_work[task_index_in_work + 1].id
    else:
        ret['next_task'] = all_tasks_in_work[0].id
    ret['work_name'] = task.work.name
    ret['user'] = user
    ret['theme'] = user.get_setting('theme')
    ret['is_teacher'] = True
    ret['task_template'] = compiled_task.template
    return ret


def change_color_theme(user, request):
    usertheme = user.get_setting('theme')
    
    if usertheme == 'dark':
        usertheme = 'light'
    elif usertheme == 'light':
        usertheme = 'dark'
    
    user.set_settings(theme=usertheme)
    request.session['color-theme'] = usertheme