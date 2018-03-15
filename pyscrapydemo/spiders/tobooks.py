# -*- coding: utf-8 -*-
import scrapy
from pyscrapydemo.items import BookItem
from scrapy.linkextractors import LinkExtractor


class TobooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse_book(self, response):
        # 提取书籍的相关信息存到item中
        book_item = BookItem()
        book_item['book_name'] = response.css(
            'div.product_main h1::text').extract_first()
        book_item['book_price'] = response.css(
            'div.product_main p.price_color::text').extract_first()
        book_item['book_star'] = response.css('p.star-rating::attr(class)')\
                                         .re_first(r'[A-Z][a-z]+')
        book_item['book_code'] = response.css(
            'tr:nth-child(1) td::text').extract_first()
        book_item['book_avai'] = response.css(
            'tr:nth-last-child(2) td::text').re_first(r'\d+')
        book_item['book_review'] = response.css(
            'tr:nth-last-child(1) td::text').extract_first()
        yield book_item

    def parse(self, response):
        # 提取主页每本书的链接
        le = LinkExtractor(restrict_css='article.product_pod h3')
        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_book)

        # 提取下一页链接
        le_next = LinkExtractor(restrict_css='ul.pager li.next')
        link_next = le_next.extract_links(response)
        if link_next:
            yield scrapy.Request(link_next[0].url)
