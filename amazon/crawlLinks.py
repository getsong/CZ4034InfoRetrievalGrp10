# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 14:40:09 2018

@author: daq11
"""
from selenium import webdriver
import re
import json

driver = webdriver.Chrome("C:/Users/daq11/chromedriver_win32/chromedriver.exe")


with open("C:/Users/daq11/Dropbox/developer/CZ4034/CZ4034InfoRetrievalGrp10/amazon/output_sports.txt") as f:
    links = [x.strip('\n') for x in f.readlines()][202:300] # should continue from 202
# try crawl index
f.close()

# for each category, initialize one json file
# =============================================================================
# with open("sports_new.json", mode='w', encoding='utf-8') as f:
#     json.dump([], f)
# f.close()
# =============================================================================

json_data = []
for link in links:
    
    data_dump = []
    driver.get(link)
    
    try:
        title_span = driver.find_element_by_xpath('//*[@id="productTitle"]')
        title = title_span.get_attribute('innerHTML')
    except:
        f_e = open('error record.txt','a')
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
            f_e = open('error record.txt','a')
            f_e.write(''.join([link,'\n']))
            f_e.close()
            continue            
    
    try:
        driver.switch_to_frame(driver.find_element_by_id("bookDesc_iframe"))
        review = driver.find_element_by_xpath('//*[@id="iframeContent"]')
        review_text = review.get_attribute('innerHTML')
        review = re.sub('<.*?>', '', review_text)
    except:
        f_e = open('error record.txt','a')
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
        
        
    with open("sports.json", mode='r', encoding='utf-8') as feedsjson:
        feeds = json.load(feedsjson)
    with open("sports.json", mode='w', encoding='utf-8') as feedsjson:
        feeds.append(data)
        json.dump(feeds, feedsjson,indent=4)
    feedsjson.close()
    
    
# =============================================================================
#     product_name
#     description
#     ratings
# =============================================================================





# =============================================================================
# # =============================================================================
# # # business - personal finance 60 entries
# # str1 = "https://www.amazon.com/s/ref=lp_2717_pg_"
# # str2 = "?rh=n%3A283155%2Cn%3A%211000%2Cn%3A3%2Cn%3A2717&page="
# # str3 = "&ie=UTF8&qid=1522379724"
# # =============================================================================
# 
# 
# 
# type_list = {
#         "business":"3A3",
#         "sports":"3A26",
#         "food":"3A6",
#         "literature":"3A17"
#             }
# 
# lp_list = [2159,10399,10129] # refer to below index, put suitable index list in
# # 2717 business - perfonal finance
# # 2675 business - management
# # 2665 business - investing
# # 2698 business - marketing
# # 2581 business - economics
# # 16327 sports - basketball
# # 16315 sports - baseball
# # 16378 sports - football
# # 16638 sports - soccer
# # 16381 sports - golf
# # 4196 food - baking
# # 4251 food - cooking
# # 4201 food - dessert
# # 4257 food - quick&easy
# # 4252 food - cooking methods
# # 4336 food - vegetarian
# # 2159 literature - drama
# # 10399 literature - classic
# # 10129 literature - contemp
# 
# for j in lp_list:   
# 
#     str1 = "https://www.amazon.com/s/ref=lp_"
#     str2 = str(j)
#     str3 = "_pg_"
#     # need str4 for page
#     str5 = "?rh=n%3A283155%2Cn%3A%211000%2Cn%"
#     str6 = type_list["literature"]  # need to change with different categories
#     str7 = "%2Cn%3A"
#     str8 = str(j)
#     str9 = "&page="
#     # need str9 for page
#     str11 = "&ie=UTF8&qid=1522382251"
#         
#     href_list = []
#     for i in range(1,101):  # extract page 1 to 100
#         driver.get(''.join([str1,str2,str3,str(i),str5,str6,str7,str8,str9,str(i),str11]))  
#         links = driver.find_elements_by_css_selector(".a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal")
#         for link in links:
#             href = link.get_attribute('href')
#             href_list.append(href)
#                 
#             
#     text_file = open("output_sports.txt", "a")
#     for href in href_list:
#         text_file.write(''.join([href,'\n']))
#     text_file.close()
# =============================================================================
    
