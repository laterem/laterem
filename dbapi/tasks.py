from django.utils.text import slugify
from django.db.models import Max
import os
from os.path import join as pathjoin
import json
from uuid import uuid4
from ltc.ltc import (
    LTCCompiler,
    LTC,
    LTCMetadataManager,
    LTCFakeMetadata,
    LTCError,
    LTCCompileError,
    LTCExecutionError,
)
from context_objects import (
    TASK_SCANNER,
    TASK_UPLOAD_PATH,
    TASK_VIEW_UPLOAD_PATH,
    LTC_DEFAULT_EXPORT_VALUE,
)
from commons import DBHybrid, NotSpecified, transliterate_ru_en, read_text_file
from core_app.models import (
    LateremGroup,
    LateremUser,
    LateremSolution,
    LateremTask,
    LateremCategory,
    LateremWork,
    LateremTaskTemplate,
)
from shutil import rmtree

TEMPLATES_VIEW_PATH = pathjoin("core_app", "templates", TASK_VIEW_UPLOAD_PATH)
if not os.path.exists(TASK_UPLOAD_PATH):
    os.makedirs(TASK_UPLOAD_PATH)
if not os.path.exists(TEMPLATES_VIEW_PATH):
    os.makedirs(TEMPLATES_VIEW_PATH)


class TaskTemplateValidationFailed(Exception):
    pass


