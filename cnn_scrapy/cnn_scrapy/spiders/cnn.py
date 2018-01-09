# encoding:utf-8
import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from cnn_scrapy.items import CnnItem


class MeishijieSpider(CrawlSpider):
    name = 'cnn'
    allowed_domains = ['cnn.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'host': "www.cnn.com",
            'connection': "keep-alive",
            'cache-control': "no-cache",
            'upgrade-insecure-requests': "1",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'referer': "http://www.cnn.com/politics",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            # 'cookie': "THEOplayer.textTrackStyle.fontFamily=; THEOplayer.textTrackStyle.fontColor=rgba(255, 255, 255, 1); THEOplayer.textTrackStyle.fontSize=1em; THEOplayer.textTrackStyle.backgroundColor=rgba(0, 0, 0, 0.75); THEOplayer.textTrackStyle.windowColor=rgba(0, 0, 0, 0); THEOplayer.textTrackStyle.edgeStyle=uniform; volume=1; theoplayer-session-id=204e8184-3088-4fc4-80d9-014001888848; metric_enabled=true; metric_downloadBytes=2197784; metric_downloadTime=0.1903000000000361; metric_latency=0.12069899999999052; countryCode=US; geoData=herndon|VA|20170|US|NA; tryThing00=6858; optimizelyEndUserId=oeu1515396174699r0.121411241465331; s_cc=true; s_fid=7799CA5E1940F980-3DF443F2BCF72DE3; __qca=P0-450045770-1515396176267; s_vi=[CS]v1|2D298E28051D217F-400019078000A33C[CE]; __gads=ID=5d791ed372f4e61b:T=1515396179:S=ALNI_MaGgJyZkjkSDSgfAQuKLS2BqfOkzA; gig_hasGmid=ver2; s_ppv=100; optimizelyBuckets=%7B%7D; IPE_S_104983=104983; __vrf=1515410903819BJBuITbGHxjdDrGqXNdSqH82zADtP4QB; optimizelySegments=%7B%22173979470%22%3A%22referral%22%2C%22175262621%22%3A%22gc%22%2C%22175404620%22%3A%22false%22%2C%22175460039%22%3A%22none%22%7D; WSOD%5FcompareToSP500=0; WSOD%5FcompareToCategory=0; __unam=7549672-160d4ab9df2-555ea13f-8; WSOD%5FxrefSymbol=ROKU; _cb_ls=1; bounceClientVisit340v=N4IgNgDiBcIBYBcEQKQGYCCKBMAxHuA7sQHQDGAdheQPYC2BIANCAE4wh00UCmAnuSq06IAL5A; _t_tests={\"[e689addd]\":{\"chosenVariant\":\"B\",\"specificLocation\":[\"*[@id='homepage1-zone-1']/div[2]/div[1]/div[3]/ul[1]/article[5]/div[1]/div[1]/h3[1]/a[1][@href='http://www.cnn.com/videos/world/2018/01/08/china-oil-tanker-freighter-collision-rivers-nr.cnn']\"]},\"[67119b0e]\":{\"chosenVariant\":\"B\",\"specificLocation\":[\"*[@id='homepage1-zone-1']/div[2]/div[1]/div[3]/ul[1]/article[2]/div[1]/div[1]/h3[1]/a[1][@href='http://www.cnn.com/2018/01/07/politics/donald-trump-schedule/index.html']\"]},\"lift_exp\":\"m\"}; ug=5a531c4f0aaa020a3c21445e53045aa3; ugs=1; _cb=Dkpa7gBpzNapq0siR; _cb_svref=http%3A%2F%2Fmoney.cnn.com%2F2018%2F01%2F05%2Ftechnology%2Falexa-headphones-smartwatches%2Findex.html; s_sq=%5B%5BB%5D%5D; hpt=cGFnZV8xNGNvbF9wb2xpdGljc19zZWN0aW9uIGZyb250X3pvbmUtMC0xX1RvcCBuZXdzIGFuZCB0ZXRyaXNfY24tLWV4cGFuZGFibGVfVG9wLVN0b3JpZXM=; hpt2=cGFnZV8xNGNvbF9wb2xpdGljc19zZWN0aW9uIGZyb250X3pvbmUtMC0xX3ByaW9yaXR5KzJfY24tLWV4cGFuZGFibGVfbGlzdDpoZWFkbGluZXMraW1hZ2Vz; _uetsid=_uet7d7e2789; session_depth=www.cnn.com%3D1%7C505661222%3D1; _chartbeat2=.1515410937879.1515411725229.1.DyjSoX391EIDJbCtCBYVgcuBZaPor; GED_PLAYLIST_ACTIVITY=W3sidSI6IkpFc2YiLCJ0c2wiOjE1MTU0MTIwODUsIm52IjoxLCJ1cHQiOjE1MTU0MTIwNzcsImx0IjoxNTE1NDEyMDg0fV0.",
        },
        'DOWNLOAD_DELAY': 1
    }

    def start_requests(self):
        url = 'http://www.cnn.com/'
        yield scrapy.Request(url)

    rules = (
        Rule(LinkExtractor(allow=('technology|politics'))),
        Rule(LinkExtractor(
            allow=('(technology|politics).*index\.html$'), deny=('videos', 'fortune', 'interactive')),
            callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if 'It could be you, or it could be us' in response.text:
            return
        s = Selector(text=response.text)
        title = s.xpath('//h1/text()').extract_first()
        t = s.xpath('//title/text()').extract_first()
        date = s.xpath('//meta[@name="date"]/@content').extract_first()
        d = s.xpath('//p[@class="update-time"]/text()|//span[@class="cnnDateStamp"]/text()').extract_first()

        keyword = s.xpath('//meta[@name="news_keywords"]/@content|//meta[@name="keywords"]/@content').extract_first()
        author = s.xpath('//meta[@name="author"]/@content').extract_first()
        a = s.xpath('//span[@class="metadata__byline__author"]//text()|//span[@class="byline"]//text()').extract()
        a = ''.join(a).replace('By', '').strip() if a else ''
        cat = s.xpath('//meta[@name="section"]/@content').extract_first()
        c = 'technology' if 'technology' in response.url else 'politics'
        p = s.xpath(
            '//div[@class="slideimg"]/img/@src|//img[@class="media__image"]/@src|//figure[contains(@class, "body_img")]/img/@src|//div[@class="l-container"]//img/@src').extract_first()
        pic = s.xpath('//img/@src').extract_first()
        p = p if p else pic
        p = ('http:' + p) if p and ('http:' not in p) else ''
        # keyword = s.xpath(
        #     '//div[@class="zn-body__paragraph"]//text()|//h2[@class="speakable"]/text()|//div[@id="storytext"]//text()').extract_first()
        text = s.xpath(
            '//div[contains(@class, "zn-body__paragraph")]//text()|//div[@id="storytext"]/p/text()|//div[@id="storytext"]/h2/text()|//div[@id="storytext"]/*[@class="speakable"]/text()').extract()
        # keyword = text[0] if text else ''
        text = '\n'.join(text) if text else ''

        item = CnnItem()
        item['url'] = response.url
        item['title'] = title if title else t
        item['author'] = author if author else a
        item['update_time'] = date if date else d
        item['cat'] = cat if cat else c
        item['pic'] = p
        item['keyword'] = keyword
        item['text'] = text

        yield item
