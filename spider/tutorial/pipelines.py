# -*- coding: utf-8 -*-

import codecs
import json
import os

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TutorialPipeline(object):
    def __init__(self):
        json_path = os.path.join(BASE_PATH, '../file/chinaz.json')
        self.file = codecs.open(json_path, mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        return item

    def close_file(self):
        self.file.close()
