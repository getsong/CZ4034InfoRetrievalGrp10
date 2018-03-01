# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 17:19:54 2018

@author: daq1130
"""

from lxml import html
import csv
import os
import requests
from exceptions import ValueError
from time import sleep
from random import randint
import json
from selenium import webdriver
from bs4 import BeautifulSoup

def parse(url):
    #driver = webdriver.Chrome("c:/users/daq11/python2virtual/lib/site-packages")
    #driver.get(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    
    try:
        # Retrying for failed requests
        for i in range(20):
            # Generating random delays
            sleep(randint(1,3))
            # Adding verify=False to avold ssl related issues
            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200: 
                doc = html.fromstring(response.content)
                XPATH_NAME = '//h1[@id="title"]//text()'
                #XPATH_NAME = '//h1[@id="title"]//span[contains(@id,"productTitle)]//text()'
                #XPATH_NAME = '//span[contains(@id,"productTitle)]/text()'
                XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
                #XPATH_DESCRIPTION = '//div[@id="bookDesc_iframe_wrapper"]//text()'
                #driver.switchTo().frame("bookDesc_iframe");
                XPATH_DESCRIPTION = "//div[@id='iframeContent']//text()"
                XPATH_DESCRIPTION = "div[@id='iframeContent' and ancestor::iframe]//text()"
                
                iframe = '<iframe id="bookDesc_iframe" class="ap_never_hide" width="100%" scrolling="no" frameborder="0" style="height: 858px;"></iframe>'
                soup = BeautifulSoup(iframe, 'html.parser')
                tag = soup.find_all('div')
                print(tag[0])

                RAW_NAME = doc.xpath(XPATH_NAME)
                RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
                RAw_DESCRIPTION = doc.xpath(XPATH_DESCRIPTION)

                NAME = ' '.join(''.join(RAW_NAME).encode('utf-8').split()) if RAW_NAME else None
                CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]).encode('utf-8') if RAW_CATEGORY else None
                DESCRIPTION = ''.join(RAw_DESCRIPTION).encode('utf-8').strip() if RAw_DESCRIPTION else None

                # retrying in case of captcha
                if not NAME:
                    raise ValueError('captcha')

                data = {
                    'NAME': NAME,
                    'CATEGORY': CATEGORY,
                    'DESCRIPTION':DESCRIPTION,
                    'URL': url,
                }
                #debugging
                print DESCRIPTION
                return data
            
            elif response.status_code==404:
                break

    except Exception as e:
        print e

def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    urls = ['0316338869',
            '0525522603']
    extracted_data = []
    print extracted_data
    for i in urls:
        url = "http://www.amazon.com/dp/" + i
        print "Processing: " + url
        # Calling the parser
        parsed_data = parse(url)
        if parsed_data:
            extracted_data.append(parsed_data)
            
    # write to json
    json_data = json.dumps(extracted_data)
    
    with open('output_json.txt','w') as outfile:
        json.dump(json_data,outfile)
    

    # Writing scraped data to csv file
    with open('scraped_data.csv', 'w') as csvfile:
        fieldnames = ['NAME','CATEGORY','DESCRIPTION','URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()    
        for data in extracted_data:
            writer.writerow(data)

if __name__ == "__main__":
    ReadAsin()