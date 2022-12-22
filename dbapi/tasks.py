import os
import shutil
import json
from ltc.ltc_compiler import LTCCompiler, LTC
from context_objects import LTM_SCANNER
from extratypes import DBHybrid
from core_app.models import LateremTask, LateremWorkCategory, LateremWork, LateremCategoryCategory

TEMPLATE_CLONING_PATH = 'core_app/templates/static_copies/'
if not os.path.exists(TEMPLATE_CLONING_PATH):
    os.makedirs(TEMPLATE_CLONING_PATH)

def open_ltc(path):
    if not path.endswith('.ltc'):
        path += '.ltc'
    with open(path, mode='r', encoding='UTF-8') as f:
        data = f.read()
    ltcc = LTCCompiler()
    ltc = ltcc.compile(data)
    ltc.execute()
    return ltc

class Task(DBHybrid):
    __dbmodel__ = LateremTask

    @property 
    def work(self):
        return Work(self.dbmodel.work)

    @property
    def template_path(self):
        task_type = self.dbmodel.task_type
        tmpviewpath = task_type + '_view' + '.html'
        return 'static_copies/' + tmpviewpath

    def compile(self):
        task_type = self.dbmodel.task_type
        path = LTM_SCANNER.id_to_path(task_type)
        ltcpath = os.path.join(path, 'config.ltc')
        viewpath = os.path.join(path, 'view.html')
        tmpviewpath = task_type + '_view' + '.html'

        shutil.copyfile(viewpath, TEMPLATE_CLONING_PATH + tmpviewpath)
        
        ltc = open_ltc(ltcpath)
        template = self.template_path
        return CompiledTask(ltc, template)


class CompiledTask():
    def __init__(self, ltc, template) -> None:
        self.ltc = ltc
        self.template = template

    @classmethod
    def from_JSON(cls, data):
        d = json.loads(data)
        ltc = LTC.from_dict(d)
        template = d['template']
        return cls(ltc, template)
    
    def test(self, fields) -> int:
        fields = {key: (value if (len(value) - 1) else value[0])
                  for key, value in fields.items()}
        return self.ltc.check(fields)
    
    def as_JSON(self):
        d = self.ltc.to_dict()
        d['template'] = self.template
        return json.dumps(d, indent=4)


class Work(DBHybrid):
    __dbmodel__ = LateremWork

    def __init__(self, dbobj):
        super().__init__(dbobj)
    
    def tasks(self):
        return [Task(x) for x in LateremTask.objects.filter(work=self.dbmodel)]
    
    def add_task(self, name, task_type):
        task = Task(LateremTask.objects.create(name=name,
                                               task_type=task_type,
                                               work=self.dbmodel))
        task.dbmodel.save()
        return task

    def remove_task(self, task):
        task.dbmodel.delete()

class WorkCategory(DBHybrid):
    __dbmodel__ = LateremWorkCategory

    def works(self, accesible_for=None):
        if accesible_for:
            return [Work(x) for x in LateremWork.objects.filter(category=self.dbmodel)
                    if accesible_for.has_access(Work(x))]
        else:
            return [Work(x) for x in LateremWork.objects.filter(category=self.dbmodel)]

class Category(DBHybrid):
    __dbmodel__ = LateremCategoryCategory

    @staticmethod
    def roots():
        catcat = [Category(x) for x in LateremCategoryCategory.objects.filter(root_category__isnull=True)]
        worcat = [WorkCategory(x) for x in LateremWorkCategory.objects.filter(root_category__isnull=True)]
        return catcat + worcat
        
    @staticmethod
    def global_tree(accesible_for=None):
        roots = Category.roots()
        ret = {}
        for child in roots:
            if child.__dbmodel__ == LateremCategoryCategory:
                result = child.tree(accesible_for)
            else:
                result = child.works(accesible_for)
            if result:
                ret[child.name] = result
        return ret

    def categories(self):
        return [WorkCategory(x) for x in LateremWorkCategory.objects.filter(root_category=self.dbmodel)] + \
            [Category(x) for x in LateremCategoryCategory.objects.filter(root_category=self.dbmodel.id)]

    def tree(self, accesible_for=None):
        children = self.categories()
        ret = {}
        for child in children:
            if child.__dbmodel__ == LateremCategoryCategory:
                result = child.tree(accesible_for)
            else:
                result = child.works(accesible_for)
            if result:
                ret[child.name] = result
        return ret