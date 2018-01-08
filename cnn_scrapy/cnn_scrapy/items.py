# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnnItem(scrapy.Item):
    """
        item['url'] = response.url
        item['title'] = title
        item['author'] = author
        item['update_time'] = update_time
        item['cat'] = cat
        item['pic'] = pic
        item['keyword'] = keyword
        item['text'] = text
    """
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    update_time = scrapy.Field()
    cat = scrapy.Field()
    pic = scrapy.Field()
    keyword = scrapy.Field()
    text = scrapy.Field()
