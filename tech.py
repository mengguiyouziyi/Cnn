# coding:utf-8

import requests
from lxml import etree
import time
from selenium import webdriver


user_agent = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
s = requests.session()


for page in range(1, 20):
    url = "http://edition.cnn.com/search?size=10&q=politics&from=40&page="+str(page)
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(2)
    list_urls = browser.find_elements_by_xpath('//div[@class="cnn-search__results-list"]//h3[@class="cnn-search__result-headline"]/a')
    for i in list_urls:
        list_url = i.get_attribute('href')
        res = s.get(list_url, headers=headers)
        detail_html = etree.HTML(res.content)
        titles = detail_html.xpath('//h1[@class="pg-headline"]/text()')
        print("标题----------" + "".join(titles).strip())
        author_name = detail_html.xpath('//p[@class="metadata__byline"]/span/a/text()')
        author_title = detail_html.xpath(
            '//div[@class="field field-name-field-external-authors"]//span[@class="expert-job-title"]/text()')
        if author_name:
            print('作者----------' + "".join([i + ',' for i in author_name]).strip())
        else:
            author_name = "空"
            print('作者----------' + author_name.strip())
        if author_title:
            print('简介-------' + "".join(author_title).strip())
        else:
            author_title = "空"
            print('简介-------' + author_title.strip())
        ctimes = detail_html.xpath('//p[@class="update-time"]/text()')
        print('发布时间--------' + "".join(ctimes).split(')')[-1].strip())
        c_type = '专题'
        print("类型-----------" + c_type)
        imgs = ""
        if detail_html.xpath('//div[@class="l-container"]/div//img/@src'):
            imgs = detail_html.xpath('//div[@class="l-container"]/div//img/@src')[0]
            img_res = s.get("http:" + imgs)
            with open(imgs.strip().split('/')[-1], 'wb') as f:
                f.write(img_res.content)
            f.close()
        else:
            imgs = '空'
        print("图片----------" + "http:" + imgs)
        source = list_url
        print('来源------------' + "http:" + list_url)
        contents = ""
        content = detail_html.xpath('//div[@class="zn-body__paragraph"]//text()')
        list_cons = list()
        for num_p in range(1, len(content) + 1):
            p_cons = detail_html.xpath('//div[@class="zn-body__paragraph"][%s]//text()' % (num_p))
            pp_cons = ""
            for p_con in p_cons:
                pp_cons += p_con.strip()
            list_cons.append(pp_cons)
        for con in list_cons:
            contents += "<div>" + con.strip().replace('\n', ' ') + "</div>"
        print("内容--------" + contents)
        keyword = ""
        if detail_html.xpath('//div[@class="zn-body__paragraph"]//text()'):
            keyword = list_cons[0]
        else:
            keyword = "空"
        print("关键字---------" + keyword.strip().replace('\n', ' '))
        if len(contents) > 0:
            with open('cnn.txt', 'a', encoding='utf-8') as f:
                f.write("".join(titles).strip() + ';;;' + "".join(author_name).strip() + ';;;' + "".join(
                    author_title).strip() + ';;;' + "".join(
                    ctimes).strip() + ';;;' + c_type.strip() + ';;;' + imgs.strip() + ';;;' + keyword.strip().replace(
                    '\n',
                    ' ') + ';;;' + list_url.strip() + ';;;' + contents.strip() + '\n')
            f.close()





