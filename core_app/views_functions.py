from itertools import count
import json
from context_objects import WORKS, SPACE_REPLACER, TASK_TYPES, WORK_DIR
from .forms import *

def fill_work_dicts(request, work_name):
    # Считывание состава работы из json
    with open('data/works/' + work_name.replace('.', '/') + '.json', 'r', encoding='UTF-8') as f:
        text = json.load(f)
    
    # Заполнение словарей работы, необходимо для системы навигации
    WORKS[work_name] = list()
    for el in text['tasks'].keys():
        task_key = str(work_name + '_id' + el)
        TASK_TYPES[task_key] = text['tasks'][el]
        WORKS[work_name].append([el, el.replace(' ', SPACE_REPLACER)])

    # Наспайдено
    if 'compiled_tasks' in request.session: 
        request.session.modified = True
        request.session['compiled_tasks'] = {} 
    
    return list(text['tasks'].keys())[0].replace(' ', SPACE_REPLACER)

def count_work(taskname):
    return taskname[taskname.rfind('/') + 1 : taskname[taskname.rfind('/') + 1 : ].find('_id')]

def fill_additional_args(request, taskname, theme):
    ret = {}
    work_name = count_work(taskname)
    ret['button1'] = AddAnswerForm()
    ret['workdir'] = WORK_DIR
    ret['meta_taskname'] = TASK_TYPES[taskname]
    ret['task_list'] = WORKS[work_name]
    ret['task_name'] = taskname[taskname.rfind('_id') + 3:]
    ret['work_name'] = work_name[work_name.rfind('.') + 1:]
    ret['user'] = request.user
    if not theme:
        theme = 'dark'
    ret['theme'] = theme
    return ret

def change_color_theme(request):
    if 'color-theme' not in request.session:
        request.session['color-theme'] = 'dark'
    
    if request.session['color-theme'] == 'dark':
        request.session['color-theme'] = 'light'
    elif request.session['color-theme'] == 'light':
        request.session['color-theme'] = 'dark'