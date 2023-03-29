from core_app.models import LateremBugReport
from commons import DBHybrid, NotSpecified
from context_objects import BUGREPORT_UPLOAD_PATH

from os.path import join as pathjoin
from os import makedirs
from os import listdir


class BugReport(DBHybrid):
    __dbmodel__ = LateremBugReport

    @classmethod
    def new_report(cls, user, text, files):
        new = cls.__dbmodel__.objects.create(
            user=user.dbmodel if user else None, text=text
        )
        p = pathjoin(BUGREPORT_UPLOAD_PATH, str(new.id))
        makedirs(p)
        if files:
            # for i, file in enumerate(files):
            with open(pathjoin(p, f"{1}.png"), "wb+") as dest:
                for chunk in files.chunks():
                    dest.write(chunk)

    @classmethod
    def all_open_reports(cls):
        return [cls(x) for x in LateremBugReport.objects.filter(closed=False)]

    def __str__(self):
        content = f"<h1>{self.id}: {self.user.email if self.user else 'Anonymous User'}</h1>"
        content += f"<h2>{self.text}</h2>"
        for filename in listdir(pathjoin(BUGREPORT_UPLOAD_PATH, str(self.id))):
            content += f'<br><img width="500px" src="/developermode/getasset/{self.id}/{filename}">'
        return content
