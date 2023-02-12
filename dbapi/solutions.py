from core_app.models import LateremSolution
from extratypes import DBHybrid
import json

class Verdicts:
    OK = 'OK'
    SENT = 'ST'
    WRONG_ANSWER = 'WA'
    PARTIALLY_SOLVED = 'PS'
    NO_ANSWER = 'NA'

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