from issue.models import Attachment, Issue
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import http_date
import time
import mimetypes

@csrf_exempt
def create(request, resource_id):
    f = request.FILES['upload']
    attachment = Attachment.objects.create(issue=Issue.objects.all()[0], writer=request.user, filename=f.name, size=f.size)
    attachment.save_file(f)
    
    return HttpResponse(attachment.url)

def show(request, resource_id):
    attachment = Attachment.objects.get(id=resource_id)
    mimetype = mimetypes.guess_type(attachment.filename)

    response = HttpResponse(attachment.file_object.read(), mimetype)
    response["Last-Modified"] = http_date(time.mktime(attachment.created.timetuple()))
    response["Content-Length"] = attachment.size
    return response