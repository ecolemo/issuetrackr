from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import redirect
from djangobp.makohelper import render_to_response
from issue.models import Issue, Tag

def index(request, resource_id):
    objects = Issue.objects.order_by('-updated')
    if 'tag' in request.GET and Tag.objects.filter(name=request.GET['tag']).exists():
        objects = objects.filter(tags__name=request.GET['tag'])
    return render_to_response('issues/index.html', locals())

@login_required
def new(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    return render_to_response('issues/new.html', locals())

@login_required
def create(request, resource_id):
    issue = request.user.issue_set.create(title=request.POST['title'], content=request.POST['content'])
    tags = request.POST['tags'].split(',')
    for tag in tags:
        issue.tags.add(Tag.objects.get_or_create(name=tag.strip())[0])

    return redirect('/issues/%d' % issue.id)

def show(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    issue = Issue.objects.get(id=resource_id)
    return render_to_response('issues/show.html', locals())

def edit(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    issue = Issue.objects.get(id=resource_id)
    return render_to_response('issues/edit.html', locals())

def update(request, resource_id):
    issue = Issue.objects.get(id=resource_id)
    issue.title = request.POST['title']
    issue.content=request.POST['content']
    issue.save()

    issue.tags.all().delete()
    tags = request.POST['tags'].split(',')
    for tag in tags:
        issue.tags.add(Tag.objects.get_or_create(name=tag.strip())[0])

    return redirect('/issues/%d' % issue.id)

def destroy(request, resource_id):
    issue = Issue.objects.get(id=resource_id)
    issue.delete()
    return redirect('/issues/')
    