# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 14:40:09 2018

@author: daq11
"""

from selenium import webdriver
import re
import json
#
# crawl text
#

driver = webdriver.Chrome("C:/Users/daq11/Downloads/chromedriver_win32/chromedriver.exe")

with open("C:/Users/daq11/Dropbox/developer/CZ4034/CZ4034InfoRetrievalGrp10/amazon/output_cook_origin.txt") as f:
    links = [x.strip('\n') for x in f.readlines()] # should continue from here
# try crawl index
f.close()

# for each category, initialize one json file
with open("literature.json", mode='w', encoding='utf-8') as f:
    json.dump([], f)
f.close()

json_data = []
for link in links:
    data_dump = []
    driver.get(link)

    try:
        title_span = driver.find_element_by_xpath('//*[@id="productTitle"]')
        title = title_span.get_attribute('innerHTML')
    except:
        f_e = open('error record_cook.txt','a')
        f_e.write(''.join([link,'\n']))
        f_e.close()
        continue

    try:
        rating_box = driver.find_element_by_xpath('//*[@id="reviewSummary"]/div[2]/span/a/span')
        rating_score = rating_box.get_attribute('innerHTML')
    except:
        try:
            rating_box = driver.find_element_by_xpath('//*[@id="dp-no-customer-review-yet"]')
            rating_score = rating_box.get_attribute('innerHTML')
        except:
            f_e = open('error record_cook.txt','a')
            f_e.write(''.join([link,'\n']))
            f_e.close()
            continue

    try:
        driver.switch_to_frame(driver.find_element_by_id("bookDesc_iframe"))
        review = driver.find_element_by_xpath('//*[@id="iframeContent"]')
        review_text = review.get_attribute('innerHTML')
        review = re.sub('<.*?>', '', review_text)
    except:
        f_e = open('error record_cook.txt','a')
        f_e.write(''.join([link,'\n']))
        f_e.close()
        continue

    data = {
			'product_name':title,
			'description':review,
			'ratings':rating_score,
            'url':link
			}

    #data_dump.append(data)


    with open("cook.json", mode='r', encoding='utf-8') as feedsjson:
        feeds = json.load(feedsjson)
    with open("cook.json", mode='w', encoding='utf-8') as feedsjson:
        feeds.append(data)
        json.dump(feeds, feedsjson,indent=4)
    feedsjson.close()

# check json file length
# with open("cook.json", mode='r', encoding='utf-8') as feedsjson:
#     feeds = json.load(feedsjson)
#     print(len(feeds))
#