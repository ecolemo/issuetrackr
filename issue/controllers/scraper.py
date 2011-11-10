# coding:utf8
import simplejson
from django.http import HttpResponse
import urllib2
from BeautifulSoup import BeautifulSoup
from urllib import urlretrieve
import Image
import os
from djangobp.route import render_to_response

class HttpResponseJSON(HttpResponse):
    def __init__(self, data):
        HttpResponse.__init__(self, simplejson.dumps(data, ensure_ascii=False), content_type='application/json')

def index(request, resource_id):
    return render_to_response('scraper/index.html', locals())

def scrap(request, resource_id):
    url = request.GET['url']

    title, imageUrls = scrapping(url)
    thumbnailImages = makeThumbnails(imageUrls)

    data = {
        'title':title,
        'images':thumbnailImages
    }

    return HttpResponseJSON(data)

def image(request, resource_id):
    imageUrl = request.GET['url']
    fileName = "./tmp_scraper/" + imageUrl.replace('/','_')
    extension = os.path.splitext(fileName)[1][1:]
    response = HttpResponse(mimetype='image/%s' % (extension))
    f=open(fileName)
    response.write(f.read())
    f.close()

    return response

def scrapping(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup.title.text, set([img['src'] for img in soup('img')])

def makeThumbnails(imageUrls):
    thumbnailCandidates = []
    for imageUrl in imageUrls:
        fileName = imageUrl.replace('/','_')
        urlretrieve(imageUrl, './tmp_scraper/' + fileName)
        size = imageSize(fileName)
        thumbnailCandidates.append({'url':imageUrl, 'fileName': fileName, 'width' : size[0], 'height':size[1]})

    top3 = sorted(thumbnailCandidates, imageCompare)[:3]
    for e in top3: makeThumbnailImage(e)
    return top3

def makeThumbnailImage(imageInfo):
    fileName = imageInfo['fileName']
    image = Image.open('./tmp_scraper/' + fileName)
    THUMBNAIL_MAX_WIDTH = 120

    newWidth = int(min(THUMBNAIL_MAX_WIDTH, imageInfo['width']))
    newHeight = int(imageInfo['height'] / float(imageInfo['width']) * newWidth + 0.5)
    resizedImage = image.resize((newWidth,newHeight))

    # overwrite
    resizedImage.save(fileName)
    imageInfo['width'] = newWidth
    imageInfo['height'] = newHeight

def imageSize(fileName):
    return Image.open('./tmp_scraper/' + fileName).size

def imageCompare(fileOne, fileTwo):
    areaOne = fileOne['width'] * fileOne['height']
    areaTwo = fileTwo['width'] * fileTwo['height']
    return areaTwo - areaOne
