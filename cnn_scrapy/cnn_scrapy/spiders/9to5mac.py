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
    name = '9to5mac'
    allowed_domains = ['9to5mac.com']

    def start_requests(self):
        url = 'https://9to5mac.com/'
        yield scrapy.Request(url)

    rules = (
        Rule(LinkExtractor(allow=('/(technology|politics)'), deny=('index\.html', 'videos', 'fortune', 'interactive'))),
        Rule(LinkExtractor(
            allow=('(\d{4}-\d{2}-\d{2}/)?(technology|politics)/(\d{4}-\d{2}-\d{2}/)?[-\w]+/index\.html$'), deny=('videos', 'fortune', 'interactive')),
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
