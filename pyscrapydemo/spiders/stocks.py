# -*- coding: utf-8 -*-
import scrapy
import re


class StocksSpider(scrapy.Spider):
    name = 'stock'
    # allowed_domains = ['baidu.com']
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://gupiao.baidu.com/',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                          Chrome/39.0.2171.95 Safari/537.36"
        }
        for href in response.css('a::attr(href)').extract():
            try:
                # 处理链接，提取出股票代码
                stock_code = re.findall(r'[s][hz]\d{6}', href)[0]
                stock_url = 'https://gupiao.baidu.com/stock/'+stock_code+'.html'
                yield scrapy.Request(stock_url, callback=self.parse_stock_info, headers=headers)
            except Exception as e:
                print(str(e))
                continue

    @staticmethod
    def parse_stock_info(response):
        info_dict = {}
        stock_info = response.css('.stock-bets')
        stock_name = stock_info.css('.bets-name').extract_first('')
        keyList = stock_info.css('dt').extract()
        valueList = stock_info.css('dd').extract()
        for index in range(len(keyList)):
            key = re.findall(r'>.*</dt>', keyList[index])[0][1:-5]
            try:
                value = re.findall(
                    r'\d+\.?.*</dd>', valueList[index])[0][0:-5]
            except Exception as e:
                print(str(e))
                value = '--'
            info_dict[key] = value
        info_dict.update(
            {'股票名称': re.findall('\s.*\(', stock_name)[0].split()[0] + re.findall('>.*<', stock_name)[0][1:-1]})
        yield info_dict


