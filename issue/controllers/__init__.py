from django.http import HttpResponseRedirect
from django.contrib.syndication.views import Feed
from issue.models import Issue

def index(request):
    return HttpResponseRedirect('/issues')

class IndexFeed(Feed):
    title = "IssueTrac.kr site index"
    link = "/issue/"
    description = "Recent Issues"
    def items(self):
        objects = Issue.objects.order_by('-updated')
        return objects

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return ""

    def item_link(self, item):
        return '/issues/' + str(item.id)
