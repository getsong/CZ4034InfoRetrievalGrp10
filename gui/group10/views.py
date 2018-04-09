from django.http import HttpResponse
from django.shortcuts import render
import os, sys
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
            query = ' '.join(queryList)
            result 
            print("query:", query)
            contextDict['result'] = "A Lot Of Results Are Retrieved for keywords: " + query
            # TODO: do something with data
            return render(request, 'group10/form.html', context=contextDict)
        except:
            return HttpResponse("no such user")
    else:
        contextDict['result'] = ""
        return render(request, 'group10/form.html', context=contextDict)
    
    
    
    
import requests
import json

response = requests.get("http://localhost:8983/solr/amazon/select?df=product_name&q=perfect%20AND%20cook")
json_data = json.loads(response.text)
docs = json_data['response']['docs']
no_docs = json_data['response']['numFound']
for i in range(no_docs):
    doc = docs[i]
    print("book title:",doc['product_name'][0])
    print("description:",doc['description'][0])
    print("rating:",doc['ratings'][0])
    print("url link:",doc['url'][0],'\n')
