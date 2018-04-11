from django.shortcuts import render
import os
import sys
import requests
import json
import traceback
import time
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
from preprocess import Preprocessor
import re
import numpy as np


indexStyle = """
.title
{
    text-align: center;
    margin: 17% 0 0 0;
}

.search-container
{
    float:center;
    margin: 40px 20% 40px 20%;
    min-width: 500px;
    text-align: center;
}

.search-bar
{
    min-width: 80%;
}

input[type=checkbox]
{
    transform: scale(1.5);
    margin: 10px 20px 0 10px;
}"""

# os_str = os.path.join(base_dir, 'gui', 'static', 'book3.jpg')
# os_str = re.sub(r"\\",'/',os_str)
                    

searchStyle = """
.title
{
    margin: 0 0 0 1%;
    max-width: 50%;
    float: left;
}

.search-container
{
    float:center;
    margin: 30px 0 10px 500px;
    max-width: 600px;
    text-align: center;
}

.search-bar
{
    min-width: 80%;
    margin: 0 0 0 0;
}

input[type=checkbox]
{
    transform: scale(1.5);
    margin: 10px 20px 0 10px;
}

.results
{
    margin-left:20px;
}

.book-title
{
    font-size: 20px;
    font-weight: bold;
    color: darkblue;
}
"""


def spellingCheck(str1):
    words = np.loadtxt('test.txt', dtype="str", delimiter=',')  # X is an array

    def levenshtein1(s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t:
            return 0
        elif len(s) == 0:
            return len(t)
        elif len(t) == 0:
            return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]

        return v1[len(t)]
    ld=[]
    for i in words:
        ld.append((levenshtein1(i, str1)))

    if(min(ld) == 0):
        return "?"
    else:
        return words[np.argmin(ld)]


def index(request):
    """show index page, no search result should be displayed and search bar is in the center of the page"""
    contextDict = {}
    contextDict['result'] = ""
    contextDict['css'] = indexStyle
    return render(request, 'group10/form.html', context=contextDict)


def search(request):
    """show search page"""
    contextDict = {}

    if request.method == 'POST':
        # if there is query (which is always through POST method)
        try:
            startTime = time.time()

            # get what user typed for query
            userQuery = request.POST.get("search")

            # check spelling
            rawQueryList = userQuery.split()
            isSpellingWrong = False
            if len(rawQueryList) == 1 and request.POST.get('cook') is None:
                returnStr = spellingCheck(rawQueryList[0])
                if returnStr != "?":
                    isSpellingWrong = True
                else:
                    isSpellingWrong = False

            # preprocess data by tokenizing, lemmatizing, etc., returning a list of lemmas
            p = Preprocessor()
            queryList = p.preprocess(userQuery)

            # if list of lemmas is not too long, try advanced search of 2-grams and combinations
            if len(queryList) <= 10:
                twoGramList = [''.join(['\"', queryList[i], ' ', queryList[i + 1], '\"^10']) for i in
                               range(len(queryList) - 1)]
                combiList = [''.join(['(', queryList[i], ' AND ', queryList[j], ')^3']) for i in range(len(queryList))
                             for j in range(i + 1, len(queryList)) if queryList[i] != queryList[j]]
                query = ' '.join(twoGramList + combiList + queryList)
            else:
                query = ' '.join(queryList)
            # replace quotation mark and whitespace with chars legit in the request url
            query = re.sub(r'\"', '%22', query)
            query = re.sub(r' ', '%20', query)
            # raise Exception("Don't get response")

            # get the query response from solr, get the records from response
            response = requests.get("http://localhost:8983/solr/amazon/select?df=product_name&q=" + query + "&rows=100")
            json_data = json.loads(response.text)
            docs = json_data['response']['docs']
            no_docs = len(docs)

            # create the starting string of results
            result = ""
            if isSpellingWrong:
                result += ''.join(
                    ["<div> Do you mean: <a id='a' href='#a' onclick='redirect(\"{}\")'>".format(returnStr),
                     returnStr, "</a>?<br></div><br>"]
                )
            result += "Results Retrieved:<br>"
            result += "<ol>"

            # retrieve the list of id, product_name and descriptions from results
            id_list = []
            book_list = []
            desc_list = []
            for i in range(no_docs):
                doc = docs[i]
                id_list.append(doc['DocID'][0])
                book_list.append(doc['product_name'][0])
                desc_list.append(doc['description'][0])

            # retrieve corresponding original documents from json file by ranked ids
            feeds = []
            with open(os.path.join(base_dir, "crawl", "amazon_all_withID.json"), mode='r', encoding='utf-8') \
                    as feedsjson:
                feeds_all = json.load(feedsjson)
                for doc_id in id_list:
                    feeds.append(feeds_all[int(doc_id)])
            print("querying speed: ", time.time()-startTime, "seconds")

            # add records into result one by one, each record is an item in ordered list
            for i in range(no_docs):
                result += "<li><ul>"
                doc = feeds[i]
                url = doc['url']
                result = ''.join([result, "<li >", "<a style='color:#73C6B6;font-size:20px;font-weight:bold;' href=\"{}\">".format(url), doc['product_name'], "</a></li>"])
                result = ''.join([result, "<li>Description: ", doc['description'], "</li>"])
                result = ''.join([result, "<li>Customer rating: ", str(doc['ratings']), "</li>"])
                result += "</ul></li><br>"
            result += "</ol>"

            # pass the result string and search css style to template and render
            contextDict['result'] = result
            contextDict['css'] = searchStyle
            return render(request, 'group10/form.html', context=contextDict)
        except:
            # if bug, print stack trace
            traceback.print_exc()
    else:
        # if no query, same as index page
        contextDict['result'] = ""
        contextDict['css'] = indexStyle
        return render(request, 'group10/form.html', context=contextDict)
