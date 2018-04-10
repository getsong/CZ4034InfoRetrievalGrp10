# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 12:49:16 2018

@author: daq11
"""

import json

if __name__ == "__main__":
    
    with open("crawl/amazon_all_withID.json", mode='w', encoding='utf-8') as f:
        json.dump([], f)
        feeds = []

    with open("crawl/amazon_all.json", mode='r', encoding='utf-8') as feedsjson:
        feeds = json.load(feedsjson)
        index = 0
        for feed in feeds:
            feed['DocID'] = index
            feeds.append(feed)
            index += 1
    print("finish")
    
    with open("crawl/amazon_all_withID.json", mode='w', encoding='utf-8') as f:
        json.dump(feeds, f, indent=4)