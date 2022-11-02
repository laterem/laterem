import os
import shutil
import json
from dtc.dtc_compiler import DTCCompiler, DTC
from context_objects import DTM_SCANNER

TEMPLATE_CLONING_PATH = 'core_app/templates/static_copies/'
if not os.path.exists(TEMPLATE_CLONING_PATH):
    os.makedirs(TEMPLATE_CLONING_PATH)


def open_dtc(path):
    if not path.endswith('.dtc'):
        path += '.dtc'
    with open(path, mode='r', encoding='UTF-8') as f:
        data = f.read()
    dtcc = DTCCompiler()
    dtc = dtcc.compile(data)
    dtc.execute()
    return dtc


class TaskData():
    def __init__(self, dtc, template) -> None:
        self.dtc = dtc
        self.template = template

    @classmethod
    def from_JSON(cls, data):
        d = json.loads(data)
        dtc = DTC.from_dict(d)
        template = d['template']
        return cls(dtc, template)

    @classmethod
    def open(cls, taskname):
        path = DTM_SCANNER.id_to_path(taskname)
        dtcpath = os.path.join(path, 'config.dtc')
        viewpath = os.path.join(path, 'view.html')
        tmpviewpath = taskname + '_view' + '.html'

        shutil.copyfile(viewpath, TEMPLATE_CLONING_PATH + tmpviewpath)
        
        dtc = open_dtc(dtcpath)
        template = 'static_copies/' + tmpviewpath
        return cls(dtc, template)
    
    def test(self, answer) -> int:
        fields = {'answer': answer}
        return self.dtc.check(fields)
    
    def as_JSON(self):
        d = self.dtc.to_dict()
        d['template'] = self.template
        return json.dumps(d, indent=4)
