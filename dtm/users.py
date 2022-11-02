import json
from os import isfile
from context_objects import SEPARATOR
from tasks import Verdicts

class User:
    def __init__(self, login):
        self.login = login
        self.loaded = False
        self.modified = False
    
    def __enter__(self):
        self.load_json()
    
    def __exit__(self):
        self.close()
    
    def close(self):
        self.dump_json()

    def _jsonpath(self):
        return 'data' + SEPARATOR + 'userdata' + SEPARATOR + 'personal' + SEPARATOR + self.login + '.json'

    def _load_dummy(self):
        self.raw_available_branches = {}
        self.raw_verdicts = {}
    
    def load_json(self):
        if not isfile(self._jsonpath):
            self._load_dummy()
        else:
            with open(self._jsonpath(), 'r', encoding='UTF-8') as f:
                d = json.load(f)
                self.raw_available_branches = d['available_branches']
                self.raw_verdicts = d['verdicts']
            
            self.loaded = True
            return d
        self.modified = False
    
    def dump_json(self):
        with open(self._jsonpath(), 'w', encoding='UTF-8') as f:
            data = {'available_branches': self.raw_available_branches,
                    'verdicts': self.raw_verdicts}
            json.dump(data, f)
        self.modified = False
    
    def get_task_verdict(self, workpath, taskname):
        worklayers = workpath.split(SEPARATOR)
        cd = self.raw_verdicts
        for layer in worklayers:
            if layer not in cd:
                return False
            cd = cd[layer]
        return cd[taskname] if taskname in cd else Verdicts.NO_ANSWER

    def set_verdict(self, workpath, taskname, verdict):
        worklayers = workpath.split(SEPARATOR)
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
