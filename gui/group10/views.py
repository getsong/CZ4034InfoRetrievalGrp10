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


indexStyle = """.title
{
    text-align: center;
    margin: 17% 0 0 0;
}

.search-bar
{
    float:center;
    margin: 50px 0 0 33%;
    min-width: 500px;
    text-align: center;
}"""

os_str = os.path.join(base_dir, 'gui', 'static', 'book3.jpg')
os_str = re.sub(r"\\",'/',os_str)
                    

searchStyle = """
.title
{
	margin: 30px 0 0 1%;
	max-width: 50%;
	float: left;
}

.search-bar
{
	margin: 40px 0 20px 100px;
	min-width: 500px;
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
            query = '%20AND%20'.join(queryList)
            response = requests.get("http://localhost:8983/solr/amazon/select?df=product_name&q=" + query+"&rows=100")
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
                for feed in feeds_all:
                    if feed['DocID'] in id_list:
                        feeds.append(feed)
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
            i = 0
            for book in book_list:
                print("Jaccard Similarity score:" ,jaccard_similarity_score(' '.join(queryList), ' '.join([book,desc_list[i]]), normalize=True))
                i += 1
            contextDict['result'] = result
            contextDict['css'] = searchStyle
            return render(request, 'group10/form.html', context=contextDict)
        except:
            traceback.print_exc()
    else:
        contextDict['result'] = ""
        contextDict['css'] = indexStyle
        return render(request, 'group10/form.html', context=contextDict)
