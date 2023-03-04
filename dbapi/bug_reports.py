from core_app.models import LateremBugReport
from commons import DBHybrid, NotSpecified
from context_objects import BUGREPORT_UPLOAD_PATH

from os.path import join as pathjoin
from os import makedirs

class BugReport(DBHybrid):
    __dbmodel__ = LateremBugReport

    @classmethod
    def new_report(cls, user, text, files):
        new = cls.__dbmodel__.objects.create(user=user.dbmodel, 
                                             text=text)
        p = pathjoin(BUGREPORT_UPLOAD_PATH, str(new.id))
        makedirs(p)
        #for i, file in enumerate(files):
        with open(pathjoin(p, f"{1}.png"), "wb+") as dest:
            for chunk in files.chunks():
                dest.write(chunk)
