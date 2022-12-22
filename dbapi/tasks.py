import os
import shutil
import json
from ltc.ltc_compiler import LTCCompiler, LTC
from context_objects import LTM_SCANNER
from extratypes import DBHybrid, NotSpecified
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

    has_children = False

    def __init__(self, dbobj):
        super().__init__(dbobj)
    
    def tasks(self):
        return [Task(x) for x in LateremTask.objects.filter(work=self.dbmodel)]
    
    def is_valid(self):
        return not not self.tasks()
    
    def __hash__(self):
        return hash('WR' + str(self.id))

    def is_visible(self, user, access_buffer=NotSpecified):
        if user is None or user is NotSpecified:
            if access_buffer is not NotSpecified:
                access_buffer[self] = True
            return True

        if user.has_global_permission('can_manage_works'):
            if access_buffer is not NotSpecified:
                access_buffer[self] = True
            return True

        if access_buffer is not NotSpecified:
            if self in access_buffer:
                return access_buffer[self]
            else:
                access_buffer[self] = self.is_valid() and user.has_access(self)
                return access_buffer[self]
        return user.has_access(self)
    
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

    has_children = True

    def is_visible(self, user, access_buffer=NotSpecified):
        if user is None or user is NotSpecified:
            if access_buffer is not NotSpecified:
                access_buffer[self] = True
            return True
        if user.has_global_permission('can_manage_works'):
            if access_buffer is not NotSpecified:
                access_buffer[self] = True
            return True
        if access_buffer is not NotSpecified:
            if self in access_buffer:
                return access_buffer[self]
            else:
                result = any(map(lambda x: x.is_visible(user, access_buffer), self.children()))
                access_buffer[self] = result
                return result
        return any(map(lambda x: x.is_visible(user, access_buffer), self.children()))

    def __hash__(self):
        return hash('WC' + str(self.id))

    def works(self, accesible_for=None):
        if accesible_for:
            return [Work(x) for x in LateremWork.objects.filter(category=self.dbmodel)
                    if accesible_for.has_access(Work(x))]
        else:
            return [Work(x) for x in LateremWork.objects.filter(category=self.dbmodel)]
    
    def children(self, *args, **kwargs):
        return self.works(*args, **kwargs)

class Category(DBHybrid):
    __dbmodel__ = LateremCategoryCategory

    has_children = True
        
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
    
    def __hash__(self):
        return hash('CC' + str(self.id))
    
    def is_visible(self, user, access_buffer=NotSpecified):
        if user is None or user is NotSpecified:
            if access_buffer is not NotSpecified:
                access_buffer[self] = True
            return True
        if user.has_global_permission('can_manage_works'):
            if access_buffer is not NotSpecified:
                access_buffer[self] = True
            return True
        if access_buffer is not NotSpecified:
            if self in access_buffer:
                return access_buffer[self]
            else:
                result = any(map(lambda x: x.is_visible(user, access_buffer), self.children()))
                access_buffer[self] = result
                return result
        return any(map(lambda x: x.is_visible(user, access_buffer), self.children()))

    def categories(self, accessible_for=None, access_buffer=NotSpecified):
        result = []

        for x in LateremWorkCategory.objects.filter(root_category=self.dbmodel):
            cat = WorkCategory(x)
            if accessible_for is not NotSpecified:
                if cat.is_visible(accessible_for, access_buffer):
                    result.append(cat)
            else:
                 result.append(cat)
        for x in LateremCategoryCategory.objects.filter(root_category=self.dbmodel.id):
            cat = Category(x)
            if accessible_for is not NotSpecified:
                if cat.is_visible(accessible_for, access_buffer):
                    result.append(cat)
            else:
                 result.append(cat)

        return result

    def children(self, *args, **kwargs):
        return self.categories(*args, **kwargs)

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

class RootsMimic:
    has_children = True

    def children(self, accesible_for=NotSpecified, access_buffer=NotSpecified):
        if access_buffer is NotSpecified:
            access_buffer = {}

        roots = Category.roots()

        return [root for root in roots if root.is_visible(accesible_for, access_buffer)]