class TaskTemplate(DBHybrid):
    __dbmodel__ = LateremTaskTemplate

    def __str__(self):
        return self.identificator()

    @classmethod
    def new(cls, name, config, view, author, check_errors=True):
        dbobj_created = False
        try:
            if check_errors and config:
                ltcc = LTCCompiler()
                try:
                    ltcfile: str = read_text_file(config)
                    ltc = ltcc.compile(map(lambda x: x.decode(), ltcfile))
                    # ltc.execute(metadata=LTCFakeMetadata())
                except (LTCCompileError, LTCError, LTCExecutionError) as e:
                    raise TaskTemplateValidationFailed(str(e))

            dbobj = cls.__dbmodel__.objects.create(
                name=name, birthname=name, author=author.dbmodel
            )
            dbobj.save()
            dbobj_created = True
            tt = cls(dbobj)

            path = tt.dir_path
            os.makedirs(path)
            os.makedirs(tt.assets_path)
            if config:
                config.seek(0)
            with open(pathjoin(path, "config.ltc"), "wb+") as dest:
                if config:
                    dest.writelines(read_text_file(config))
            with open(
                pathjoin(TEMPLATES_VIEW_PATH, f"{tt}.html"), "wb+"
            ) as dest:
                if view:
                    for chunk in view.chunks():
                        dest.write(chunk)
            return tt
        except UnicodeDecodeError:
            if dbobj_created:
                tt.dbmodel.delete()
            return None

    @classmethod
    def delete(cls, id):
        this = cls.by_id(id)
        if os.path.isdir(this.dir_path):
            rmtree(this.dir_path)
        if os.path.isfile(this.view_path_absolute):
            os.remove(this.view_path_absolute)
        this.dbmodel.delete()

    @property
    def assets_path(self):
        return pathjoin(self.dir_path, "assets")

    @property
    def dir_path(self):
        return pathjoin(TASK_UPLOAD_PATH, str(self))

    @property
    def view_path(self):
        body = self.dbmodel.view_path or (str(self) + ".html")
        return pathjoin(TASK_VIEW_UPLOAD_PATH, body)

    @property
    def view_path_absolute(self):
        return pathjoin("core_app", "templates", self.view_path)

    @property
    def ltc_path(self):
        return self.dbmodel.config_path or pathjoin(
            TASK_UPLOAD_PATH, str(self), "config.ltc"
        )

    def write_ltc(self, text, check_errors=True):
        if check_errors:
            ltcc = LTCCompiler()
            try:
                ltc = ltcc.compile(text.splitlines())
                ltc.execute(metadata=LTCFakeMetadata())
            except (LTCCompileError, LTCError, LTCExecutionError) as e:
                raise TaskTemplateValidationFailed(str(e))
        with self.open_ltc(mode="w") as dest:
            dest.write(text.replace("\n", ""))

    def write_html(self, text, resettle=True):
        if resettle:
            os.remove(self.view_path_absolute)
            self.dbmodel.view_path = str(uuid4()) + ".html"
            self.dbmodel.save()

        with self.open_view(mode="w") as dest:
            dest.write(text.replace("\n", ""))

    def open_view(self, **kwargs):
        return open(self.view_path_absolute, encoding="UTF-8", **kwargs)

    def open_ltc(self, **kwargs):
        return open(self.ltc_path, encoding="UTF-8", **kwargs)

    def identificator(self):
        return slugify(
            f"ID{self.dbmodel.id}-{transliterate_ru_en(self.dbmodel.birthname)}"
        )

    def assets(self):
        try:
            return os.listdir(self.assets_path)
        except FileNotFoundError:
            os.makedirs(self.assets_path)
            return []

    def add_asset(self, name, file):
        file.seek(0)
        with open(pathjoin(self.assets_path, name), mode="wb+") as dump:
            for chunk in file.chunks():
                dump.write(chunk)
        return True

    def remove_asset(self, name):
        if name in self.assets():
            os.remove(pathjoin(self.assets_path, name))
            return True
        return False


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

    def set_field_overrides(self, overrides, mask=True, pick_first=False):
        cur = self.field_overrides
        if mask:
            overrides = {
                key: (value if not pick_first else value[0])
                for key, value in overrides.items()
                if key in cur
            }
        cur.update(overrides)
        self.dbmodel.field_overrides = json.dumps(cur)
        self.modified = True

    @property
    def field_overrides_items(self):
        return self.field_overrides.items()

    def solutions(self, group=NotSpecified):
        from .solutions import Solution

        if group is NotSpecified:
            return map(
                Solution, LateremSolution.objects.filter(task=self.dbmodel)
            )
        else:
            users = LateremUser.objects.filter(
                lateremgroupmembership__group=group.dbmodel
            )
            return map(
                Solution,
                LateremSolution.objects.filter(
                    task=self.dbmodel, user__in=users
                ),
            )

    def generate_metadata(self, user=NotSpecified):
        if user is NotSpecified:
            return LTCFakeMetadata()

        metadata = LTCMetadataManager()
        metadata.seed = self.id * 109231 ^ user.id * 2913884
        metadata.salt = self.id * 423 ^ user.id * 562
        metadata.xor = self.id * 3294829 ^ user.id * 6456484
        return metadata

    def compile(self, user=NotSpecified, answers=NotSpecified):
        if answers is NotSpecified:
            answers = {}
        else:
            answers = {
                key: (value if (len(value) - 1) else value[0])
                for key, value in answers.items()
            }
        with open(self.template.ltc_path, mode="r", encoding="UTF-8") as f:
            data = f.readlines()
        ltcc = LTCCompiler()
        ltc = ltcc.compile(data)
        extend_ns = self.field_overrides
        extend_ns.update(answers)
        metadata = self.generate_metadata(user)
        ltc.execute(extend_ns, metadata)
        view = self.view_path
        return CompiledTask(ltc, view)

    def update_exporting_fields(self):
        compiled = self.compile()
        exporting_fields = {
            key: (
                LTC_DEFAULT_EXPORT_VALUE
                if key not in compiled.ltc.namespace
                else compiled.ltc.namespace[key]
            )
            for key in compiled.ltc.exporting_fields
            if key not in self.field_overrides
        }
        self.set_field_overrides(exporting_fields, mask=False)

    def __str__(self):
        return self.dbmodel.name


class CompiledTask:
    def __init__(self, ltc, view) -> None:
        self.ltc = ltc
        self.template = view

    @classmethod
    def from_JSON(cls, data):
        d = json.loads(data)
        ltc = LTC.from_dict(d)
        template = d["template"]
        return cls(ltc, template)

    # def test(self, fields) -> int:
    #    fields = {key: (value if (len(value) - 1) else value[0])
    #              for key, value in fields.items()}
    #    return self.ltc.check(fields)

    def as_JSON(self):
        d = self.ltc.to_dict()
        d["template"] = self.template
        return json.dumps(d, indent=4)


