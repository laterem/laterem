import json
from context_objects import SEPARATOR


class User:
    def __init__(self, login):
        return NotImplemented
        self.login = login

    def _jsonpath(self):
        return 'data' + SEPARATOR + 'userdata' + SEPARATOR + 'personal' + SEPARATOR + self.login + '.json'

    def _register_empty_json(self):
        return NotImplemented
    
    def load_json(self):
        return NotImplemented

        with open(self._jsonpath(), 'r', encoding='UTF-8') as f:
            d = json.load(f)