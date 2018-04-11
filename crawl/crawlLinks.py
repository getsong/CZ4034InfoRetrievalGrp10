# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 14:40:09 2018

@author: daq11
"""
from selenium import webdriver

driver = webdriver.Chrome("chromedriver.exe")

type_list = {
        "business":"3A3",
        "sports":"3A26",
        "food":"3A6",
        "literature":"3A17"
            }

lp_list = [4245] # refer to below index, put suitable index list in
# 2717 business - perfonal finance
# 2675 business - management
# 2665 business - investing
# 2698 business - marketing
# 2581 business - economics
# 16327 sports - basketball
# 16315 sports - baseball
# 16378 sports - football
# 16638 sports - soccer
# 16381 sports - golf
# 4196 food - baking
# 4251 food - cooking
# 4201 food - dessert
# 4257 food - quick&easy
# 4252 food - cooking methods
# 4336 food - vegetarian
# 4245 food - outdoor cooking
# 2159 literature - drama
# 10399 literature - classic
# 10129 literature - contemp

for j in lp_list:

    str1 = "https://www.amazon.com/s/ref=lp_"
    str2 = str(j)
    str3 = "_pg_"
    # need str4 for page
    str5 = "?rh=n%3A283155%2Cn%3A%211000%2Cn%"
    str6 = type_list["food"]  # need to change with different categories
    str7 = "%2Cn%3A"
    str8 = str(j)
    str9 = "&page="
    # need str9 for page
    str11 = "&ie=UTF8&qid=1522382251"

    href_list = []
    for i in range(1,61):  # extract page 1 to 100
        href_list = []
        driver.get(''.join([str1,str2,str3,str(i),str5,str6,str7,str8,str9,str(i),str11]))
        links = driver.find_elements_by_css_selector(".a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal")
        for link in links:
            href = link.get_attribute('href')
            href_list.append(href)

        text_file = open("output_cook_addon.txt", "a")
        for href in href_list:
            text_file.write(''.join([href,'\n']))
        text_file.close()

        text_file = open("progress_cook_addon.txt", "a")
        text_file.write(''.join(["list", str(j), "page", str(i), "append finish","\n"]))
        text_file.close()

        print("list", j, "page", i, "append finish")

#remove duplicates
with open("output_business_origin.txt") as f:
    links = [x.strip('\n') for x in f.readlines()]
f.close()
links = set(links)
print(len(links))
text_file = open("output_business_origin.txt", "w")
for link in links:
    text_file.write(''.join([link, "\n"]))
text_file.close()

# check json file length
# with open("cook.json", mode='r', encoding='utf-8') as feedsjson:
#     feeds = json.load(feedsjson)
#     print(len(feeds))
#
