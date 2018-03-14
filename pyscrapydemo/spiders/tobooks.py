# -*- coding: utf-8 -*-
import scrapy
from pyscrapydemo.items import BookItem


class TobooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        book_item = BookItem()
        for book in response.css('article.product_pod'):
            book_item['book_name'] = book.css(
                'h3 a::attr(title)').extract_first()
            book_item['book_price'] = book.css(
                'p.price_color::text').extract_first()
            book_item['book_star'] = book.css('p').extract_first()
            yield book_item
        next_url = response.css('li.next a::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
