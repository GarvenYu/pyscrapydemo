# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    """docstring for BookItem"""
    book_name = scrapy.Field()
    book_price = scrapy.Field()
    book_star = scrapy.Field()
    book_code = scrapy.Field()
    book_avai = scrapy.Field()
    book_review = scrapy.Field()
