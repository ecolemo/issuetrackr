from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import redirect
from djangobp.route import render_to_response
from issue.models import Issue


@login_required
def create(request, resource_id):
    issue = Issue.objects.get(id=request.POST['issue'])
    issue.comment_set.create(writer=request.user, content=request.POST['content'])
    issue.save()
    return redirect('/issues/%d' % issue.id)

@login_required
def edit(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    issue = Issue.objects.get(id=resource_id)
    return render_to_response('issues/edit.html', locals())

@login_required
def update(request, resource_id):
    issue = Issue.objects.get(id=resource_id)
    issue.update(title=request.POST['title'], content=request.POST['content'])
    return redirect('/issues/%d' % issue.id)

@login_required
def destroy(request, resource_id):
    issue = Issue.objects.get(id=resource_id)
    issue.delete()
    return redirect('/issues/')
    