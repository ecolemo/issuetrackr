# coding:utf8
import os
from django.http import HttpResponse
from djangobp.route import render_to_response, render_to_json
from issue.scraper.scraper import Scraper

tempfile_storage_path = os.environ['HOME'] + '/issuetrackr_files/tmp_scraper/'

def index(request, resource_id):
    return render_to_response('scraper/index.html', locals())

def scrap(request, resource_id):
    url = request.GET['url']

    try:
        scraper = Scraper(url).load()

        data = {
            'status':'ok',
            'title':scraper.title,
            'images':scraper.thumbnailImages(),
            'url':url,
            'site_url':scraper.siteUrl,
        }
    except Exception as e:
        print 'controller.scraper:', e
        data = {
            'status':'error'
        }
        
    return render_to_json(data)

def image(request, resource_id):
    imageUrl = request.GET['url']
    fileName = tempfile_storage_path + imageUrl.replace('/','_')
    extension = os.path.splitext(fileName)[1][1:]
    response = HttpResponse(mimetype='image/%s' % (extension))
    with open(fileName) as f: response.write(f.read())
    return response
