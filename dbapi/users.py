from context_objects import USER_DEFAULT_SETTINGS
from .solutions import Verdicts, Solution, NASolution
from .tasks import Work
from .groups import Group
from core_app.models import LateremAssignment, LateremUser, LateremGroup, LateremWork, LateremSolution
from extratypes import DBHybrid
import json
import datetime

class User(DBHybrid):
    __dbmodel__ = LateremUser

    def __init__(self, dbobj):
        super().__init__(dbobj)

    def groups(self):
        return [Group(x) for x in LateremGroup.objects.filter(lateremgroupmembership__user=self.dbmodel)]

    def available_works(self):
        return [Work(x) for x in LateremWork.objects.filter(lateremassignment__user=self.dbmodel)]

    def has_global_permission(self, name):
        # TODO: Оптимизировать сырым SQL запросом / вырезать
        return bool([x for x in LateremGroup.objects.filter(lateremgroupmembership__user=self.dbmodel) if x.__getattribute__(name) == True])

    def solve(self, task, answers, verdict):
        new = LateremSolution.objects.create(user=self.dbmodel,
                                             task=task.dbmodel,
                                             verdict=verdict,
                                             answers=json.dumps(answers),
                                             teacher_comment='',
                                             timestamp=datetime.datetime.now()
                                            )
        new.save()
        return new
    
    def has_access(self, work):
        for group in self.groups():
            assignments = LateremAssignment.objects.filter(group=group.dbmodel, work=work.dbmodel)
            if assignments: return True
        assignments = LateremAssignment.objects.filter(user=self.dbmodel, work=work.dbmodel) 
        if assignments: return True
        return False

    def get_task_solution(self, task):
        solutions = LateremSolution.objects.filter(user=self.dbmodel,
                                              task=task.dbmodel,
                                              )
        if solutions:
            return Solution(solutions.latest('timestamp'))
        else:
            fake = NASolution()
            fake.task = task
            fake.user = self
            return fake
    
    def set_settings(self, **settings):
        self.modified = True
        usettings = json.loads(self.dbmodel.settings)
        for key, value in settings.items():
            usettings[key] = value
        self.dbmodel.settings = json.dumps(usettings)
    
    def get_setting(self, setting):
        settings = json.loads(self.dbmodel.settings)
        if setting in settings:
            return settings[setting]
        else:
            return USER_DEFAULT_SETTINGS[setting]

    def get_work_stats(self, work, normalize=False):
        tasks = work.tasks()
        na = 0
        wa = 0
        ps = 0
        ok = 0
        st = 0
        for task in tasks:
            verdict = self.get_task_solution(task).verdict
            if verdict == Verdicts.WRONG_ANSWER:
                wa += 1
            elif verdict == Verdicts.PARTIALLY_SOLVED:
                ps += 1
            elif verdict == Verdicts.SENT:
                st += 1
            elif verdict == Verdicts.OK:
                ok += 1
            else:
                na += 1
                
        if normalize:
            s = na + wa + ps + ok + st
            na = na / s
            wa = wa / s
            ps = ps / s
            ok = ok / s
            st = st / s

        return {Verdicts.OK: ok,
                Verdicts.PARTIALLY_SOLVED: ps,
                Verdicts.SENT: st,
                Verdicts.WRONG_ANSWER: wa,
                Verdicts.NO_ANSWER: na}

