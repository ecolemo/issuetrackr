import os
from urllib import urlretrieve
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup
import Image

tempfile_storage_path = os.environ['HOME'] + '/issuetrackr_files/tmp_scraper/'

class RetrieveDataError(Exception):
    def __str__(self):
        return "Exception at retrieving html"

class Scraper:
    def __init__(self, url):
        self.url = url
        self.siteUrl = self.extractSiteUrl()

    def extractSiteUrl(self):
        o = urlparse.urlparse(self.url)
        return o.scheme + '://' + o.hostname

    def load(self):
        self.soup = self.loadHtmlAndMakeSoup(self.url)
        try:
            self.title = self.soup.title.text
        except AttributeError:
            self.title = 'no title'
        return self

    def loadHtml(self,url):
        return urllib2.urlopen(url).read()

    def loadHtmlAndMakeSoup(self,url):
        try:
            return BeautifulSoup(self.loadHtml(url))
        except urllib2.URLError:
            raise RetrieveDataError()

    def thumbnailImages(self):
        return self.makeThumbnails(self.extractImageUrls(self.soup, self.siteUrl))

    def extractImageUrls(self, soup, siteUrl):
        imageUrls = []
        for img in soup('img'):
            try:
                imageUrls.append(img['src'])
            except Exception as e: # wrong img tag problem
                pass

        result = []
        for e in set(imageUrls):
            if not e.startswith('http://') and not e.startswith('https://'):
                result.append(urlparse.urljoin(siteUrl,e))
            else:
                result.append(e)

        return result

    def makeThumbnails(self, imageUrls):
        thumbnailCandidates = []
        for imageUrl in imageUrls:
            try:
                fileName = imageUrl.replace('/','_')
                urlretrieve(imageUrl, tempfile_storage_path + fileName)
                size = self.imageSize(fileName)
                thumbnailCandidates.append({'url':imageUrl, 'fileName': fileName, 'width' : size[0], 'height':size[1]})
            except IOError: # bad image or unknown image format
                pass

        top3 = sorted(thumbnailCandidates, self.imageCompare)[:3]
        for e in top3: self.makeThumbnailImage(e)
        return top3

    def makeThumbnailImage(self, imageInfo):
        fileName = imageInfo['fileName']
        fullFilePath = tempfile_storage_path + fileName
        image = Image.open(fullFilePath)
        format = image.format
        THUMBNAIL_MAX_WIDTH = 120

        newWidth = int(min(THUMBNAIL_MAX_WIDTH, imageInfo['width']))
        newHeight = int(imageInfo['height'] / float(imageInfo['width']) * newWidth + 0.5)
        resizedImage = image.resize((newWidth,newHeight))

        # overwrite
        resizedImage.save(fullFilePath, format)
        imageInfo['width'] = newWidth
        imageInfo['height'] = newHeight

    def imageSize(self, fileName):
        return Image.open(tempfile_storage_path + fileName).size

    def imageCompare(self, fileOne, fileTwo):
        areaOne = fileOne['width'] * fileOne['height']
        areaTwo = fileTwo['width'] * fileTwo['height']
        return areaTwo - areaOne

