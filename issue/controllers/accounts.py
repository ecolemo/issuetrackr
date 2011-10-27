from djangobp.makohelper import render_to_response
from social_auth.context_processors import social_auth_by_type_backends
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

def login(request, object_id):
    csrf_token = csrf(request)['csrf_token']
    reverse_url = reverse
    l = locals()
    l.update(social_auth_by_type_backends(request))
    return render_to_response('login.html', l)

def logout(request, object_id):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/issues')

@login_required
def show(request, object_id):
    csrf_token = csrf(request)['csrf_token']
    return render_to_response('accounts/show.html', locals())

@login_required
def update(request, object_id):
    request.user.username = request.POST['username']
    request.user.save()
    return HttpResponseRedirect('/accounts/%d/show' % request.user.id)