class Work(DBHybrid):
    __dbmodel__ = LateremWork
    has_children = False
    json_type = "work"

    def __init__(self, dbobj):
        super().__init__(dbobj)

    def tasks(self):
        return sorted(
            [Task(x) for x in LateremTask.objects.filter(work=self.dbmodel)],
            key=lambda x: x.dbmodel.order,
        )

    def groups(self):
        from .groups import Group

        return [
            Group(x)
            for x in LateremGroup.objects.filter(
                lateremassignment__work=self.dbmodel
            )
        ]

    def get_answers(self, group=NotSpecified):
        ret = []
        for task in self.tasks():
            ret.extend(list(task.solutions(group=group)))
        return ret

    def is_valid(self):
        return not not self.tasks()

    def __hash__(self):
        return hash("WR" + str(self.id))

    def is_visible(self, user):
        if user.has_global_permission("can_manage_works"):
            return True
        return user.has_access(self)

    def add_task(self, name, task_type):
        if isinstance(task_type, str):
            if "-" in task_type:
                task_type = TaskTemplate.by_id(
                    int(task_type[len("ID") : task_type.find("-")])
                )
            else:
                task_type = TaskTemplate.by_id(int(task_type[len("ID") :]))

        last_order = LateremTask.objects.aggregate(Max("order"))["order__max"]
        last_order = last_order or 0

        task = Task(
            LateremTask.objects.create(
                name=name,
                task_type=task_type.dbmodel,
                work=self.dbmodel,
                order=last_order + 1,
            )
        )
        task.update_exporting_fields()
        task.close()
        task.dbmodel.save()
        return task

    def remove_task(self, task):
        task.dbmodel.delete()

    def reorder(self, task, new_order):
        tasks = self.tasks()
        tasks.remove(task)
        tasks.insert(new_order, task)
        for i, task in enumerate(tasks):
            task.dbmodel.order = i
            task.dbmodel.save()

    def __str__(self):
        return self.dbmodel.name


class Category(DBHybrid):
    __dbmodel__ = LateremCategory
    has_children = True
    json_type = "category"

    @staticmethod
    def roots():
        cat = [
            Category(x)
            for x in LateremCategory.objects.filter(root_category__isnull=True)
        ]
        wor = [
            Work(x) for x in LateremWork.objects.filter(category__isnull=True)
        ]
        return cat + wor

    def __hash__(self):
        return hash("CC" + str(self.id))

    def is_valid(self):
        return not not self.children()

    def is_visible(self, user):
        if user.has_global_permission("can_manage_works"):
            return True
        return any(map(lambda x: x.is_visible(user), self.children()))

    def categories(self):
        result = []
        for x in LateremCategory.objects.filter(root_category=self.dbmodel.id):
            cat = Category(x)
            result.append(cat)
        return result

    def works(self):
        result = []
        for x in LateremWork.objects.filter(category=self.dbmodel):
            work = Work(x)
            result.append(work)
        return result

    def children(self, *args, **kwargs):
        return self.categories(*args, **kwargs) + self.works(*args, **kwargs)

    def __str__(self):
        return self.dbmodel.name


class RootsMimic:
    __dbmodel__ = None
    has_children = True
    name = "mother"
    id = "mother"
    json_type = "category"

    def children(self, **kwargs):
        return Category.roots()


class WorkTreeView:
    def __init__(
        self,
        root,
        filter=NotSpecified,
        buffer=NotSpecified,
        node_mapper=NotSpecified,
        leaf_mapper=NotSpecified,
    ):
        if filter is NotSpecified:
            filter = lambda x: True
        if buffer is NotSpecified:
            buffer = {}
        if node_mapper is NotSpecified:
            node_mapper = {}
        if leaf_mapper is NotSpecified:
            leaf_mapper = {}

        self.root = root
        self.filter = filter
        self.buffer = buffer

        self.node_mapper = node_mapper
        self.leaf_mapper = leaf_mapper

    def children(self):
        for child in self.root.children():
            if child in self.buffer:
                flag = self.buffer[child]
            else:
                flag = self.filter(child)
            if flag:
                yield WorkTreeView(
                    child,
                    filter=self.filter,
                    buffer=self.buffer,
                    node_mapper=self.node_mapper,
                    leaf_mapper=self.leaf_mapper,
                )

    def jsonize(self):
        obj = {
            "name": self.root.name,
            "type": self.root.json_type,
            "id": self.root.id,
        }
        if self.root.has_children:
            # Node
            obj["children"] = []
            for child in self.children():
                obj["children"].append(child.jsonize())
            for name, func in self.node_mapper.items():
                obj[name] = func(self.root)
        else:
            # Leaf
            for name, func in self.leaf_mapper.items():
                obj[name] = func(self.root)
        return obj

    @staticmethod
    def user_access_filter(user, ensure_validation=True):
        if ensure_validation:
            return lambda x: x.is_visible(user) and x.is_valid()
        return lambda x: x.is_visible(user)
