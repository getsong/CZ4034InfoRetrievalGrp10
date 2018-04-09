from django.http import HttpResponse
from django.shortcuts import render
import os
import sys
import requests
import json
import traceback
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
            for i in range(no_docs):
                result += "<li><ul>"
                doc = docs[i]
                result = ''.join([result, "<li>Book title: ", doc['product_name'][0], "</li>"])
                result = ''.join([result, "<li>Description: ", doc['description'][0], "</li>"])
                result = ''.join([result, "<li>Rating: ", str(doc['ratings'][0]), "</li>"])
                url = doc['url'][0]
                result = ''.join([result, "<li>Url link: <a href=\"{}\">".format(url), url, "</a></li>"])
                result += "</ul></li>"
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
