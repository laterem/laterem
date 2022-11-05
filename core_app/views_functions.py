from context_objects import SPACE_REPLACER, WORK_DIR, SEPARATOR
from .forms import *
from ltm.users import User as LateremUser
from ltm.tasks import Verdicts
from ltm.works import Work
from django.http import HttpResponseRedirect

def fill_additional_args(request, taskname):
    work_name, taskid = taskname.split('_id')
    taskid = taskid.replace(SPACE_REPLACER, ' ')
    work_path = Work.split_full_name(work_name, separator='.', space_replacement=SPACE_REPLACER)
    workobject = Work(work_path)
    userobject = LateremUser(request.user.email).open()

    ret = {}
    ret['button1'] = AddAnswerForm()
    ret['workdir'] = WORK_DIR
    ret['meta_tasktype'] = workobject.tasks[taskid]
    ret['task_list'] = workobject.tasks.keys()
    ret['task_name'] = taskid
    ret['work_name'] = work_path[-1]
    ret['user'] = userobject
    ret['theme'] = userobject.get_setting('theme')
    return ret

def change_color_theme(user, request):
    usertheme = user.get_setting('theme')
    
    if usertheme == 'dark':
        usertheme = 'light'
    elif usertheme == 'light':
        usertheme = 'dark'
    
    user.set_setting('theme', usertheme)
    request.session['color-theme'] = usertheme