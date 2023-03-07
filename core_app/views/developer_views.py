from core_app.views.views_commons import *

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
