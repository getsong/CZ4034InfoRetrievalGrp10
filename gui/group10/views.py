from django.http import HttpResponse
from django.shortcuts import render


contextDict = {}


def index(request):
    contextDict['result'] = ""
    return render(request, 'group10/form.html', context=contextDict)


def search(request):
    if request.method == 'POST':
        try:
            contextDict['result'] = "A Lot Of Results Are Retrieved"
            # TODO: do something with data
            return render(request, 'group10/form.html', context=contextDict)
        except:
            return HttpResponse("no such user")
    else:
        contextDict['result'] = ""
        return render(request, 'group10/form.html', context=contextDict)
