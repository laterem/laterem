from context_objects import SEPARATOR
from .tasks import Verdicts
from .works import Work
from .groups import Group
from core_app.models import LateremGroupMembership, LateremGroup, LateremWork
from extratypes import DBHybrid

class User(DBHybrid):
    def __init__(self, dbobj):
        super().__init__(dbobj)

    def groups(self):
        return [Group(x) for x in LateremGroup.objects.filter(lateremgroupmembership__user=self.dbmodel)]

    def available_works(self):
        return [Work(x) for x in LateremWork.objects.filter(lateremassignment__user=self.dbmodel)]

    def get_task_verdict(self, worklayers, taskname):
        return NotImplemented

        cd = self.raw_verdicts
        for layer in worklayers:
            if layer not in cd:
                return Verdicts.NO_ANSWER
            cd = cd[layer]
        return cd[taskname] if taskname in cd else Verdicts.NO_ANSWER
    
    def get_task_verdicts(self, worklayers, tasknames):
        return NotImplemented

        cd = self.raw_verdicts
        for layer in worklayers:
            if layer not in cd:
                return [Verdicts.NO_ANSWER for _ in tasknames]
            cd = cd[layer]
        return [(cd[taskname] if taskname in cd else Verdicts.NO_ANSWER)
                for taskname in tasknames]
    
    def get_work_stats(self, worklayers, normalize=False):
        return NotImplemented

        cd = self.raw_verdicts
        work = Work(worklayers)
        tasks = work.tasks.keys()
        for layer in worklayers:
            if layer not in cd:
                na = 1 if normalize else len(tasks)
                return {Verdicts.OK: 0,
                        Verdicts.PARTIALLY_SOLVED: 0,
                        Verdicts.SENT: 0,
                        Verdicts.WRONG_ANSWER: 0,
                        Verdicts.NO_ANSWER: na}
            cd = cd[layer]

        na = 0
        wa = 0
        ps = 0
        ok = 0
        st = 0
        for task in tasks:
            if task not in cd: 
                na += 1
                continue
            verdict = cd[task]
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

    def get_work_verdict(self, worklayers=None):
        return NotImplemented

        stats = self.get_work_stats(worklayers)
        return Work.stat_to_average_verdict(stats)

    def set_verdict(self, worklayers, taskname, verdict):
        return NotImplemented

        cd = self.raw_verdicts
        for layer in worklayers:
            if layer not in cd:
                cd[layer] = {}
            cd = cd[layer]
        cd[taskname] = verdict
        self.modified = True

    def open_branch(self, categorypath):
        return NotImplemented

        worklayers = categorypath.split(SEPARATOR)
        cd = self.raw_available_branches
        for layer in worklayers:
            if layer not in cd:
                cd[layer] = {}
            cd = cd[layer]
        self.modified = True
