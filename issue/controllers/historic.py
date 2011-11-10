# coding:utf8
import simplejson
import urllib2
import urllib
from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
from djangobp.route import render_to_response

class HttpResponseJSON(HttpResponse):
    def __init__(self, data):
        HttpResponse.__init__(self, simplejson.dumps(data, ensure_ascii=False), content_type='application/json')

def index(request, resource_id):
    return render_to_response('historic/index.html', locals())

import re
def strip_tags(text):
    return re.sub('<[^>]+>', '', text)

def scrap(request, resource_id):
    keyword = request.GET['keyword']

    reqStr = u'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8'
    referer = u'http://issuetrac.kr/'
    googleApiKey = u"ABQIAAAAAr4MSzqu68JO_IAhdAmTPxQhRzS6oMlTs9O9b-4VnBCnWbncyxSsr378Ohb5DbzTf_Ug0js0jgwmng"
    req = urllib2.Request(reqStr+'&'+urllib.urlencode({'q':keyword.encode('utf8'), 'key':googleApiKey}))

    req.add_header('Referer', referer)
    text = urllib2.urlopen(req).read()
    searchResults = simplejson.loads(text)['responseData']['results']
    results = [{'title' : e['title'],
               'url' : e['url'],
               'site_url' : e['visibleUrl'],
               'summary' : strip_tags(e['content'])
               } for e in searchResults]

    return HttpResponseJSON(results)

def addToHistory(request, resource_id):
    title = request.POST['title']
    url  = request.POST['url']
    site_url = request.POST['site_url']
    summary = request.POST['summary']
    results = [{'title' : title,
               'url' : url,
               'site_url' : site_url,
               'summary' : summary}]
    
    return HttpResponseJSON(results)