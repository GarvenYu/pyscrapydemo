# -*- coding: utf-8 -*-
import scrapy
import re


class StocksSpider(scrapy.Spider):
    name = 'stock'
    # allowed_domains = ['baidu.com']
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                # 处理链接，提取出股票代码
                stock_code = re.findall(r'[s][hz]\d{6}', href)[0]
                stock_url = 'http://gupiao.baidu.com/stock/'+stock_code+'.html'
                yield scrapy.Request(stock_url, callback=self.parse_stockinfo)
            except Exception as e:
                print(str(e))
                continue

    def parse_stockinfo(self, response):
        infoDict = {}
        stock_info = response.css('.stock-bets')
        stock_name = stock_info.css('.bets-name').extract_first('')
        keyList = stock_info.css('dt').extract()
        valueList = stock_info.css('dd').extract()
        for index in range(len(keyList)):
            key = re.findall(r'>.*</dt>', keyList[index])[0][1:-5]
            try:
                value = re.findall(
                    r'\d+\.?.*</dd>', valueList[index])[0][0, -5]
            except Exception as e:
                print(str(e))
                value = '--'
            infoDict[key] = value
        infoDict.update(
            {'股票名称': re.findall('\s.*\(', stock_name)[0].split()[0] +
             re.findall('\>.*\<', stock_name)[0][1:-1]})
        yield infoDict
