# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)

import base64
from random import choice
from scrapy.exceptions import IgnoreRequest, CloseSpider


# from jianjie.utils.bloomfilter import PyBloomFilter, rc


# class BloomfilterMiddleware(object):
# 	def __init__(self):
# 		self.bf = PyBloomFilter(conn=rc)
#
# 	def process_request(self, request, spider):
# 		url = request.url
# 		if self.bf.is_exist(url):
# 			raise IgnoreRequest
# 		else:
# 			self.bf.add(url)

# class CloseMiddleware(object):
# 	def process_response(self, request, response, spider):
# 		if response.status == 402:
# 			raise CloseSpider('402 proxy no use')
# 		else:
# 			return response


class ProxyMiddleware(object):
    def __init__(self):
        self.proxyServer = "http://http-dyn.abuyun.com:9020"
        pl = [
            "H1XX369E3AGF7AQD:F2F5005CDF302D89",
        ]
        self.proxyAuths = ["Basic " + base64.urlsafe_b64encode(bytes(p, "ascii")).decode("utf8") for p in pl]

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxyServer
        request.headers["Proxy-Authorization"] = choice(self.proxyAuths)


class RetryMiddleware(object):
    def process_response(self, request, response, spider):
        if response.status in [429, 503]:
            # print('wrong status: %s, retrying~~' % response.status, request.url)
            retryreq = request.copy()
            retryreq.dont_filter = True
            return retryreq
        else:
            # url = response.url
            # if 'doDetailSearch' in url:
            # 	paramAn = response.xpath('//input[@id="paramAn"]/@value').extract_first()
            # 	if not paramAn:
            # 		print('no paramAn, retry')
            # 		retryreq = request.copy()
            # 		retryreq.dont_filter = True
            # 		return retryreq
            return response


class RotateUserAgentMiddleware(object):
    """Middleware used for rotating user-agent for each request"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('USER_AGENT_CHOICES', []))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', choice(self.agents))
