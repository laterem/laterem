import os
from os.path import join as pathjoin
import json
from ltc.ltc_compiler import LTCCompiler, LTC, LTCMetadataManager
from context_objects import TASK_SCANNER, TASK_UPLOAD_PATH, TASK_VIEW_UPLOAD_PATH
from extratypes import DBHybrid, NotSpecified
from core_app.models import LateremGroup, LateremUser, LateremSolution, LateremTask, LateremCategory, LateremWork, LateremTaskTemplate
from shutil import rmtree
from .solutions import Solution

TEMPLATES_VIEW_PATH = pathjoin('core_app', 'templates', TASK_VIEW_UPLOAD_PATH)
if not os.path.exists(TASK_UPLOAD_PATH):
    os.makedirs(TASK_UPLOAD_PATH)
if not os.path.exists(TEMPLATES_VIEW_PATH):
    os.makedirs(TEMPLATES_VIEW_PATH)    

class TaskTemplate(DBHybrid):
    __dbmodel__ = LateremTaskTemplate

    def __str__(self):
        return self.identificator()
    
    @classmethod
    def new(cls, name, config, view, author):
        dbobj = cls.__dbmodel__.objects.create(name=name,
                                               author=author.dbmodel)
        dbobj.save()
        tt = cls(dbobj)
        path = pathjoin(TASK_UPLOAD_PATH, tt.identificator())
        os.makedirs(path)

        with open(pathjoin(path, "config.ltc"), "wb+") as dest:
            for chunk in config.chunks():
                dest.write(chunk)
        with open(pathjoin(TEMPLATES_VIEW_PATH, f"{tt}.html"), "wb+") as dest:
            for chunk in view.chunks():
                dest.write(chunk)

        return tt

    @classmethod
    def delete(cls, id):
        this = cls.by_id(id)
        if os.path.isdir(this.dir_path):
            rmtree(this.dir_path)
        if os.path.isfile(this.view_path_absolute):
            os.remove(this.view_path_absolute)
        this.dbmodel.delete()

    @property
    def dir_path(self):
        return pathjoin(TASK_UPLOAD_PATH, str(self))
    
    @property
    def view_path(self):
        return pathjoin(TASK_VIEW_UPLOAD_PATH, str(self) + '.html')
    
    @property
    def view_path_absolute(self):
        return pathjoin(TEMPLATES_VIEW_PATH, str(self) +'.html')

    @property
    def ltc_path(self):
        return pathjoin(TASK_UPLOAD_PATH, str(self), 'config.ltc')
    
    def open_view(self):
        return open(self.view_path_absolute)
    
    def open_ltc(self):
        return open(self.ltc_path)
    
    def identificator(self):
        return f'ID{self.dbmodel.id}-{self.dbmodel.name}'

class Task(DBHybrid):
    __dbmodel__ = LateremTask

    @property 
    def work(self):
        return Work(self.dbmodel.work)

    @property
    def template(self):
        return TaskTemplate(self.dbmodel.task_type)

    @property
    def view_path(self):
        return self.template.view_path

    @property
    def field_overrides(self):
        return json.loads(self.dbmodel.field_overrides)

    def solutions(self, group=NotSpecified):
        if group is NotSpecified:
            return map(Solution, LateremSolution.objects.filter(task=self.dbmodel))
        else:
            users = LateremUser.objects.filter(lateremgroupmembership__group=group.dbmodel)
            return map(Solution, LateremSolution.objects.filter(task=self.dbmodel,
                                                                user__in=users))

    def generate_metadata(self, user):
        metadata = LTCMetadataManager()
        metadata.seed = self.id * 109231 ^ user.id * 2913884
        metadata.salt = self.id * 423 ^ user.id * 562
        metadata.xor = self.id * 3294829 ^ user.id * 6456484
        return metadata

    def compile(self, user, answers=NotSpecified):
        if answers is NotSpecified:
            answers = {}
        else:
            answers = {key: (value if (len(value) - 1) else value[0])
                       for key, value in answers.items()}
        with open(self.template.ltc_path, mode='r', encoding='UTF-8') as f:
            data = f.read()
        ltcc = LTCCompiler()
        ltc = ltcc.compile(data)
        extend_ns = self.field_overrides
        extend_ns.update(answers)
        with self.template.open_view() as io:
            ltc.feed_html(io.read())
        metadata = self.generate_metadata(user)
        ltc.execute(extend_ns, metadata)
        print(metadata.seed)
        
        view = self.view_path
        return CompiledTask(ltc, view)

class CompiledTask():
    def __init__(self, ltc, view) -> None:
        self.ltc = ltc
        self.template = view

    @classmethod
    def from_JSON(cls, data):
        d = json.loads(data)
        ltc = LTC.from_dict(d)
        template = d['template']
        return cls(ltc, template)
    
    #def test(self, fields) -> int:
    #    fields = {key: (value if (len(value) - 1) else value[0])
    #              for key, value in fields.items()}
    #    return self.ltc.check(fields)
    
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
    
    def groups(self):
        from .groups import Group
        return [Group(x) for x in LateremGroup.objects.filter(lateremassignment__work=self.dbmodel)]

    def get_answers(self, group=NotSpecified):
        ret = []
        for task in self.tasks():
            ret.extend(list(task.solutions(group=group)))
        return ret

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
        if isinstance(task_type, str):
            task_type = TaskTemplate.by_id(int(task_type[len('ID'):task_type.find('-')])) 

        task = Task(LateremTask.objects.create(name=name,
                                               task_type=task_type.dbmodel,
                                               work=self.dbmodel))
        task.dbmodel.save()
        return task

    def remove_task(self, task):
        task.dbmodel.delete()

class Category(DBHybrid):
    __dbmodel__ = LateremCategory

    has_children = True
        
    @staticmethod
    def roots():
        cat = [Category(x) for x in LateremCategory.objects.filter(root_category__isnull=True)]
        wor = [Work(x) for x in LateremWork.objects.filter(category__isnull=True)]
        return cat + wor
    
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

    def categories(self, accessible_for=NotSpecified, access_buffer=NotSpecified):
        result = []
        for x in LateremCategory.objects.filter(root_category=self.dbmodel.id):
            cat = Category(x)
            if accessible_for is not NotSpecified:
                if cat.is_visible(accessible_for, access_buffer):
                    result.append(cat)
            else:
                 result.append(cat)
        return result

    def works(self, accesible_for=NotSpecified, access_buffer=NotSpecified):
        result = []
        for x in LateremWork.objects.filter(category=self.dbmodel):
            work = Work(x)
            if accesible_for is not NotSpecified:
                if work in access_buffer:
                    if access_buffer[work]:
                        result.append(work)
                    continue
                if accesible_for.has_access(work):
                    if access_buffer is not NotSpecified:
                        access_buffer[work] = True
                    result.append(work)
            else:
                if access_buffer is not NotSpecified:
                    access_buffer[work] = True
                result.append(work)
        return result

    def children(self, *args, **kwargs):
        return self.categories(*args, **kwargs) + self.works(*args, **kwargs)

class RootsMimic:
    __dbmodel__ = None
    has_children = True

    def children(self, accesible_for=NotSpecified, access_buffer=NotSpecified):
        if access_buffer is NotSpecified:
            access_buffer = {}

        roots = Category.roots()

        return [root for root in roots if root.is_visible(accesible_for, access_buffer)]