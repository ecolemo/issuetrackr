from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.core.context_processors import csrf
from django.shortcuts import redirect
from djangobp.route import render_to_response, render_to_json
from issue.models import Issue, Tag, IssueHistory, Comment
from django.core.exceptions import ObjectDoesNotExist

import re
def strip_tags(text):
    return re.sub('<[^>]+>', '', text)

def index(request, resource_id):
    objects = Issue.objects.order_by('-updated')

    class IndexFeed(Feed):
        title = "IssueTrac.kr site index"
        link = "/issue/"
        description = "Recent Issues"
        def items(self): return objects
        def item_title(self, item): return item.title
        def item_description(self, item): return item.content
        def item_link(self, item): return '/issues/' + str(item.id)

    if 'tag' in request.GET:
        for tag in request.GET.getlist('tag'):
            objects = objects.filter(tags__name=tag)
    if request.format == 'xml': return IndexFeed()(request)
    else: return render_to_response('issues/index.html', locals())

@login_required
def new(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    return render_to_response('issues/new.html', locals())

@login_required
def create(request, resource_id):
    issue = request.user.issue_set.create(title=request.POST['title'], content=request.POST['content'], updated=datetime.now())
    issue.save_history()
    issue.update_tags(request.POST['tags'])

    return redirect('/issues/%d' % issue.id)

def show(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    issue = Issue.objects.get(id=resource_id)
    issue.read_count += 1
    issue.save()

    class ShowFeed(Feed):
        title = "IssueTrac.kr issue"
        link = "/issue/"
        description = "Recent Issues"
        def get_object(self, request, resource_id): return issue
        def items(self): return Comment.objects.filter(issue=issue)
        def item_title(self, item): return "comment : " + strip_tags(item.content)[:50]
        def item_description(self, item): return item.content
        def item_link(self, item): return '/issues/%d#c-%d' % (issue.id, item.id)

    if request.user.is_anonymous():
        user_vote = None
    else:
        try:
            user_vote = issue.vote_set.get(voter=request.user)
        except ObjectDoesNotExist:
            user_vote = None

    if request.format == 'xml': return ShowFeed()(request, resource_id)
    else: return render_to_response('issues/show.html', locals())

@login_required
def edit(request, resource_id):
    csrf_token = csrf(request)['csrf_token']
    issue = Issue.objects.get(id=resource_id)
    return render_to_response('issues/edit.html', locals())

@login_required
def update(request, resource_id):
    issue = Issue.objects.get(id=resource_id)
    issue.title = request.POST['title']
    issue.content=request.POST['content']
    issue.save()

    issue.update_tags(request.POST['tags'])

    issue.save_history()

    return redirect('/issues/%d' % issue.id)

def destroy(request, resource_id):
    issue = Issue.objects.get(id=resource_id)
    issue.delete()
    return redirect('/issues/')


def histories(request, resource_id):
    issue = Issue.objects.get(id=resource_id)
    return render_to_response('issues/histories.html', locals())

def history(request, resource_id):
    history = IssueHistory.objects.get(id=resource_id)
    return render_to_response('issues/history.html', locals())

@login_required
def restore(request, resource_id):
    history = IssueHistory.objects.get(id=resource_id)
    history.restore()
    return redirect('/issues/%d' % history.target.id)
