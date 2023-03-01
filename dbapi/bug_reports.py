from core_app.models import LateremBugReport
from commons import DBHybrid, NotSpecified
from context_objects import BUGREPORT_UPLOAD_PATH

from os.path import join as pathjoin

class BugReport(DBHybrid):
    __dbmodel__ = LateremBugReport

    @classmethod
    def new_report(cls, user, text, files):
        new = cls.__dbmodel__.objects.create(user=user.dbmodel, 
                                             text=text)
        for i, file in enumerate(files):
            with open(pathjoin(BUGREPORT_UPLOAD_PATH, str(new.id), f"{i}.png"), "wb+") as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
