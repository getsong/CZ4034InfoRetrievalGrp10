# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 13:39:28 2018

@author: daq11
"""

import preprocess
import json
import re

def manualRemove(text):
    text = re.sub('‘', '\'', text)
    text = re.sub('’','\'', text)
    text = re.sub('“', '\'', text)
    text = re.sub('”', '\'', text)
    text = re.sub('—', ' ', text)
    return text

if __name__ == "__main__":

    with open("crawl/amazon_Stemmed.json", mode='w', encoding='utf-8') as f:
        json.dump([], f)
        
    feeds = []
    product_names = []
    descriptions = []

    with open("crawl/amazon_all_withID.json", mode='r', encoding='utf-8') as feedsjson:
        feeds_o = json.load(feedsjson)[]
        
    index = 1
    for feed in feeds_o:
        name_origin = manualRemove(feed['product_name'])
        feed['product_name'] = preprocess.processJson(name_origin)
        description_origin = manualRemove(feed['description'])
        feed['description'] = preprocess.processJson(description_origin)
        feeds.append(feed)
        print("finish ", index)
        if index % 20 == 0:
            with open("preprocess/amazon_Stemmed.json", mode='a', encoding='utf-8') as f:
                json.dump(feeds, f, indent=4)
                feeds = []
        index += 1
            

