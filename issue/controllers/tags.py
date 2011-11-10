from issue.models import Tag
from djangobp.route import render_to_response
def index(request, resource_id):
    tags = Tag.objects.all()
    return render_to_response('tags/index.html', locals())