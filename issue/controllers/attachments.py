from issue.models import Attachment
from django.http import HttpResponse
def create(request, resource_id):
    f = request.FILES['upload']
    attachment = Attachment.objects.create(issue=resource_id, writer=request.user, filename=f.name)
    return HttpResponse(attachment.url())