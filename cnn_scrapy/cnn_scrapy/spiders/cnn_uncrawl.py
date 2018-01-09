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
    name = 'cnn_uncrawl'
    allowed_domains = ['cnn.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'origin': "http://edition.cnn.com",
            'referer': "http://edition.cnn.com/search/?size=10&q=technology&from=30&page=4",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
            'cache-control': "no-cache",
            'postman-token': "4d85af38-befa-3602-b49e-32bf9f803900"
        },
        'DOWNLOAD_DELAY': 1
    }
    start_urls = ['http://edition.cnn.com/search/?size=10&q=technology', 'http://www.cnn.com/']

    rules = (
        Rule(LinkExtractor(allow=(
        'technology|politics|us', '/search/\?size=\d+\&q=(technology|politics|us|china)\&from=\d+\&page=\d+'))),
        Rule(LinkExtractor(
            allow=('(technology|politics|us).*index\.html$'), deny=('videos', 'fortune', 'interactive')),
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
