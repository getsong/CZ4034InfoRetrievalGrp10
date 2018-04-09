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
            print("query:", query)
            contextDict['result'] = "A Lot Of Results Are Retrieved for keywords: " + query
            # TODO: do something with data
            return render(request, 'group10/form.html', context=contextDict)
        except:
            return HttpResponse("no such user")
    else:
        contextDict['result'] = ""
        return render(request, 'group10/form.html', context=contextDict)
