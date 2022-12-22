from .forms import *
from dbapi.solutions import Verdicts
from dbapi.tasks import Category, Work, RootsMimic
from dbapi.groups import Group
from dbapi.users import User
from .models import LateremUser
from extratypes import NotSpecified
from context_objects import LATEREM_FLAGS, DEBUG_DBSamples

if DEBUG_DBSamples in LATEREM_FLAGS:
    from secret_data import ADMIN_PASSWORD
    def DEBUG_assure_admin(email='admin@admin.admin',
                        password=ADMIN_PASSWORD):
        admin = LateremUser.objects.filter(email=email)
        if not admin:
            admin = LateremUser.objects.create_user(email=email, password=password, username=email, settings='{}')
            admin.save()
            testcat = LateremWorkCategory.objects.create(name='Misc.')
            admins = LateremGroup.objects.create(name="ADMINS",
                                                can_solve_tasks=True,
                                                can_manage_groups=True,
                                                can_manage_users=True,
                                                can_manage_works=True)

            with Group(admins) as gr:
                gr.add_member(User(admin), is_group_admin=True)
            admins.save()
            testcat.save()
            print('\n')
            print('|\t В базе данных не было обнаружено пользователя-админа, поэтому')
            print('|\t были созданы следующие тестовые сущности:')
            print('|\t - Пользователь-админ ' + f'("{email}"; "{password}")')
            print('|\t - Группа админов ("ADMINS")')
            print('|\t - Категория для работ ("Misc.")')
            print('\n')
else:
    def DEBUG_assure_admin(*args, **kwargs):
        pass

def render_args(*, 
                me=NotSpecified, 
                current_task=NotSpecified,
                current_work=NotSpecified,
                current_group=NotSpecified,
                meta_all_users_available=False,
                meta_all_groups_available=False,
                meta_all_works_available=False,
                additional={}
                ):
    ret = {}

    if me is not NotSpecified:
        #if meta_all_works_available:
        #    ret['workdir'] = RootsMimic.children()
       #else:
        #    ret['workdir'] = RootsMimic.children(me)
        ret['workdir'] = RootsMimic()
        ret['user'] = me
        ret['theme'] = me.get_setting('theme')
        ret['is_teacher'] = True
    
    if current_task is not NotSpecified:
        task_work = current_task.work
        if current_work is NotSpecified:
            current_work = task_work
        all_tasks_in_task_work = task_work.tasks()
        task_index = all_tasks_in_task_work.index(current_task)
        ret['task'] = current_task
        if (task_index >= 0) and task_index + 1 < len(all_tasks_in_task_work):
            ret['next_task'] = all_tasks_in_task_work[task_index + 1].id
        else:
            ret['next_task'] = all_tasks_in_task_work[0].id
    
    if current_work is not NotSpecified:
        all_tasks_in_work = current_work.tasks()
        ret['work'] = current_work
        ret['work_name'] = current_work.name
        _colors = {Verdicts.NO_ANSWER: 'no-answer',
                   Verdicts.OK: 'correct',
                   Verdicts.PARTIALLY_SOLVED: 'partial',
                   Verdicts.SENT: 'partial',
                   Verdicts.WRONG_ANSWER: 'wrong'}
        if me is not NotSpecified:
            ret['task_list'] = [(_task, _colors[me.get_task_solution(_task).verdict]) 
                                for _task in all_tasks_in_work]
        else:
            ret['task_list'] = [(_task, _colors[Verdicts.NO_ANSWER]) 
                                for _task in all_tasks_in_work]
    
    if current_group is not NotSpecified:
        ret['group'] = current_group

    if meta_all_users_available:
        ret['allusers'] = map(User, LateremUser.objects.all())
    
    if meta_all_groups_available:
        ret['allgroup'] = map(Group, LateremGroup.objects.all())
    
    if meta_all_works_available:
        ret['allworks'] = map(Work, LateremWork.objects.all())

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

def get_category_for_work(post, label='new-work_'):
    res = dict()
    for key, value in dict(post).items():
        print(key[:len(label)], label)
        if key[:len(label)] == label:
            res[key[len(label):]] = value
    return res
