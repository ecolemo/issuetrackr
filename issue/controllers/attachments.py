from issue.models import Attachment, Issue
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create(request, resource_id):
    f = request.FILES['upload']
    attachment = Attachment.objects.create(issue=Issue.objects.all()[0], writer=request.user, filename=f.name)
    return HttpResponse(attachment.url())