from core_app.models import LateremSolution
from extratypes import DBHybrid

class Verdicts:
    OK = 'OK'
    SENT = 'ST'
    WRONG_ANSWER = 'WA'
    PARTIALLY_SOLVED = 'PS'
    NO_ANSWER = 'NA'

class Solution(DBHybrid):
    __dbmodel__ = LateremSolution

class NASolution:
    user = None
    task = None
    verdict = Verdicts.NO_ANSWER
    answers = '{}'
    timestamp = None
    teacher_comment = ''