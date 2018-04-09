from django.http import HttpResponse
from django.shortcuts import render
import os
import sys
import requests
import json
import traceback
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
from preprocess import Preprocessor




def index(request):
    contextDict = {}
    contextDict['result'] = ""
    return render(request, 'group10/form.html', context=contextDict)


def search(request):
    contextDict = {}
    p = Preprocessor()
    if request.method == 'POST':
        try:
            queryList = p.preprocess(request.POST.get("search"))
            query = '%20AND%20'.join(queryList)
            response = requests.get("http://localhost:8983/solr/amazon/select?df=product_name&q=" + query+"&rows=100")
            json_data = json.loads(response.text)
            docs = json_data['response']['docs']
            no_docs = len(docs)
            result = "Results Retrieved:<br>"
            result += "<ol>"
            # retrieve DocID from results
            id_list = []
            for i in range(no_docs):
                doc = docs[i]
                id_list.append(doc['DocID'][0])
            # retreive corresponding original documents from json file by id
            feeds = []
            with open(os.path.join(base_dir, "crawl", "amazon_all_withID.json"), mode='r', encoding='utf-8') as feedsjson:
                feeds_all = json.load(feedsjson)
                for feed in feeds_all:
                    if feed['DocID'] in id_list:
                        feeds.append(feed)            
            # display in HTMl
            for i in range(no_docs):
                result += "<li><ul>"
                doc = feeds[i]
                result = ''.join([result, "<li>Book title: ", doc['product_name'], "</li>"])
                result = ''.join([result, "<li>Description: ", doc['description'], "</li>"])
                result = ''.join([result, "<li>Rating: ", str(doc['ratings']), "</li>"])
                url = doc['url']
                result = ''.join([result, "<li>Url link: <a href=\"{}\">".format(url), url, "</a></li>"])
                result += "</ul></li><br>"
            result += "</ol>"
            print("query:", query)
            contextDict['result'] = result
            # TODO: do something with data
            return render(request, 'group10/form.html', context=contextDict)
        except Exception as e:
            traceback.print_exc()
    else:
        contextDict['result'] = ""
        return render(request, 'group10/form.html', context=contextDict)
