from context_objects import SEPARATOR, SPACE_REPLACER
import json
from .tasks import Verdicts
from extratypes import DBHybrid

class Work(DBHybrid):
    def __init__(self, dbobj):
        super().__init__(dbobj)


    @staticmethod
    def stat_to_average_verdict(stats):
        ok = stats[Verdicts.OK] or stats[Verdicts.SENT]
        na = stats[Verdicts.NO_ANSWER]
        wa = stats[Verdicts.WRONG_ANSWER]
        ps = stats[Verdicts.PARTIALLY_SOLVED]
        # Нечитабельная булевошизия, знаю, но кароче это то же самое, что set_work_verdict
        if (ok and ((not na) and (not wa) and (not ps))):
            return GroupVerdict.ALL_CORRECT
        elif (ok or ps):
            return GroupVerdict.PARTIALLY_SOLVED
        else:
            return GroupVerdict.NOT_STARTED

    @staticmethod
    def split_full_name(full_name, separator=SEPARATOR, space_replacement=SPACE_REPLACER):
        return full_name.replace(space_replacement, ' ').split(separator)
    
    def get_tasks_ids(self):
        return list(self.tasks.items())