# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv

class NewsPipeline(object):
    def __init__(self):
            self.file = open('C:/Users/徐/Desktop/news/ji.csv', 'w+',encoding="utf-8",newline="")
            # csv写法
            self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        self.writer.writerow([item['title'],item['datetime'],item['url'],item['content'],item['source']])

    def close_spider(self, spider):
        self.file.close()