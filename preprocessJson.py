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
    # with open("crawl/cook.json", mode='r', encoding='utf-8') as feedsjson:
    #     feeds = json.load(feedsjson)[:2]
    #     description_list = []
    #     for jsonData in feeds:
    #         description = manualRemove(jsonData['description'])
    #         processed_des_list = preprocess.processJson(description)
    #         description_list.append(processed_des_list)
    #
    # print(description_list)

    with open("amazon_all.json", mode='w', encoding='utf-8') as f:
        json.dump([], f)
        feeds = []

    with open("crawl/cook.json", mode='r', encoding='utf-8') as feedsjson:
        feeds_cook = json.load(feedsjson)
        for feed in feeds_cook:
            feed['category'] = 'cook'
            rating_str = feed['ratings']
            if rating_str == "There are no customer reviews yet.":
                feed['ratings'] = 0
            else:
                score = rating_str.split(" ")[0]
                score = float(score)
                feed['ratings'] = score
            feeds.append(feed)
    print("finish1")

    with open("crawl/literature.json", mode='r', encoding='utf-8') as feedsjson:
        feeds_lit = json.load(feedsjson)
        for feed in feeds_lit:
            feed['category'] = 'literature'
            rating_str = feed['ratings']
            if rating_str == "There are no customer reviews yet.":
                feed['ratings'] = 0
            else:
                score = rating_str.split(" ")[0]
                score = float(score)
                feed['ratings'] = score
            feeds.append(feed)
    print("finish2")

    with open("crawl/sports.json", mode='r', encoding='utf-8') as feedsjson:
        feeds_sports = json.load(feedsjson)
        for feed in feeds_sports:
            feed['category'] = 'sports'
            rating_str = feed['ratings']
            if rating_str == "There are no customer reviews yet.":
                feed['ratings'] = 0
            else:
                score = rating_str.split(" ")[0]
                score = float(score)
                feed['ratings'] = score
            feeds.append(feed)
    print("finish3")

    with open("crawl/business.json", mode='r', encoding='utf-8') as feedsjson:
        feeds_biz = json.load(feedsjson)
        for feed in feeds_biz:
            feed['category'] = 'business'
            rating_str = feed['ratings']
            if rating_str == "There are no customer reviews yet.":
                feed['ratings'] = 0
            else:
                score = rating_str.split(" ")[0]
                score = float(score)
                feed['ratings'] = score
            feeds.append(feed)
    print("finish4")

    with open("crawl/amazon_all.json", mode='w', encoding='utf-8') as f:
        json.dump(feeds, f, indent=4)




