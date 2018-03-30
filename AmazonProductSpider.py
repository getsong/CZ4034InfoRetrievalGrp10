# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import urllib
from amazon.items import AmazonItem
from urllib.request import urlopen


class AmazonProductSpider(scrapy.Spider):
    name = 'AmazonDeals'
    allowed_domains = ['amazon.com']
    start_urls = [
"https://www.amazon.com/Girls-Burn-Brighter-Shobha-Rao/dp/1250074258/ref=tmm_hrd_swatch_0/ref=s9_acss_bw_cg_KCedit_3a1_w?_encoding=UTF8&qid=&sr=&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=CTKPFANT9RVASAN96NXD&pf_rd_t=101&pf_rd_p=c253803e-5e23-4dbc-9098-ecc0478fba31&pf_rd_i=17143709011%27"
]
    
    def parse(self, response):
        items = AmazonItem()
        title = response.xpath('//h1[@id="title"]/span/text()').extract()
##        sale_price = response.xpath('//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()').extract()
##        category = response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract()
##        availability = response.xpath('//div[@id="availability"]//text()').extract()
        description = response.css('div#bookDescription_feature_div noscript').extract()
        print(description)
        items['product_name'] = ''.join(title).strip()
##        items['product_sale_price'] = ''.join(sale_price).strip()
##        items['product_category'] = ','.join(map(lambda x: x.strip(), category)).strip()
##        items['product_availability'] = ''.join(availability).strip()
        yield items
        
