#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
spider_run.py

Author: Jason liu
Date: 2016-04-22
"""
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from spider.tutorial.spiders.ChinazSpider import ChinazSpider
from twisted.internet import reactor


def run_spiders():
    """
    说明：
        如果该调用程序是程序的最外层循环，那么此处可以直接调用爬虫的配置文件：
        在文件中使用如下代码：
        from scrapy.utils.project import get_project_settings
        # some code
        runner = CrawlerRunner(get_project_settings())

        如果该程序调用只是一个封装的函数，则配置文件需要自己构造，如下面的代码
    """
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})  # 定义日志格式
    # 设置当前爬虫的配置信息，此处是选择要调用的pipe
    settings = Settings()
    settings.set('ITEM_PIPELINES', {'spider.tutorial.pipelines.TutorialPipeline': 300,})
    # 将加载后的配置文件加载到爬虫中
    runner = CrawlerRunner(settings)  # 启用爬虫运行器

    d = runner.crawl(ChinazSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    run_spiders()
