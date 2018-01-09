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
import json
import codecs
from scrapy.spiders import Spider
from cnn_scrapy.items import CnnItem


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
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
            'cache-control': "no-cache",
            'postman-token': "4d85af38-befa-3602-b49e-32bf9f803900"
        },
        'DOWNLOAD_DELAY': 1
    }

    def start_requests(self):
        tech = ['https://search.api.cnn.io/content?size=100&q=technology&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
                for i in range(1, 300)]
        for url in tech:
            yield scrapy.Request(url)
        poli = ['https://search.api.cnn.io/content?size=100&q=politics&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
                for i in range(1, 781)]
        for url in poli:
            yield scrapy.Request(url)
        us = ['https://search.api.cnn.io/content?size=100&q=us&from={f}&page={p}'.format(f=100 * (i - 1), p=i)
              for i in range(1, 1567)]
        for url in us:
            yield scrapy.Request(url)

    def parse(self, response):
        obj = json.loads(response.body_as_unicode())
        results = obj.get('result', [])
        for result in results:
            if result.get('type', '') != 'article':
                continue
            item = CnnItem()
            url = result.get('url', '')
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
