import os
import shutil
import json
from ltc.ltc_compiler import LTCCompiler, LTC
from context_objects import LTM_SCANNER

TEMPLATE_CLONING_PATH = 'core_app/templates/static_copies/'
if not os.path.exists(TEMPLATE_CLONING_PATH):
    os.makedirs(TEMPLATE_CLONING_PATH)

class Verdicts:
    OK = 'OK'
    SENT = 'ST'
    WRONG_ANSWER = 'WA'
    PARTIALLY_SOLVED = 'PS'
    NO_ANSWER = 'NA'


def open_ltc(path):
    if not path.endswith('.ltc'):
        path += '.ltc'
    with open(path, mode='r', encoding='UTF-8') as f:
        data = f.read()
    ltcc = LTCCompiler()
    ltc = ltcc.compile(data)
    ltc.execute()
    return ltc


class TaskData():
    def __init__(self, ltc, template) -> None:
        self.ltc = ltc
        self.template = template

    @classmethod
    def from_JSON(cls, data):
        d = json.loads(data)
        ltc = LTC.from_dict(d)
        template = d['template']
        return cls(ltc, template)

    @classmethod
    def open(cls, taskname):
        path = LTM_SCANNER.id_to_path(taskname)
        ltcpath = os.path.join(path, 'config.ltc')
        viewpath = os.path.join(path, 'view.html')
        tmpviewpath = taskname + '_view' + '.html'

        shutil.copyfile(viewpath, TEMPLATE_CLONING_PATH + tmpviewpath)
        
        ltc = open_ltc(ltcpath)
        template = 'static_copies/' + tmpviewpath
        return cls(ltc, template)
    
    def test(self, fields) -> int:
        fields = {key: (value if (len(value) - 1) else value[0])
                  for key, value in fields.items()}
        return self.ltc.check(fields)
    
    def as_JSON(self):
        d = self.ltc.to_dict()
        d['template'] = self.template
        return json.dumps(d, indent=4)
