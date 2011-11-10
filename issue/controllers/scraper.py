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

tempfile_storage_path = os.environ['HOME'] + '/issuetrackr_files/tmp_scraper/'

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
    fileName = tempfile_storage_path + imageUrl.replace('/','_')
    extension = os.path.splitext(fileName)[1][1:]
    response = HttpResponse(mimetype='image/%s' % (extension))
    f=open(fileName)
    response.write(f.read())
    f.close()

    return response

def extractSiteUrl(url):
    import re
    return re.search("(?P<url>https?://[^\s]+)/?", url).group("url")

def extractImageUrls(url, soup):
    siteUrl = extractSiteUrl(url)

    imageUrls = set([img['src'] for img in soup('img')])
    result = []
    for e in imageUrls:
        if not e.startswith('http://') and not e.startswith('https://'):
            result.append(siteUrl + e)
        else:
            result.append(e)

    return result

def scrapping(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    title = soup.title.text
    imageUrls = extractImageUrls(url, soup)
    return title, imageUrls

def makeThumbnails(imageUrls):
    thumbnailCandidates = []
    for imageUrl in imageUrls:
        fileName = imageUrl.replace('/','_')
        urlretrieve(imageUrl, tempfile_storage_path + fileName)
        size = imageSize(fileName)
        thumbnailCandidates.append({'url':imageUrl, 'fileName': fileName, 'width' : size[0], 'height':size[1]})

    top3 = sorted(thumbnailCandidates, imageCompare)[:3]
    for e in top3: makeThumbnailImage(e)
    return top3

def makeThumbnailImage(imageInfo):
    fileName = imageInfo['fileName']
    fullFilePath = tempfile_storage_path + fileName
    image = Image.open(fullFilePath)
    THUMBNAIL_MAX_WIDTH = 120

    newWidth = int(min(THUMBNAIL_MAX_WIDTH, imageInfo['width']))
    newHeight = int(imageInfo['height'] / float(imageInfo['width']) * newWidth + 0.5)
    resizedImage = image.resize((newWidth,newHeight))

    # overwrite
    resizedImage.save(fullFilePath)
    imageInfo['width'] = newWidth
    imageInfo['height'] = newHeight

def imageSize(fileName):
    return Image.open(tempfile_storage_path + fileName).size

def imageCompare(fileOne, fileTwo):
    areaOne = fileOne['width'] * fileOne['height']
    areaTwo = fileTwo['width'] * fileTwo['height']
    return areaTwo - areaOne
