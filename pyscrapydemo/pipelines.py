# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re


class BaidustocksInfoPipeline(object):
    def open_spider(self, spider):
        self.f = open(os.path.abspath('.')+'\\BaiduStockInfo.txt', 'w')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        try:
            line = str(dict(item)) + '\n'
            self.f.write(line)
        except:
            pass
        return item


class BookPipeline(object):
    star_dict = {
        'One': '1星',
        'Two': '2星',
        'Three': '3星',
        'Four': '4星',
        'Five': '5星',
    }

    @classmethod
    def from_crawler(cls, crawler):
        cls.exchange_rate = 8.8135
        return cls()

    def process_item(self, item, spider):
        item['book_star'] = self.star_dict.get(item['book_star'], 'No Star')
        return item
