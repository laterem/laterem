from http.client import PARTIAL_CONTENT
import json
from ssl import VERIFY_DEFAULT
from termios import PARENB
from context_objects import WORKS, SPACE_REPLACER, TASK_TYPES, WORK_DIR, SEPARATOR
from .forms import *
from dtm.users import User as LateremUser
from dtm.tasks import Verdicts
from django.http import HttpResponseRedirect

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
    if not request.session.get('personal_tree'):
        request.session['personal_tree'] = init_personal_tree(WORK_DIR)
    ret['workdir'] = request.session['personal_tree']
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

def init_personal_tree(tree):
    ret = dict()
    for el in list(tree.keys()):
        if type(tree[el]) == type(dict()):
            # Ситуация на узле
            ret[el] = init_personal_tree(tree[el])
        else:
            # Ситуация последнего узла
            ret[el] = dict()
            for i in tree[el]:
                #  i - имя работы
                ret[el][i] = Verdicts.NO_ANSWER
    return ret

def set_work_verdict(answers):
    if answers[Verdicts.NO_ANSWER] == 0:
        if (answers[Verdicts.WRONG_ANSWER] == answers[Verdicts.PARTIALLY_SOLVED] == 0):
            return Verdicts.OK
    elif (answers[Verdicts.OK] > 0) or (answers[Verdicts.SENT] > 0) or (answers[Verdicts.PARTIALLY_SOLVED] > 0):
        return Verdicts.PARTIALLY_SOLVED
    else:
        return Verdicts.NO_ANSWER

def merge_tree(tree1, tree2, user):
    # tree1 - WORKDIR или его ветка; tree2 - Дерево ученика; ret - результат
    ret = dict()
    if type(tree1) != type(dict()):
        # Обработка листьев (работ)
        for k in tree1:
            # k - имя работы
            # answers - словарь. ключ - вердикт; значение - сколько задач с таким вердиктом в работе
            answers = {Verdicts.NO_ANSWER: 0,
                Verdicts.OK: 0,
                Verdicts.PARTIALLY_SOLVED: 0,
                Verdicts.SENT: 0,
                Verdicts.WRONG_ANSWER: 0
            }

            work_name_for_WORKS = k[11:k.rfind('.')].replace(SEPARATOR, '.')
            work_name_for_user = k[11:k.rfind('.')]

            for t in WORKS[work_name_for_WORKS][0]:
                if user.get_task_verdict(work_name_for_user, t):
                    answers[user.get_task_verdict(work_name_for_user, t)] += 1
                else:
                    answers[Verdicts.NO_ANSWER] += 1

            # Функция, определяющая вердикт работы от количества вердиктов по задачам
            ret[k] = set_work_verdict(answers)
    else:
        for k in list(tree1.keys()):
            if k in list(tree2.keys()):
                ret[k] = merge_tree(tree1[k], tree2[k], user)
            else:
                ret[k] = init_personal_tree(tree1)
    return ret

def analyze_answer(request, task, taskname):
    if request.POST.getlist('checks'):
        answer = request.POST.getlist('checks')
    else:
        form = AddAnswerForm(request.POST) 
        if form.is_valid():
            answer = form.cleaned_data['answer'].strip()

    # Правильный ответ
    if task.test(answer):
        with LateremUser(request.user.email) as user:
            print(taskname)
            argtaskname = taskname[taskname.find('_id') + 3:]
            argworkpath = taskname[:taskname.find('_id')]
            argworkpath = argworkpath.replace('.', SEPARATOR)
            user.set_verdict(argworkpath, argtaskname, Verdicts.OK)

            request.session['personal_tree'] = merge_tree(WORK_DIR, user.raw_verdicts, user)
            
        return HttpResponseRedirect('/completed/')
    
    # Неправильный ответ
    with LateremUser(request.user.email) as user:
        argtaskname = taskname[taskname.find('_id') + 3:]
        argworkpath = taskname[:taskname.find('_id')]
        argworkpath = argworkpath.replace('.', SEPARATOR)
        user.set_verdict(argworkpath, argtaskname, Verdicts.WRONG_ANSWER)
        
        request.session['personal_tree'] = merge_tree(WORK_DIR, user.raw_verdicts, user)


    return HttpResponseRedirect('/failed/')
