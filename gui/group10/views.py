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
import re
from sklearn.metrics import jaccard_similarity_score


indexStyle = """
body
{
    background-image: url("C:/Users/daq11/Dropbox/developer/CZ4034/CZ4034InfoRetrievalGrp10/gui/static/book3.jpg");
}

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
    margin: 30px 0 0 1%;
    max-width: 50%;
    float: left;
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


def index(request):
    contextDict = {}
    contextDict['result'] = ""
    contextDict['css'] = indexStyle
    return render(request, 'group10/form.html', context=contextDict)


def search(request):
    contextDict = {}
    p = Preprocessor()
    if request.method == 'POST':
        try:
            queryList = p.preprocess(request.POST.get("search"))
            print('cook:', request.POST.get("cook"), type(request.POST.get("cook")))
            if len(queryList) <= 10:
                twoGramList = [''.join(['\"', queryList[i], ' ', queryList[i + 1], '\"^10']) for i in
                               range(len(queryList) - 1)]
                combiList = [''.join(['(', queryList[i], ' AND ', queryList[j], ')^3']) for i in range(len(queryList))
                             for j in range(i + 1, len(queryList)) if queryList[i] != queryList[j]]
                query = ' '.join(twoGramList + combiList + queryList)
            else:
                query = ' '.join(queryList)
            query = re.sub(r'\"', '%22', query)
            query = re.sub(r' ', '%20', query)
            raise Exception("Don't get response")
            response = requests.get("http://localhost:8983/solr/amazon/select?df=product_name&q=" + query + "&rows=100")
            json_data = json.loads(response.text)
            docs = json_data['response']['docs']
            no_docs = len(docs)
            result = "Results Retrieved:<br>"
            result += "<ol>"
            # retrieve DocID from results
            id_list = []
            book_list = []
            desc_list = []
            for i in range(no_docs):
                doc = docs[i]
                id_list.append(doc['DocID'][0])
                book_list.append(doc['product_name'][0])
                desc_list.append(doc['description'][0])
            # retreive corresponding original documents from json file by id
            feeds = []
            with open(os.path.join(base_dir, "crawl", "amazon_all_withID.json"), mode='r', encoding='utf-8') as feedsjson:
                feeds_all = json.load(feedsjson)
                for doc_id in id_list:
                    feeds.append(feeds_all[int(doc_id)])
            # display in HTMl
            for i in range(no_docs):
                result += "<li><ul>"
                doc = feeds[i]
                url = doc['url']
                result = ''.join([result, "<li >", "<a style='color:darkblue;font-size=35px;font-weight:bold;' href=\"{}\">".format(url), doc['product_name'], "</a></li>"])
                result = ''.join([result, "<li>Description: ", doc['description'], "</li>"])
                result = ''.join([result, "<li>Customer rating: ", str(doc['ratings']), "</li>"])
                result += "</ul></li><br>"
            result += "</ol>"
            print("query:", query)

            contextDict['result'] = result
            contextDict['css'] = searchStyle
            return render(request, 'group10/form.html', context=contextDict)
        except:
            traceback.print_exc()
    else:
        contextDict['result'] = ""
        contextDict['css'] = indexStyle
        return render(request, 'group10/form.html', context=contextDict)
