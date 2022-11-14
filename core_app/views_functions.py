from context_objects import SPACE_REPLACER, WORK_DIR, SEPARATOR
from .forms import *
from ltm.users import User as LateremUser
from ltm.tasks import Verdicts
from ltm.works import Work

def fill_additional_args(request, taskname, template):
    work_name, taskid = taskname.split('_id')
    taskid = taskid.replace(SPACE_REPLACER, ' ')
    work_path = Work.split_full_name(work_name, separator='.', space_replacement=SPACE_REPLACER)
    workobject = Work(work_path)
    userobject = LateremUser(request.user.email).open()

    ret = {}
    ret['workdir'] = WORK_DIR
    ret['meta_tasktype'] = workobject.tasks[taskid]
    _colors = {Verdicts.NO_ANSWER: 'no-answer',
                Verdicts.OK: 'correct',
                Verdicts.PARTIALLY_SOLVED: 'partial',
                Verdicts.SENT: 'partial',
                Verdicts.WRONG_ANSWER: 'wrong'}
    verdicts = (_colors[ver] for ver in userobject.get_task_verdicts(work_path, workobject.tasks.keys()))
    ret['task_list'] = zip(workobject.tasks.keys(), verdicts)
    ret['task_name'] = taskid
    if (list(workobject.tasks.keys()).index(taskid) >= 0) and list(workobject.tasks.keys()).index(taskid) + 1 < len(list(workobject.tasks.keys())):
        ret['next_task'] = list(workobject.tasks.keys())[list(workobject.tasks.keys()).index(taskid) + 1]
    else:
        ret['next_task'] = list(workobject.tasks.keys())[0]
    ret['work_name'] = work_path[-1]
    ret['user'] = userobject
    ret['theme'] = userobject.get_setting('theme')
    ret['task_template'] = template
    return ret

def change_color_theme(user, request):
    usertheme = user.get_setting('theme')
    
    if usertheme == 'dark':
        usertheme = 'light'
    elif usertheme == 'light':
        usertheme = 'dark'
    
    user.set_setting('theme', usertheme)
    request.session['color-theme'] = usertheme