# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import urllib
from amazon.items import AmazonItem
from urllib.request import urlopen
import os


class AmazonProductSpider(scrapy.Spider):
    name = 'AmazonDeals'
    allowed_domains = ['amazon.com']
    start_urls = []
    
    def parse(self, response):
        with open(os.path.join('..', 'output_business.txt'), 'r') as infile:
            url = infile.readline().strip()
            count = 0
            while len(url) > 0 and count < 5:
                self.start_urls.append(url)
                url = infile.readline().strip()
                count += 1
        print('urls: ')
        print(self.start_urls)
        items = AmazonItem()
        title = response.xpath('//h1[@id="title"]/span/text()').extract()
##        sale_price = response.xpath('//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()').extract()
##        category = response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract()
##        availability = response.xpath('//div[@id="availability"]//text()').extract()
        description = response.css('div#bookDescription_feature_div noscript').extract()
        print(description)
        items['product_description'] = ''.join(title).strip()
##        items['product_sale_price'] = ''.join(sale_price).strip()
##        items['product_category'] = ','.join(map(lambda x: x.strip(), category)).strip()
##        items['product_availability'] = ''.join(availability).strip()
        yield items
        
