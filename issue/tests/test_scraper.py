# coding: utf8
import unittest
import urllib2
from issue.scraper.scraper import Scraper, RetrieveDataError

class ScraperTest(unittest.TestCase):
    def testParsingError(self):
        url = "http://test.co.kr"
        def loadHtml(self,url):
            with open('parse_error.html') as f: return f.read()

        Scraper.loadHtml = loadHtml

        scraper = Scraper(url).load()
        self.assertEquals ("no title", scraper.title)
        thumbnailImages = scraper.makeThumbnails(scraper.extractImageUrls(scraper.soup, scraper.siteUrl))
        self.assertEquals([], thumbnailImages)



    def testEtomato(self):
        url = "http://news.etomato.com/Home/ReadNews.aspx?no=201886"
        scraper = Scraper(url)
        def loadHtml(url):
            with open('news_etomato.html') as f: return f.read()
        scraper.loadHtml = loadHtml
            
        self.assertEquals (url, scraper.url)
        self.assertEquals ('http://news.etomato.com', scraper.siteUrl)

        scraper.load()
        expectedTitle = u'경제전문 멀티미디어 뉴스 - 뉴스 토마토 -'
        self.assertEquals (expectedTitle, scraper.title)

        thumbnailImages = scraper.makeThumbnails(scraper.extractImageUrls(scraper.soup, scraper.siteUrl))
        self.assertTrue (thumbnailImages is not None)

    def testMediatoday(self):
        url = "http://www.mediatoday.co.kr/news/articleView.html?idxno=98608"
        scraper = Scraper(url)
        def loadHtml(url):
            with open('mediatoday.html') as f: return f.read()
        scraper.loadHtml = loadHtml

        self.assertEquals (url, scraper.url)
        self.assertEquals ('http://www.mediatoday.co.kr', scraper.siteUrl)

        scraper.load()
        expectedTitle = u'미디어오늘 : "강용석 의원님, 우리는 닥치고 개그나 할게요"'
        self.assertEquals (expectedTitle, scraper.title)

    def testLoadWithWrongURL(self):
        url = "http://wrongwuhaha.com/"
        scraper = Scraper(url)
        def loadHtml(url):
            raise urllib2.URLError('no site')
        scraper.loadHtml = loadHtml
        try:
            scraper.load()
            self.fail("no exception")
        except RetrieveDataError, e:
            pass

if __name__=="__main__":
    unittest.main(argv=('','-v'))