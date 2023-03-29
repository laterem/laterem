from context_objects import USER_DEFAULT_SETTINGS
from .tasks import Work
from .groups import Group
from core_app.models import (
    LateremAssignment,
    LateremUser,
    LateremGroup,
    LateremWork,
    LateremSolution,
)
from commons import DBHybrid, NotSpecified
import json
import datetime


class User(DBHybrid):
    __dbmodel__ = LateremUser

    def __init__(self, dbobj):
        super().__init__(dbobj)

    def __str__(self):
        return self.username

    @property
    def username(self):
        return (
            (" ".join((self.dbmodel.first_name, self.dbmodel.last_name)))
            or self.dbmodel.username
            or self.dbmodel.email
        )

    @classmethod
    def create(
        cls, email, password, first_name=NotSpecified, last_name=NotSpecified
    ):
        if first_name is NotSpecified:
            first_name = email
        if last_name is NotSpecified:
            last_name = ""
        LateremUser.objects.create_user(
            email=email,
            password=password,
            username=email,
            first_name=first_name,
            last_name=last_name,
            settings="{}",
        )

    def groups(self):
        return [
            Group(x)
            for x in LateremGroup.objects.filter(
                lateremgroupmembership__user=self.dbmodel
            )
        ]

    def available_works(self):
        return [
            Work(x)
            for x in LateremWork.objects.filter(
                lateremassignment__user=self.dbmodel
            )
        ]

    def has_global_permission(self, name):
        # TODO: Оптимизировать сырым SQL запросом / вырезать

        return bool(
            [
                x
                for x in LateremGroup.objects.filter(
                    lateremgroupmembership__user=self.dbmodel
                )
                if x.__getattribute__(name) == True
            ]
        )

    def is_teacher(self):
        for perm in (
            "can_manage_users",
            "can_manage_works",
            "can_manage_groups",
            "can_manage_tasks",
        ):
            if self.has_global_permission(perm):
                return True
        return False

    def solve(self, task, answers, verdict):
        new = LateremSolution.objects.create(
            user=self.dbmodel,
            task=task.dbmodel,
            verdict=verdict,
            answers=json.dumps(answers),
            teacher_comment="",
            timestamp=datetime.datetime.now(),
        )
        new.save()
        return new

    def has_access(self, work):
        if self.has_global_permission("can_manage_works"):
            return True

        for group in self.groups():
            assignments = LateremAssignment.objects.filter(
                group=group.dbmodel, work=work.dbmodel
            )
            if assignments:
                return True
        assignments = LateremAssignment.objects.filter(
            user=self.dbmodel, work=work.dbmodel
        )
        if assignments:
            return True
        return False

    def get_task_solution(self, task):
        from .solutions import Solution, NASolution

        solutions = LateremSolution.objects.filter(
            user=self.dbmodel,
            task=task.dbmodel,
        )
        if solutions:
            return Solution(solutions.latest("timestamp"))
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
        from .solutions import Verdicts

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

        if tasks and normalize:
            s = na + wa + ps + ok + st
            na = na / s
            wa = wa / s
            ps = ps / s
            ok = ok / s
            st = st / s

        return {
            Verdicts.OK: ok,
            Verdicts.PARTIALLY_SOLVED: ps,
            Verdicts.SENT: st,
            Verdicts.WRONG_ANSWER: wa,
            Verdicts.NO_ANSWER: na,
        }
