from django.http import HttpResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from dbapi.bug_reports import BugReport

from os.path import join as pathjoin

from context_objects import BUGREPORT_UPLOAD_PATH

@login_required
def bug_report_asset(request, br_id, filename):
    if request.user.email.lower() != "admin@admin.admin":
        raise PermissionDenied
    path = pathjoin(BUGREPORT_UPLOAD_PATH, br_id, filename)
    try:
        return FileResponse(open(path, "rb"))
    except FileNotFoundError:
        raise Http404('Asset not found')


@login_required
def bug_reports(request):
    if request.user.email.lower() != "admin@admin.admin":
        raise PermissionDenied
    content = ''
    for bugrep in BugReport.all_open_reports():
        content += str(bugrep)
    return HttpResponse(content)
