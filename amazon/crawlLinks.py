# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 14:40:09 2018

@author: daq11
"""
from selenium import webdriver

driver = webdriver.Chrome("C:/Users/daq11/chromedriver_win32/chromedriver.exe")


# =============================================================================
# # business - personal finance 60 entries
# str1 = "https://www.amazon.com/s/ref=lp_2717_pg_"
# str2 = "?rh=n%3A283155%2Cn%3A%211000%2Cn%3A3%2Cn%3A2717&page="
# str3 = "&ie=UTF8&qid=1522379724"
# =============================================================================

# 2717 business - perfonal finance
# 2675 business - management
# 2665 business - investing
# 2698 business - marketing
# 2581 business - economics

lp_list = [2665,2698,2581]

for j in lp_list:
    str1 = "https://www.amazon.com/s/ref=lp_"
    str2 = str(j)
    str3 = "_pg_"
    # need str4 for page
    str5 = "?rh=n%3A283155%2Cn%3A%211000%2Cn%3A3%2Cn%3A"
    str6 = "&page="
    # need str7 for page
    str8 = "&ie=UTF8&qid=1522382251"
    

    href_list = []
    for i in range(1,61):
        driver.get(''.join([str1,str2,str3,str(i),str5,str6,str(i),str8]))  
        links = driver.find_elements_by_css_selector(".a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal")
        for link in links:
            href = link.get_attribute('href')
            href_list.append(href)
                
            
    text_file = open("amazon_output.txt", "a")
    for href in href_list:
        text_file.write(''.join([href,'\n']))
    text_file.close()
