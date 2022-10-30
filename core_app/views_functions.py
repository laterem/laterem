import json
from context_objects import WORKS, SPACE_REPLACER, TASKS, TASKS_IN_WORKS, WORK_DIR
from .forms import *

def fill_work_dicts(request, work_name):
    # Считывание состава работы из json
    with open('dtm/works/' + work_name.replace('.', '/') + '.json', 'r', encoding='UTF-8') as f:
        text = json.load(f)
    
    # Заполнение словарей работы, необходимо для системы навигации
    WORKS[work_name] = list()
    for el in text['tasks'].keys():
        task_key = str(work_name + '_id' + el)
        TASKS[task_key] = text['tasks'][el]
        WORKS[work_name].append([el, el.replace(' ', SPACE_REPLACER)])
        TASKS_IN_WORKS[task_key] = work_name

        if task_key in request.session: del request.session[task_key] # Наспайдено
    
    return list(text['tasks'].keys())[0].replace(' ', SPACE_REPLACER)

def fill_additional_args(taskname):
    ret = {}
    ret['button1'] = AddAnswerForm()
    ret['workdir'] = WORK_DIR
    ret['meta_taskname'] = TASKS[taskname]
    ret['task_list'] = WORKS[TASKS_IN_WORKS[taskname]]
    ret['task_name'] = taskname[taskname.rfind('_id') + 3:]
    return ret