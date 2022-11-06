import json
from os.path import isfile
from context_objects import SEPARATOR
from .tasks import Verdicts
from .works import Work, GroupVerdict

DEFAULT_SETTINGS = {'theme': 'dark',
                    }


class User:
    def __init__(self, login):
        self.login = login
        self.username = login
        self.loaded = False
        self.modified = False
    
    def __enter__(self):
        self.load_json()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def open(self):
        self.load_json()
        return self
    
    def close(self):
        self.dump_json()

    @property
    def _jsonpath(self):
        return 'data' + SEPARATOR + 'userdata' + SEPARATOR + 'personal' + SEPARATOR + self.login + '.json'

    def _load_dummy(self):
        self.raw_available_branches = {}
        self.raw_verdicts = {}
        self.raw_settings = {}
    
    def get_setting(self, setting):
        return self.raw_settings[setting] if setting in self.raw_settings else DEFAULT_SETTINGS[setting]
    
    def set_setting(self, setting, value):
        self.raw_settings[setting] = value
        self.modified = True
    
    def load_json(self):
        if not isfile(self._jsonpath):
            self._load_dummy()
        else:
            with open(self._jsonpath, 'r', encoding='utf-8') as f:
                d = json.load(f)
                self.raw_available_branches = d['available_branches']
                self.raw_verdicts = d['verdicts']
                self.raw_settings = d['settings']
            
            self.loaded = True
            return d
        self.modified = False
    
    def dump_json(self):
        with open(self._jsonpath, 'w', encoding='utf-8') as f:
            data = {'available_branches': self.raw_available_branches,
                    'verdicts': self.raw_verdicts,
                    'settings': self.raw_settings}
            json.dump(data, f, sort_keys=True, indent=4,
                      ensure_ascii=False)
        self.modified = False
    
    def get_task_verdict(self, worklayers, taskname):
        cd = self.raw_verdicts
        for layer in worklayers:
            if layer not in cd:
                return Verdicts.NO_ANSWER
            cd = cd[layer]
        return cd[taskname] if taskname in cd else Verdicts.NO_ANSWER
    
    def get_task_verdicts(self, worklayers, tasknames):
        cd = self.raw_verdicts
        for layer in worklayers:
            if layer not in cd:
                return Verdicts.NO_ANSWER
            cd = cd[layer]
        return [(cd[taskname] if taskname in cd else Verdicts.NO_ANSWER)
                for taskname in tasknames]
    
    def get_work_stats(self, worklayers):
        cd = self.raw_verdicts
        for layer in worklayers:
            if layer not in cd:
                return GroupVerdict.NOT_STARTED
            cd = cd[layer]
        work = Work(worklayers)

        na = 0
        wa = 0
        ps = 0
        ok = 0
        st = 0
        for task in work.tasks.keys():
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

        return {Verdicts.OK: ok,
                Verdicts.PARTIALLY_SOLVED: ps,
                Verdicts.SENT: st,
                Verdicts.WRONG_ANSWER: wa,
                Verdicts.NO_ANSWER: na}

    def get_work_verdict(self, worklayers):
        stat = self.get_work_stats(worklayers)
        ok = stat[Verdicts.OK] or stat[Verdicts.SENT]
        na = stat[Verdicts.NO_ANSWER]
        wa = stat[Verdicts.WRONG_ANSWER]
        ps = stat[Verdicts.PARTIALLY_SOLVED]
        # Нечитабельная булевошизия, знаю, но кароче это то же самое, что set_work_verdict
        if (ok and ((not na) and (not wa) and (not ps))):
            return GroupVerdict.ALL_CORRECT
        elif (ok or ps):
            return GroupVerdict.PARTIALLY_SOLVED
        else:
            return GroupVerdict.NOT_STARTED

    def set_verdict(self, worklayers, taskname, verdict):
        cd = self.raw_verdicts
        for layer in worklayers:
            if layer not in cd:
                cd[layer] = {}
            cd = cd[layer]
        cd[taskname] = verdict
        self.modified = True

    def open_branch(self, categorypath):
        worklayers = categorypath.split(SEPARATOR)
        cd = self.raw_available_branches
        for layer in worklayers:
            if layer not in cd:
                cd[layer] = {}
            cd = cd[layer]
        self.modified = True
