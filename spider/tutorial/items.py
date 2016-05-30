# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    web_title = scrapy.Field()
    web_url = scrapy.Field()
    alexa_num = scrapy.Field()
    alexa_url = scrapy.Field()
    baidu_num = scrapy.Field()
    baidu_url = scrapy.Field()
    google_num = scrapy.Field()
    google_url = scrapy.Field()
