# -*- coding: utf-8 -*-
import scrapy
from amazon.items import AmazonItem


class AmazonProductSpider(scrapy.Spider):
    name = 'AmazonDeals'
    allowed_domains = ['amazon.com']
    start_urls = [
        "https://www.amazon.com/gp/product/B01M7XPGYE/"
    ]

    def parse(self, response):
        items = AmazonItem()
        # description = response.xpath(
        #     "$('iframe[@id=\"bookDesc_iframe\"].find('p').text()//$(document).html//div[@id=iframeContent]/p[2]/text()'
        # ).extract()
        # description = response.xpath(
        #     '$("span[id=\"ebooksProductTitle\"]").text()'
        # ).extract()
        items['product_description'] = ''.join(description).strip()
        yield items

