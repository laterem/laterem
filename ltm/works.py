from context_objects import SEPARATOR, SPACE_REPLACER
import json

class GroupVerdict:
    ALL_CORRECT = 'OK'
    PARTIALLY_SOLVED = 'PS'
    NOT_STARTED = 'NA'

class Work:
    _cache = {}

    def __init__(self, worklayers):
        self.path = worklayers
        self.load_json()
    
    @property
    def _jsonpath(self):
        return 'data' + SEPARATOR + 'works' + SEPARATOR + SEPARATOR.join(self.path) + '.json'

    def load_json(self, cache=True):
        p = self._jsonpath

        if p in Work._cache:
            d = Work._cache[p]
            self.title = d['title']
            self.tasks = d['tasks']
            return
        with open(p, mode='r', encoding='utf-8') as f:
            d = json.load(f)
            self.title = d['title']
            self.tasks = d['tasks']
        if cache:
            Work._cache[p] = d

    
    def get_full_name(self, separator=SEPARATOR, space_replacement=SPACE_REPLACER):
        return separator.join(self.path).replace(' ', space_replacement)
    
    @staticmethod
    def split_full_name(full_name, separator=SEPARATOR, space_replacement=SPACE_REPLACER):
        return full_name.replace(space_replacement, ' ').split(separator)
    
    def get_tasks_ids(self):
        return list(self.tasks.items())