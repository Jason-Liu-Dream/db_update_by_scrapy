# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from spider.tutorial.items import TutorialItem


class ChinazSpider(CrawlSpider):
    """chinaz的爬虫"""
    name = "ChinazSpider"
    download_delay = 0.5  # 设置爬虫的延时，为0.5s
    allowed_domains = ["top.chinaz.com"]  # 设置爬虫的爬取域

    # 设置爬虫的起始位置
    start_urls = (
        'http://top.chinaz.com/all/index.html',
    )

    rules = (
        Rule(LinkExtractor(allow=('all/index(_([\d]+))?.html',), ), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        # 将获取的信息保存成项目的形式

        blocks = sel.xpath('//ul[@class="listCentent"]/li/div[@class="CentTxt"]')
        items = []  # 将item按照列表保存

        for block in blocks:
            item = TutorialItem()
            web_title = block.xpath(u'h3/a/text()').extract_first()
            web_url = block.xpath(u'h3/a/@href').re_first('\w?\/site_([\w\.-]+)\.html')
            item['web_title'] = web_title.replace('\"', '\'').strip()
            item['web_url'] = web_url

            alexa_num = block.xpath(u'div/p[contains(span/text(), "Alexa周排名：")]/a/text()').extract_first()
            alexa_url = block.xpath(u'div/p[contains(span/text(), "Alexa周排名：")]/a/@href').extract_first()
            item['alexa_num'] = alexa_num
            item['alexa_url'] = alexa_url

            baidu_num = block.xpath(u'div/p[contains(span/text(), "百度权重为：")]/a/img/@src').re_first('baidu\/(\d+)\.gif')
            baidu_url = block.xpath(u'div/p[contains(span/text(), "百度权重为：")]/a/@href').extract_first()
            item['baidu_num'] = baidu_num
            item['baidu_url'] = baidu_url

            google_num = block.xpath(u'div/p[contains(span/text(), "PR：")]/a/img/@src').re_first('Rank_(\d+).gif')
            google_url = block.xpath(u'div/p[contains(span/text(), "PR：")]/a/@href').extract_first()
            item['google_num'] = google_num
            item['google_url'] = google_url

            items.append(item)
        return items
