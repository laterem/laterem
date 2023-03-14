from core_app.models import LateremSolution
from commons import DBHybrid
import json

class Verdicts:
    OK = 'OK'
    SENT = 'ST'
    WRONG_ANSWER = 'WA'
    PARTIALLY_SOLVED = 'PS'
    NO_ANSWER = 'NA'


class SolutionView:
    __dbmodel__ = LateremSolution

    filters = {}

    @classmethod
    def register_filter(cls, name):
        def deco(func):
            cls.filters[name] = func
            return func
        return deco


    def __init__(self, work, group):
        self.work = work
        self.group = group

    def view_jsonconf(self, obj):
        filters = []
        if 'filters' in obj:
            for name, *args in obj['filters']:
                filters.append(self.filters[name](*args))
        
        return self.view(group_by=obj['group_by'],
                         filters=filters,)
    
    def view(self, group_by='none', filters=None,):
        from .users import User
        from .tasks import Task
        obj = {}
        all_solutions = self.work.get_answers(self.group)
        if group_by == 'none':
            obj["main"] = []
            for sol in all_solutions:
                flag = True
                for filter in filters:
                    if not filter(sol):
                        flag = False
                        break
                if not flag:
                    continue
                obj["main"].append(sol)
            return obj
        elif group_by == 'user':
            all_users = [User(sol.dbmodel.user) for sol in all_solutions]
            for user in all_users:
                obj[user] = userfilter(user.id)
        elif group_by == 'task':
            all_tasks = [Task(sol.dbmodel.task) for sol in all_solutions]
            for task in all_tasks:
                obj[task] = taskfilter(task.id)
        elif group_by == 'verdict':
            all_verdicts = [sol.dbmodel.verdict for sol in all_solutions]
            for verdict in all_verdicts:
                obj[verdict] = verdictfilter(verdict)
        for label, filter in obj.items():
            obj[label] = []
            for sol in all_solutions:
                flag = True
                for fr in filters + [filter]:
                    if not fr(sol):
                        flag = False
                        break
                if not flag:
                    continue
                obj[label].append(sol)
        return obj

                

class Solution(DBHybrid):
    __dbmodel__ = LateremSolution

    @property
    def answers(self):
        return json.loads(self.dbmodel.answers)

    @property
    def items_answers(self):
        return list(self.answers.items())

class NASolution:
    user = None
    task = None
    verdict = Verdicts.NO_ANSWER
    answers = {}
    timestamp = None
    teacher_comment = ''


@SolutionView.register_filter('user')
def userfilter(user_id):
    def filt(sol):
        return sol.dbmodel.user.id == user_id
    return filt

@SolutionView.register_filter('verdict')
def verdictfilter(verdict):
    verdict = verdict.lower()
    def filt(sol):
        return sol.dbmodel.verdict.lower() == verdict
    return filt

@SolutionView.register_filter('task')
def taskfilter(task_id):
    def filt(sol):
        return sol.dbmodel.task.id == task_id
    return filt
