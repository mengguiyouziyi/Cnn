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
import json
import scrapy
from redis import StrictRedis
from scrapy.spiders import Spider
from cnn_scrapy.items import CnnItem
from scrapy.exceptions import CloseSpider


class MeishijieSpider(Spider):
    name = 'cnn_uncrawl'
    allowed_domains = ['cnn.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'origin': "http://edition.cnn.com",
            'referer': "http://edition.cnn.com/search/?size=10&q=technology&from=30&page=4",
            'cache-control': "no-cache",
        },
        'DOWNLOAD_DELAY': 2
    }

    def __init__(self):
        self.server = StrictRedis(host=self.settings.get('REDIS_HOST'), decode_responses=True)

    def start_requests(self):
        while True:
            url = self.server.spop('cnn_uncrawl:myrequests')
            if not url:
                raise CloseSpider('no datas')
            yield scrapy.Request(url)

    def parse(self, response):
        obj = json.loads(response.body_as_unicode())
        results = obj.get('result', [])
        for result in results:
            if result.get('type', '') != 'article':
                continue
            item = CnnItem()
            url = result.get('url', '')
            if self.server.sismember('cnn_uncrawl:myitem', url):
                continue
            self.server.sadd('cnn_uncrawl:myitem', url)
            if 'technology' in url:
                item['cat'] = 'technology'
            elif 'politics' in url:
                item['cat'] = 'politics'
            elif 'us' in url:
                item['cat'] = 'us'
            else:
                continue
            item['url'] = url
            item['title'] = result.get('headline', '')
            item['author'] = result.get('byLine', '')
            item['update_time'] = result.get('firstPublishDate', '')
            item['pic'] = result.get('thumbnail', '')
            item['keyword'] = ','.join(result.get('topics', []))
            item['text'] = result.get('body', '')
            yield item
